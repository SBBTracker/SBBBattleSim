import collections
import logging
import random
from collections import OrderedDict, defaultdict

from sbbbattlesim import utils
from sbbbattlesim.action import Damage
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import EventManager, OnStart
from sbbbattlesim.heros import registry as hero_registry
from sbbbattlesim.spells import registry as spell_registry, TargetedSpell
from sbbbattlesim.treasures import registry as treasure_registry
from collections import defaultdict

logger = logging.getLogger(__name__)


class CastSpellOnStart(OnStart):
    def handle(self, *args, **kwargs):
        self.player.cast_spell(self.spell, trigger_onspell=False)


class Player(EventManager):
    def __init__(self, characters, id, board, treasures, hero, hand, spells, level=0, raw=False, *args, **kwargs):
        super().__init__()
        # Board is board
        self.board = board

        self.stateful_effects = {}

        self.id = id
        self.opponent = None
        self.level = level
        self._last_attacker = None
        self._attack_chain = 0

        #TODO Make a better implementation of this later
        if 'spells_cast' in kwargs:
            self._spells_cast = kwargs['spells_cast']
        else:
            self._spells_cast = None

        self.__characters = OrderedDict({i: None for i in range(1, 8)})

        self._attack_slot = None
        self.graveyard = []

        self.treasures = collections.defaultdict(list)
        mimic = 'SBB_TREASURE_TREASURECHEST' in treasures
        for tres in treasures:
            treasure = treasure_registry[tres]
            mimic_count = mimic + ((hero == 'SBB_HERO_THECOLLECTOR') if treasure._level <= 3 else 0)
            treasure = treasure(player=self, mimic=mimic_count)
            logger.debug(f'{self.id} Registering treasure {treasure.pretty_print()}')
            self.treasures[treasure.id].append(treasure)

        self.hand = [character_registry[char_data['id']](player=self, **char_data) for char_data in hand]
        self.hero = hero_registry[hero](player=self, *args, **kwargs)
        logger.debug(f'{self.id} registering hero {self.hero.pretty_print()}')

        import copy
        for spl in spells:
            if spl in utils.START_OF_FIGHT_SPELLS:
                priority = spell_registry[spl]().priority
                self.board.register(CastSpellOnStart, spell=spl, player=self, priority=priority)

        for char_data in characters:
            char = character_registry[char_data['id']](player=self, **char_data)
            logger.debug(f'{self.id} registering character {char.pretty_print()}')
            self.__characters[char.position] = char

        # This is designed to remove temp buffs that were passed in
        singingswords = 'SBB_TREASURE_WHIRLINGBLADES' in treasures
        attack_multiplier = 1
        if singingswords:
            attack_multiplier = 2
            if mimic:
                attack_multiplier = 3

        if raw:
            for char in self.__characters.values():
                if char:
                    char._base_health -= char._temp_health
                    char._base_attack -= int(char._temp_attack/attack_multiplier)
                    
        self.aura_buffs = set()
        for char in self.valid_characters():
            if char.aura and char.aura_buff:
                try:
                    self.aura_buffs.update(set(char.aura_buff))
                except TypeError:
                    self.aura_buffs.add(char.aura_buff)

            if char.player_buff is not None:
                char.player_buff.execute()

        for tid, tl in self.treasures.items():
            if tid == '''SBB_TREASURE_WHIRLINGBLADES''':
                continue

            for treasure in tl:
                if treasure.aura and treasure.aura_buff:
                    try:
                        self.aura_buffs.update(set(treasure.aura_buff))
                    except TypeError:
                        self.aura_buffs.add(treasure.aura_buff)

    def pretty_print(self):
        return f'{self.id} {", ".join([char.pretty_print() if char else "_" for char in self.characters.values()])}'

    def get_attack_slot(self):
        if self._attack_slot is None:
            self._attack_slot = 1

        # Handle case where tokens are spawning in the same position
        # With the max chain of 5 as implemented to stop trophy hunter + croc + grim soul shenanigans
        if (self.characters.get(self._attack_slot) is self._last_attacker) or (self._attack_chain >= 5) or (self._last_attacker is None):
            # Prevents the same character from attacking repeatedly
            if self._last_attacker is not None:
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
        else:
            return None

        return self._attack_slot

    def spawn(self, character, position):
        logger.info(f'Spawning {character.pretty_print()} in {position} position')
        self.__characters[position] = character
        character.position = position

        support_positions = utils.get_behind_targets(position)
        possible_supports = self.valid_characters(_lambda=lambda char: char.position in support_positions and char.support and char.support_buff)
        support_buffs = {char.support_buff for char in possible_supports}
        for buff in sorted(support_buffs | self.aura_buffs, key=lambda b: b.priority, reverse=True):
            buff.execute(character)

        if character.player_buff:
            character.player_buff.execute()

        return character

    def despawn(self, character):
        logger.info(f'Despawning {character.pretty_print()}')
        position = character.position
        self.graveyard.append(character)
        self.__characters[position] = None
        logger.info(f'{character.pretty_print()} died')

        if character.support and character.support_buff:
            character.support_buff.roll_back()

        if character.aura and character.aura_buff:
            character.aura_buff.roll_back()

    @property
    def characters(self):
        return {pos: char for pos, char in self.__characters.items()}

    def summon_from_different_locations(self, characters, *args, **kwargs):
        '''Pumpkin King spawns each evil unit at the location a prior one died. This means that we need to be
        able to summon from multiple points at once before running the onsummon stack. This may be useful
        for other things too'''
        summoned_characters = [self.spawn(char, char.position) for char in characters]

        self('OnSummon', summoned_characters=summoned_characters)

        return summoned_characters

    def summon(self, pos, characters, *args, **kwargs):
        summoned_characters = []
        spawn_order = utils.get_spawn_positions(pos)
        for char in characters:
            pos = next((pos for pos in spawn_order if self.__characters.get(pos) is None), None)
            if pos is None:
                break

            summoned_characters.append(self.spawn(char, pos))

        # The player handles on-summon effects
        stack = self('OnSummon', summoned_characters=summoned_characters)

        return summoned_characters

    def transform(self, pos, character, *args, **kwargs):
        if self.__characters[pos] is not None:
            self.spawn(character, pos)

            # TODO wrap this into a nice helper function to be used in the attack slot getter as well
            if self._attack_slot == pos:
                self._attack_slot += 1
                if self._attack_slot > 7:
                    self.attack_slot = 1

    def valid_characters(self, _lambda=lambda char: True):
        """
        Return a list of valid characters based on an optional lambda that is passed in as an additoinal filter
        onto the base lambda that guarantees that the character exists and is not dead
        """
        # NOTE: this assumes that a dead thing can NEVER be targeted
        base_lambda = lambda char: char is not None and not char.dead

        return [char for char in self.__characters.values() if base_lambda(char) and _lambda(char)]

    def cast_spell(self, spell_id, trigger_onspell=True):
        spell = spell_registry[spell_id]()
        if spell is None:
            return

        target = None
        if spell.targeted:
            valid_targets = self.valid_characters(_lambda=spell.filter)
            if valid_targets:
                target = random.choice(valid_targets)

        if isinstance(spell, TargetedSpell) and target is None:
            return

        logger.debug(f'{self.id} casting {spell}')

        stack = None
        if trigger_onspell:  # for spells in the passed-in list of spells cast, do not increment
            if self._spells_cast is None:
                self._spells_cast = 0
            self._spells_cast += 1

            stack = self('OnSpellCast', caster=self, spell=spell, target=target)

        spell.cast(player=self, target=target, stack=stack)

