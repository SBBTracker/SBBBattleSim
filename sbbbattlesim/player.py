import logging
from collections import OrderedDict

from sbbbattlesim.treasures import registry as treasure_registry
from sbbbattlesim.heros import registry as hero_registry
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim import utils
from sbbbattlesim.events import EventManager

logger = logging.getLogger(__name__)


class Player(EventManager):
    def __init__(self, characters, treasures, hero, hand):
        super().__init__()
        self.opponent = None
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

    @property
    def front(self):
        return dict(list(self.characters.items())[:4])

    @property
    def back(self):
        return dict(list(self.characters.items())[4:])

    @property
    def attack_character(self):
        for _ in range(7):
            character = self.characters[self._attack_slot]
            if character is not None:
                if character.attack > 0:
                    break

            if self._attack_slot == 7:
                self._attack_slot = 0
            self._attack_slot += 1

        return self.characters.get(self._attack_slot)

    def resolve_board(self):
        # Remove all bonus'
        for pos, char in self.characters.items():
            if char is None:
                continue

            char.attack_bonus, char.health_bonus = 0, 0
            char.clear_temp()

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

                # On Support Event Trigger
                # Maybe this only needs to trigger once
                # self('Support', support_target=buff_target)

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

        for pos, char in self.characters.items():
            if char is None:
                continue

            if char.dead:
                dead_characters.append(char)
                action_taken = True

                self.graveyard.append(char)
                self.characters[pos] = None

                logger.info(f'{char} died')

        for char in dead_characters:
            char('OnDeath', *args,  **kwargs)
            logger.info(f'ONDEATH COMPLETED HERE!!!!!!!!!')

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

        # TODO Summong Portal

        return summoned_characters

    def valid_characters(self, _lambda=lambda char : char is not None and not char.dead):
        """
        Return a list of valid characters based on an optional lambda that is passed in.
        You probably do not need to pass in a lambda, so the default behavior is "return all characters that exist and
        are not dead" effectively filtering out empty board slots.
        """

        return [char for char in self.characters.values() if _lambda(char)]


    # TODO Calculate Damage