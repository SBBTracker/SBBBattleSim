import collections
import logging
import random
from collections import OrderedDict, defaultdict

from sbbbattlesim import utils
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import EventManager, OnStart, OnSetup
from sbbbattlesim.heroes import registry as hero_registry
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.treasures import registry as treasure_registry

logger = logging.getLogger(__name__)


class CastSpellOnStart(OnStart):
    def handle(self, *args, **kwargs):
        self.source.cast_spell(self.kwargs['spell'], trigger_onspell=False)


class PlayerOnSetup(OnSetup):
    def handle(self, stack, *args, **kwargs):
        # TODO Change setup to True when raw gets removed
        setup = self.kwargs.get('raw', False)

        for char in self.source.valid_characters():
            # Apply existing buffs
            support_positions = (5, 6, 7) if self.source.banner_of_command else utils.get_behind_targets(char.position)
            support_units = self.source.valid_characters(_lambda=lambda char: (char.position in support_positions and char.support))
            support_buffs = set([char.support for char in support_units])
            for buff in sorted(self.source.auras | support_buffs, key=lambda b: b.priority, reverse=True):
                buff.execute(char, setup=setup)


class Player(EventManager):
    def __init__(self, id, characters, treasures, hero, hand, spells, level=0, raw=False, *args, **kwargs):
        raw=True
        super().__init__()

        self.id = id
        self.__characters = OrderedDict({i: None for i in range(1, 8)})

        self.register(PlayerOnSetup, source=self, priority=0, raw=raw)

        self.stateful_effects = {}
        self._attack_slot = None
        self.graveyard = []
        self.id = id
        self.opponent = None
        self.level = level
        self._last_attacker = None
        self._attack_chain = 0
        self._spells_cast = kwargs.get('spells_cast', None)
        self.spells = spells

        # Treasure Counting
        self.banner_of_command = 'SBB_TREASURE_BANNEROFCOMMAND' in treasures
        evileye = 'SBB_TREASURE_HELMOFCOMMAND' in treasures
        mimic = 'SBB_TREASURE_TREASURECHEST' in treasures

        self.support_itr = 1
        if evileye:
            self.support_itr = 2
            if mimic:
                self.support_itr = 3
        logger.debug(f'{self.id} support_itr = {self.support_itr}')

        self.auras = set()

        self.treasures = collections.defaultdict(list)
        for tres in treasures:
            treasure = treasure_registry[tres]
            mimic_count = mimic + ((hero == 'SBB_HERO_THECOLLECTOR') if treasure._level <= 3 else 0)
            treasure = treasure(player=self, mimic=mimic_count)
            logger.debug(f'{self.id} Registering treasure {treasure.pretty_print()}')
            self.treasures[treasure.id].append(treasure)

        self.hero = hero_registry[hero](player=self, *args, **kwargs)
        if not self.hero.id:
            self.hero.id = hero
        logger.debug(f'{self.id} registering hero {self.hero.pretty_print()}')

        for spl in spells:
            if spl in utils.START_OF_FIGHT_SPELLS:
                self.register(CastSpellOnStart, spell=spl, source=self, priority=spell_registry[spl].priority)

        for char_data in characters:
            char = character_registry[char_data['id']](player=self, **char_data)
            logger.debug(f'{self.id} registering character {char.pretty_print()}')
            self.__characters[char.position] = char

        for char in self.valid_characters():
            if char.aura:
                try:
                    self.auras.update(set(char.aura))
                except TypeError:
                    self.auras.add(char.aura)

        for tid, tl in self.treasures.items():
            for treasure in tl:
                if treasure.aura and treasure.aura:
                    try:
                        self.auras.update(set(treasure.aura))
                    except TypeError:
                        self.auras.add(treasure.aura)

        if self.hero.aura:
            try:
                self.auras.update(set(self.hero.aura))
            except TypeError:
                self.auras.add(self.hero.aura)

        self.hand = [character_registry[char_data['id']](player=self, **char_data) for char_data in hand if isinstance(char_data, dict) and 'id' in char_data and char_data['id'].startswith('SBB_CHARACTER')]

        for aura in self.auras:
            logger.debug(f'{self.id} found aura {aura}')

    def pretty_print(self):
        return f'{self.id} {", ".join([char.pretty_print() if char else "_" for char in self.characters.values()])}'

    def get_attack_slot(self):
        if self._attack_slot is None:
            self._attack_slot = 1

        # Handle case where tokens are spawning in the same position
        # With the max chain of 5 as implemented to stop trophy hunter + croc + grim soul shenanigans
        attack_slot_char = self.characters.get(self._attack_slot)

        if (self._attack_chain >= 5) or (self._last_attacker is None) or (attack_slot_char is not None and attack_slot_char.has_attacked):
            # Prevents the same character from attacking repeatedly
            if self._last_attacker is not None:
                self._last_attacker.has_attacked = False
                self._attack_slot += 1
            self._attack_chain = 0
        else:
            self._attack_chain += 1

        # If we are advancing the attack slot do it here
        found_attacker = False
        for _ in range(8):
            character = self.characters.get(self._attack_slot)
            if character is not None:
                if character.attack > 0:
                    found_attacker = True
                    break
            self._attack_slot += 1

            if self._attack_slot >= 8:
                self._attack_slot = 1

        # If we have not found an attacker just return None
        if found_attacker:
            self._last_attacker = self.characters.get(self._attack_slot)
            self._last_attacker.has_attacked = True
        else:
            return None

        return self._attack_slot

    def spawn(self, character, position):
        logger.info(f'Spawning {character.pretty_print()} in {position} position')

        # all my spawning homies hate temporary events
        for action in character._action_history:
            if action.temp:
                action.roll_back(character)

        self.__characters[position] = character
        character.position = position

        # Apply existing buffs
        support_positions = (5, 6, 7) if self.banner_of_command else utils.get_behind_targets(position)
        support_units = self.valid_characters(_lambda=lambda char: (char.position in support_positions and char.support))
        support_buffs = set([char.support for char in support_units])
        for buff in sorted(self.auras | support_buffs, key=lambda b: b.priority, reverse=True):
            buff.execute(character)

        # Apply new support buffs
        if character.support:
            pos_ls = utils.get_support_targets(position, self.banner_of_command)
            character.support.execute(*self.valid_characters(_lambda=lambda char: char.position in pos_ls))

        # Apply new auras
        if character.aura:
            try:
                self.auras.update(set(character.aura))
            except TypeError:
                self.auras.add(character.aura)
            character.aura.execute(*self.valid_characters())

        character('OnSpawn')

        return character

    def despawn(self, *characters, **kwargs):
        kill = kwargs.get('kill', True)

        # This is only false for transform effects
        for char in characters:
            logger.info(f'Despawning {char.pretty_print()}')
            position = char.position
            self.__characters[position] = None

            if kill:
                self.graveyard.append(char)
                logger.info(f'{char.pretty_print()} died')

            char('Despawn', **kwargs)

        if kill:
            for char in characters:
                char('OnDeath', **kwargs)

        for char in characters:
            if char.support:
                char.support.roll_back()

            if char.aura:
                logger.debug(f'{self.id} Auras for spawning is {self.auras}')

                try:
                    self.auras -= set(char.aura)
                except TypeError:
                    try:
                        self.auras.remove(char.aura)
                    except KeyError:
                        pass

                char.aura.roll_back()

    @property
    def characters(self):
        return {pos: char for pos, char in self.__characters.items()}

    def summon_from_different_locations(self, characters, *args, **kwargs):
        '''Pumpkin King spawns each evil unit at the location a prior one died. This means that we need to be
        able to summon from multiple points at once before running the onsummon stack. This may be useful
        for other things too'''

        final_summoned_characters = []
        pos2char = defaultdict(list)
        for char in characters:
            pos2char[char.position].append(char)

        for pos, char_ls in pos2char.items():
            final_summoned_characters.extend(self.summon(pos, char_ls, onsummon=False))

        stack = self('OnSummon', summoned_characters=final_summoned_characters)

        return final_summoned_characters

    def summon(self, pos, characters, onsummon=True, *args, **kwargs):
        summoned_characters = []
        spawn_order = utils.get_spawn_positions(pos)
        for char in characters:
            pos = next((pos for pos in spawn_order if self.__characters.get(pos) is None), None)
            if pos is None:
                break

            summoned_characters.append(self.spawn(char, pos))

        # The player handles on-summon effects
        if onsummon:
            stack = self('OnSummon', summoned_characters=summoned_characters)

        return summoned_characters

    def transform(self, pos, character, *args, **kwargs):
        char_to_transform = self.__characters[pos]
        if char_to_transform is not None:
            character.has_attacked = char_to_transform.has_attacked
            self.despawn(char_to_transform, kill=False)
            self.spawn(character, pos)

    def valid_characters(self, _lambda=lambda char: True):
        """
        Return a list of valid characters based on an optional lambda that is passed in as an additoinal filter
        onto the base lambda that guarantees that the character exists and is not dead
        """
        # NOTE: this assumes that a dead thing can NEVER be targeted
        base_lambda = lambda char: char is not None and not char.dead and char.health > 0

        return [char for char in self.__characters.values() if base_lambda(char) and _lambda(char)]

    def cast_spell(self, spell_id, trigger_onspell=True):
        spell = spell_registry[spell_id]
        if spell is None:
            return

        target = None
        if spell.targeted:
            valid_targets = self.valid_characters(_lambda=spell.filter)
            if valid_targets:
                target = random.choice(valid_targets)

        if spell.targeted and target is None:
            return

        logger.debug(f'{self.id} casting {spell}')

        stack = None
        if trigger_onspell:  # for spells in the passed-in list of spells cast, do not increment
            if self._spells_cast is None:
                self._spells_cast = 0
            self._spells_cast += 1

            stack = self('OnSpellCast', caster=self, spell=spell, target=target)

        spell(self).cast(target=target)

    def to_state(self):
        # Need to case the tribes from enum to their strings
        treasures = [key for key, value in self.treasures.items() for treasure in value ]

        characters = [
            {
                'position': slot,
                'id': character.id,
                'attack': character.attack,
                'health': character.health,
                'golden': character.golden,
                'cost': character.cost,
                'tribes': [tribe.name.lower() for tribe in character.tribes],
            }
            for slot, character in self.__characters.items()
            if character is not None
        ]
        hero = self.hero.id
        spells = list(self.spells)
        hand = [
            {
                'slot': 0,
                'id': character.id,
                'attack': character.attack,
                'health': character.health,
                'golden': character.golden,
                'cost': character.cost,
                'tribes': [tribe.name.lower() for tribe in character.tribes],
            }
            for character in self.hand
        ]

        return {
            'characters': characters,
            'treasures': treasures,
            'hero': hero,
            'spells': spells,
            'hand': hand,
            'level': self.level,
        }
