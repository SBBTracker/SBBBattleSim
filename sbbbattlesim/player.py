import collections
import logging
import random
import typing
from collections import OrderedDict, defaultdict
from functools import cached_property

from sbbbattlesim import utils
from sbbbattlesim.action import Aura, Support
from sbbbattlesim.characters import registry as character_registry, Character
from sbbbattlesim.events import EventManager, OnStart, OnSetup
from sbbbattlesim.heroes import registry as hero_registry
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.treasures import registry as treasure_registry, Treasure

logger = logging.getLogger(__name__)


class CastSpellOnStart(OnStart):
    def handle(self, *args, **kwargs):
        self.source.cast_spell(self.kwargs['spell'], trigger_onspell=False)


class Player(EventManager):
    def __init__(
            self,
            id: str,
            hero: str,
            characters: (typing.List[dict], None) = None,
            treasures: (typing.List[dict], None) = None,
            hand: (typing.List[dict], None) = None,
            spells: (typing.List[dict], None) = None,
            level: int = 0,
            raw=False,
            *args,
            **kwargs
    ):
        # DO NOT TOUCH
        raw = True
        super().__init__()
        self.player = self
        # DO NOT TOUCH

        # Base Values
        self.id = id
        self.__characters = OrderedDict({i: None for i in range(1, 8)})
        self.treasures = []
        self.hand = []
        self.spells = spells or []
        self.auras = set()
        self.level = level

        # Hidden Counters
        self._spells_cast = kwargs.get('spells_cast', None)
        self._puff_puff_counter = kwargs.get('puff_puff_counter', None)

        # Base Setup
        self.hero = hero_registry[hero](player=self, *args, **kwargs)
        logger.debug(f'{self.id} registering hero {self.hero.pretty_print()} {self.hero.id}')

        if treasures:
            self.add_treasure(*treasures)

        if characters:
            for char_data in characters:
                # This does not use self.add_character as that currently uses spawn
                char = character_registry[char_data['id']](player=self, **char_data)
                logger.debug(f'{self.id} registering character {char.pretty_print()}')
                self.__characters[char.position] = char

        if hand:
            for char_data in hand:
                try:
                    char_id = char_data['id']
                except KeyError:
                    char_id = char_data

                if not char_id.startswith('SBB_CHARACTER'):
                    continue

                self.add_character_to_hand(char_data)

        # Combat values
        self.opponent = None
        self.stateful_effects = {}  # Currently only used for old puff puff logic. TODO: redo logic to use new hidden counter
        self._attack_slot = None
        self.graveyard = []
        self._last_attacker = None
        self._attack_chain = 0
        self.action_counters = collections.defaultdict(int)

        # Gather and apply auras from creatures assumed to be on the player
        # NOTE: Aura priority is independent of Support priority and this *could* change
        auras = set()
        if self.hero.aura:
            try:
                auras.update(set(self.hero.aura))
            except TypeError:
                auras.add(self.hero.aura)

        for char in self.valid_characters():
            if char.aura:
                try:
                    auras.update(set(char.aura))
                except TypeError:
                    auras.add(char.aura)

        for treasure in self.treasures:
            if treasure.aura:
                try:
                    auras.update(set(treasure.aura))
                except TypeError:
                    auras.add(treasure.aura)

        for aura in auras:
            logger.debug(f'{self.id} found aura {aura}')

        self.add_aura(*auras, setup=raw)

        # Apply support buffs from creatures assumed to be on the player
        banner = self.banner_of_command
        front = (1, 2, 3, 4)
        back = (5, 6, 7)
        support_characters = self.valid_characters(_lambda=lambda char: char.position in back and char.support)
        for char in sorted(support_characters, key=lambda char: char.support.priority, reverse=True):
            support_targets = front if banner else utils.get_support_targets(char.position)
            char.support.execute(*self.valid_characters(_lambda=lambda char: char.position in support_targets), setup=raw)

    def pretty_print(self):
        return f'{self.id} {", ".join([char.pretty_print() if char else "_" for char in self.characters.values()])}'

    def replace_hero(self, hero_id: str, *args, **kwargs):
        self.hero = hero_registry[hero_id](player=self, *args, **kwargs)
        logger.debug(f'{self.id} registering hero {self.hero.pretty_print()} {self.hero.id}')

    def add_character(self, char: (str, dict, Character)) -> Character:
        if isinstance(char, str):
            char = character_registry[char].new(player=self, position=0, golden=False)
        elif isinstance(char, dict):
            char = character_registry[char['id']](player=self, **char)
        # TODO This either needs to always use spawn logic or implment something else
        self.spawn(char, char.position)
        return char

    def remove_character(self, position: int):
        char = self.__characters.get(position)
        if char:
            # TODO: This either needs to always use despawn logic or implement something else
            self.despawn(char, kill=False)

    def add_character_to_hand(self, char: (str, dict, Character)) -> Character:
        if isinstance(char, str):
            char = character_registry[char].new(player=self, position=0, golden=False)
        elif isinstance(char, dict):
            char = character_registry[char['id']](player=self, **char)
        logger.debug(f'{self.id} adding character {char.pretty_print()} to hand')
        self.hand.append(char)
        return char

    # TODO: Do we need a remove from hand option or should that be on the user since Player.hand is a public list?

    def add_treasure(self, *treasure_ids: typing.List[str]):
        for treasure_id in treasure_ids:
            if len(self.treasures) >= 3:
                return

            treasure = treasure_registry[treasure_id]
            mimic = 'SBB_TREASURE_TREASURECHEST' in treasure_ids
            multiplier = mimic + ((self.hero.id == 'SBB_HERO_THECOLLECTOR') if treasure._level <= 3 else 0)
            treasure = treasure(player=self, multiplier=multiplier)
            logger.debug(f'{self.id} Registering treasure {treasure.pretty_print()}')
            self.treasures.append(treasure)

    @property
    def banner_of_command(self):
        return 'SBB_TREASURE_BANNEROFCOMMAND' in [treasure.id for treasure in self.treasures]

    @property
    def support_itr(self):
        treasure_ids = [treasure.id for treasure in self.treasures]
        evileye = 'SBB_TREASURE_HELMOFCOMMAND' in treasure_ids
        mimic = 'SBB_TREASURE_TREASURECHEST' in treasure_ids

        support_itr = 1
        if evileye:
            support_itr = 2
            if mimic:
                support_itr = 3

        return support_itr

    def add_aura(self, *auras: Aura, **kwargs):
        auras = set(sorted(auras, key=lambda aura: aura.priority, reverse=True))

        for aura in auras:
            aura.execute(*self.valid_characters(), **kwargs)

        self.auras.update(auras)

    def prepare_combat(self):
        self.opponent = None
        self.stateful_effects = {}  # Currently only used for old puff puff logic. TODO: redo logic to use new hidden counter
        self._attack_slot = None
        self.graveyard = []
        self._last_attacker = None
        self._attack_chain = 0
        self.action_counters = collections.defaultdict(int)

        for spl in self.spells:
            if spl in utils.START_OF_FIGHT_SPELLS:
                self.register(CastSpellOnStart, spell=spl, source=self, priority=spell_registry[spl].priority)

    def resolve_combat(self):
        self.opponent = None
        self.stateful_effects = {}  # Currently only used for old puff puff logic. TODO: redo logic to use new hidden counter
        self._attack_slot = None
        self.graveyard = []
        self._last_attacker = None
        self._attack_chain = 0

        if 'OnSetup' in self._events:
            self._events.pop('OnSetup')

        if 'OnStart' in self._events:
            self._events.pop('OnStart')

    def get_attack_slot(self) -> (int, None):
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

    def spawn(self, character: 'Character', position: int):
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
        if character.support and character.position in (5, 6, 7):
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

    def despawn(self, *characters: 'Character', **kwargs):
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
    def characters(self) -> typing.Dict[int, 'Character']:
        return {pos: char for pos, char in self.__characters.items()}

    def summon_from_different_locations(self, characters: typing.List['Character'], *args, **kwargs) -> typing.List['Character']:
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

    def summon(self, pos: int, characters: typing.List['Character'], onsummon: bool = True, *args, **kwargs) -> typing.List['Character']:
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

    def transform(self, pos: int, character: 'Character', *args, **kwargs):
        char_to_transform = self.__characters[pos]
        if char_to_transform is not None:
            character.has_attacked = char_to_transform.has_attacked
            self.despawn(char_to_transform, kill=False)
            self.spawn(character, pos)

    def valid_characters(self, _lambda: typing.Callable[[Character], bool] = lambda char: True) -> typing.List['Character']:
        """
        Return a list of valid characters based on an optional lambda that is passed in as an additoinal filter
        onto the base lambda that guarantees that the character exists and is not dead
        """
        # NOTE: this assumes that a dead thing can NEVER be targeted
        base_lambda = lambda char: char is not None and not char.dead and char.health > 0

        return [char for char in self.__characters.values() if base_lambda(char) and _lambda(char)]

    def cast_spell(self, spell_id: str, trigger_onspell: bool = True):
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
