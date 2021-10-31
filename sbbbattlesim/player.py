import logging
from collections import OrderedDict

from sbbbattlesim.treasures import registry as treasure_registry
from sbbbattlesim.heros import registry as hero_registry
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim import utils
from sbbbattlesim.events import EventManager

logger = logging.getLogger(__name__)


class Player(EventManager):
    def __init__(self, characters, treasures, hero, hand, id, board):
        super().__init__()
        # Board is board
        self.board = board

        self.id = id
        self.opponent = None
        self._last_attacker = None
        self._attack_chain = 0
        self.characters = OrderedDict({i: None for i in range(1, 8)})

        def make_character(char_data):
            return character_registry[char_data['id']](
                owner=self,
                position=char_data.get('position'),
                attack=char_data['attack'],
                health=char_data['health'],
                golden=char_data['golden'],
                keywords=char_data['keywords'],
                tribes=char_data['tribes'],
                cost=char_data['cost']
            )

        for char_data in characters:
            char = make_character(char_data)
            self.characters[char.position] = char

        self._attack_slot = 1
        self.hand = [make_character(char_data) for char_data in hand]
        self.graveyard = []

        self.treasures = {}
        for tres in treasures:
            treasure = treasure_registry[tres]
            if treasure is not None:
                self.treasures[treasure.id] = treasure()

        self.hero = hero_registry[hero]

        self.stateful_effects = dict()


    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'{self.id} {", ".join([char.__repr__() for char in self.characters.values()])}'

    #TODO Make a pretty print for player

    @property
    def front(self):
        return dict(list(self.characters.items())[:4])

    @property
    def back(self):
        return dict(list(self.characters.items())[4:])

    @property
    def attack_character(self):
        # Handle case where tokens are spawning in the same position
        # With the max chain of 5 as implemented to stop trophy hunter + croc + grim soul shenanigans
        if (self.characters.get(self._attack_slot) == self._last_attacker) or (self._attack_chain >= 5) or (self._last_attacker is None):
            if self._last_attacker is not None:
                self._attack_slot += 1
            self._attack_chain = 0
        else:
            self._attack_chain += 1
            logger.info(f'Attacker is {self._last_attacker}')
            return self._last_attacker

        # If we are advancing the attack slot do it here
        found_attacker = False
        for _ in range(7):
            character = self.characters.get(self._attack_slot)
            if character is not None:
                if character.attack > 0:
                    found_attacker = True
                    break
            self._attack_slot += 1

            if self._attack_slot == 8:
                self._attack_slot = 1

        # If we have not found an attacker just return None
        if found_attacker:
            attacker = self.characters.get(self._attack_slot)
            self._last_attacker = attacker
            logger.info(f'Attacker is {attacker}')
            return attacker
        else:
            logger.info(f'There is no attacker')
            return None

    def resolve_board(self):
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

        # Iterate over buff targets and auras then apply them to all necessary targets
        for pos, char in self.characters.items():
            if char is None:
                continue

            # Support & Aura Targeting
            # This does talk about buffs, but it is for buffs that can only be changed by board state
            buff_targets = []
            if getattr(char, 'support', False):
                buff_targets = utils.get_support_targets(position=char.position,
                                                         horn='SBB_TREASURE_BANNEROFCOMMAND' in self.treasures)
            elif getattr(char, 'aura', False):
                buff_targets = self.characters.keys()

            buff_targets = [self.characters[buff_pos] for buff_pos in buff_targets if self.characters.get(buff_pos)]

            for buff_target in buff_targets:
                char.buff(target_character=buff_target)

            if getattr(char, 'buff_player', False):
                char.buff_player(player=self)

                # On Support Event Trigger
                # Maybe this only needs to trigger once
                # self('Support', support_target=buff_target)

        # Apply buffs from treasures
        for treasure in self.treasures.values():
            if treasure.aura:
                for pos, char in self.characters.items():
                    if char is not None:
                        treasure.buff(char)

        # TODO Add Temporary Event Stuff

    def resolve_damage(self, *args, **kwargs):
        action_taken = False

        # TODO Remove all characters before death triggers

        # Resolve Character Deaths
        dead_characters = []

        logger.debug(f'RESOLVING DAMAGE FOR {self}')

        for pos, char in self.characters.items():
            if char is None:
                continue

            if char.dead:
                dead_characters.append(char)
                action_taken = True

                self.graveyard.append(char)
                self.characters[pos] = None

                logger.info(f'{char} died')

        for char in sorted(dead_characters, key=lambda _char: _char.position, reverse=True):
            char('OnDeath', *args,  **kwargs)

        return action_taken

    def summon(self, pos, *characters):
        summoned_characters = []
        spawn_order = utils.get_spawn_positions(pos)
        for char in characters:
            # TODO This could be better
            pos = next((pos for pos in spawn_order if self.characters.get(pos) is None), None)
            if pos is None:
                break

            self.characters[pos] = char
            summoned_characters.append(char)
            logger.info(f'Spawning {char} in {pos} position')

        # Now that we have summoned units, make sure they have the buffs they should
        self.resolve_board()

        # The player handles on-summon effects
        self('OnSummon', summoned_characters=summoned_characters)

        return summoned_characters

    def valid_characters(self, _lambda=lambda char: True):
        """
        Return a list of valid characters based on an optional lambda that is passed in as an additoinal filter
        onto the base lambda that guarantees that the character exists and is not dead
        """
        # NOTE: this assumes that a dead thing can NEVER be targetted
        base_lambda = lambda char : char is not None and not char.dead

        return [char for char in self.characters.values() if base_lambda(char) and _lambda(char)]


    # TODO Calculate Damage