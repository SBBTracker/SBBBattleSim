import logging
import random
from collections import OrderedDict, defaultdict

from sbbbattlesim import utils
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

        self.stateful_effects = defaultdict(lambda : defaultdict(lambda : None))

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

        self.characters = OrderedDict({i: None for i in range(1, 8)})

        self._attack_slot = None
        self.graveyard = []

        self.treasures = defaultdict(list)
        mimic = 'SBB_TREASURE_TREASURECHEST' in treasures
        for tres in treasures:
            treasure = treasure_registry[tres]
            logger.debug(f'{self.id} Registering treasure {treasure}')
            self.treasures[treasure.id].append(treasure(self, mimic + ((hero == 'SBB_HERO_THECOLLECTOR') if treasure._level <= 3 else 0)))

        self.hand = [character_registry[char_data['id']](owner=self, **char_data) for char_data in hand]
        self.hero = hero_registry[hero](player=self, *args, **kwargs)
        logger.debug(f'{self.id} registering hero {self.hero}')

        import copy
        for spl in spells:
            if spl in utils.START_OF_FIGHT_SPELLS:
                priority = spell_registry[spl]().priority
                self.board.register(CastSpellOnStart, spell=spl, player=self, priority=priority)

        for char_data in characters:
            char = character_registry[char_data['id']](owner=self, **char_data)
            logger.debug(f'{self.id} registering character {char}')
            self.characters[char.position] = char

        # This is designed to remove temp buffs that were passed in
        singingswords = 'SBB_TREASURE_WHIRLINGBLADES' in treasures
        attack_multiplier = 1
        if singingswords:
            attack_multiplier = 2
            if mimic:
                attack_multiplier = 3

        if raw:
            self.resolve_board()
            for char in self.characters.values():
                if char:
                    char._base_health -= char._temp_health
                    char._base_attack -= int(char._temp_attack/attack_multiplier)

    def pretty_print(self):
        return f'{self.id} {", ".join([char.pretty_print() if char else "_" for char in self.characters.values()])}'

    @property
    def attack_slot(self):
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

    def resolve_board(self, *args, **kwargs):

        old_temp_health_dt = {char: char._temp_health for char in self.valid_characters()}

        # Remove all bonuses
        # these need to be prior so that there is not
        # wonky ordering issues with clearing buffs
        # and units that give secondary units buffs that buff
        # arbitrary units
        self.clear_temp()
        for pos, char in self.characters.items():
            if char is None:
                continue
            char.clear_temp()

        # If a stack was passed in through kwargs it will return
        # If a stack wasn't passed it will be generated and returned
        kwargs['stack'] = self('OnResolveBoard', *args, **kwargs)

        # TREASURE BUFFS

        # HERO BUFFS:
        if self.hero.id != "SBB_HERO_PRINCESSBELLE":
            if self.hero.aura:
                for target in self.valid_characters():
                    self.hero.buff(target, *args, **kwargs)

        for t, treasure_ls in self.treasures.items():
            for treasure in treasure_ls:
                if t == "SBB_TREASURE_WHIRLINGBLADES":
                    continue
                if t == "SBB_TREASURE_CLOAKOFTHEASSASSIN":
                    continue
                if treasure.aura:
                    for target in self.valid_characters():
                        treasure.buff(target, *args, **kwargs)

        if self.hero.id == "SBB_HERO_PRINCESSBELLE":
            for target in self.valid_characters():
                self.hero.buff(target, *args, **kwargs)

        # CHARACTER BUFFS
        # Iterate over buff targets and auras then apply them to all necessary targets
        # Support & Aura Targeting
        # This does talk about buffs, but it is for buffs that can only be changed by board state
        support_itr = 1
        if "SBB_TREASURE_HELMOFCOMMAND" in self.treasures:
            if "SBB_TREASURE_TREASURECHEST" in self.treasures:
                support_itr = 3  # mimic and evil eye
            else:
                support_itr = 2  # evil eye but not mimic

        for char in self.valid_characters():
            if char.aura:
                for target in self.valid_characters():
                    char.buff(target, *args, **kwargs)

        for char in self.valid_characters():
            if char.support:
                for _ in range(support_itr):  # my commit but blame regi
                    for target_position in utils.get_support_targets(position=char.position, horn='SBB_TREASURE_BANNEROFCOMMAND' in self.treasures):
                        target = self.characters.get(target_position)
                        if target:
                            char.buff(target, *args, **kwargs)
                            char('OnSupport', buffed=target, support=char, *args, **kwargs)

        cloak_ls = self.treasures.get("SBB_TREASURE_CLOAKOFTHEASSASSIN", False)
        if cloak_ls:
            for target in self.valid_characters():
                cloak_ls[0].buff(target, *args, **kwargs)

        # we need to apply singing swords last
        # TODO Add priority to treasures and sort this loop by that priority
        if "SBB_TREASURE_WHIRLINGBLADES" in self.treasures:
            attack_dt = dict()
            for target in self.valid_characters():
                attack_dt[target] = target.attack
            for target in self.valid_characters():
                self.treasures["SBB_TREASURE_WHIRLINGBLADES"][0].buff(target, attack_override=attack_dt[target], *args, **kwargs)
        new_temp_health_dt = {char: char._temp_health for char in self.valid_characters()}

        for char, new_temp_health in new_temp_health_dt.items():
            old_temp_health = old_temp_health_dt[char]

            if new_temp_health < old_temp_health:
                char._damage -= min(char._damage, old_temp_health - new_temp_health)

        for char in self.valid_characters():
            if char.health < 0:
                char.change_stats(damage=0, source=self, reason=None)

    def summon_from_different_locations(self, characters, *args, **kwargs):
        '''Pumpkin King spawns each evil unit at the location a prior one died. This means that we need to be
        able to summon from multiple points at once before running the onsummon stack. This may be useful
        for other things too'''
        summoned_characters = []
        for char in characters:
            pos = char.position
            self.characters[pos] = char
            summoned_characters.append(self.characters[pos])
            logger.info(f'Spawning {char} in {pos} position')

        # Now that we have summoned units, make sure they have the buffs they should
        self.resolve_board(summoned_characters=summoned_characters, *args, **kwargs)

        self('OnSummon', summoned_characters=summoned_characters)

        return summoned_characters

    def summon(self, pos, characters, *args, **kwargs):
        summoned_characters = []
        spawn_order = utils.get_spawn_positions(pos)
        for char in characters:
            # TODO This could be better
            pos = next((pos for pos in spawn_order if self.characters.get(pos) is None), None)
            if pos is None:
                break

            char.position = pos
            self.characters[pos] = char
            summoned_characters.append(self.characters[pos])
            logger.info(f'Spawning {char} in {pos} position')

        # Now that we have summoned units, make sure they have the buffs they should
        self.resolve_board(summoned_characters=summoned_characters, *args, **kwargs)

        # The player handles on-summon effects
        stack = self('OnSummon', summoned_characters=summoned_characters)

        return summoned_characters

    def transform(self, pos, character, *args, **kwargs):
        if self.characters[pos] is not None:
            self.characters[pos] = character
            self.resolve_board(summoned_characters=[character], *args, **kwargs)

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

        return [char for char in self.characters.values() if base_lambda(char) and _lambda(char)]

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

