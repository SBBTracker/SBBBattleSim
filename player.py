from collections import OrderedDict
from treasures import registry as treasure_registry


class Player:
    def __init__(self, characters, treasures, hero, hand):
        self.player_num = None
        self.characters = OrderedDict({i: None for i in range(1, 8)})

        for slot, character in characters.items():
            character.position = slot
            character.owner = self
            self.characters[slot] = character

        self.treasures = {treasure: treasure_registry[treasure] for treasure in treasures}
        self._attack_slot = 1
        # self.hero = hero
        # self.hand = OrderedDict({i: characters for i, characters in enumerate(hand)})
        # self.graveyard = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'{self.characters}'

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
            self._attack_slot += 1

        return self.characters.get(self._attack_slot)

    def resolve_board(self):
        # Remove all bonus'
        for i, m in self.characters.items():
            if m is None:
                continue

            m.attack_bonus, m.health_bonus = 0, 0
            m.buff_funcs = []

            # Support Targeting
            buff_slots = []
            if getattr(m, 'support', False):
                if self.treasures.get('horn_of_olympus'):
                    buff_slots = [1, 2, 3, 4]
                elif 5 <= m.position <= 7:
                    buff_slots = {5: [1, 2], 6: [2, 3], 7: [3, 4]}[i]

            elif getattr(m, 'aura', False):
                buff_slots = range(1, 8)

            for i in buff_slots:
                buffed_character = self.characters[i]
                if buffed_character:
                    buffed_character.buff_funcs.extend(m.buffs)

        for i, m in self.characters.items():
            if m is None:
                continue
            for buff in m.buff_funcs:
                buff(buff_target=m)

            # TODO Add On Buff Trigger

        #TODO Add treasure effects


    def summon(self, slot, *characters):
        # TODO How do things summon
        summoned_characters = []
        front_row_check = slot <= 4

        # print(f'Characters to Summon {characters}')

        for character in characters:
            #Fill current slot
            # print(f'Current Slot {self.characters[slot] is None}')
            if self.characters[slot] is None:
                self.characters[slot] = character
                character.position = slot
                summoned_characters.append((slot, character))
                continue

            #Right row adjacent
            right_row_avaiable_slot = next((i for i in range(slot, 4 if front_row_check else 7) if self.characters[i] is None), None)
            # print(f'Right Row Adjacent {right_row_avaiable_slot}')
            if right_row_avaiable_slot:
                self.characters[right_row_avaiable_slot] = character
                character.position = right_row_avaiable_slot
                summoned_characters.append((right_row_avaiable_slot, character))
                continue

            #Left row adjacent
            left_row_available_slot = next((i for i in range(slot, 1 if front_row_check else 4, -1) if self.characters[i] is None), None)
            # print(f'Left Row Adjacent {left_row_available_slot}')
            if left_row_available_slot:
                self.characters[left_row_available_slot] = character
                character.position = left_row_available_slot
                summoned_characters.append((left_row_available_slot, character))
                continue

            #Right diagonal adjacent
            right_adjacenties = {0: 4, 1: 5, 2: 6, 4: 2, 5: 2, 6: 3}
            right_diagonal_adjacent_avaialable_slot = right_adjacenties.get(slot)
            # print(f'Right Diagonal Row Adjacent {right_diagonal_adjacent_avaialable_slot}')
            if self.characters.get(right_diagonal_adjacent_avaialable_slot, '') is None:
                self.characters[right_diagonal_adjacent_avaialable_slot] = character
                character.position = right_diagonal_adjacent_avaialable_slot
                summoned_characters.append((right_diagonal_adjacent_avaialable_slot, character))
                continue

            #Left diagonal adjacent
            left_adjacenties = {v: k for k, v in reversed(list(right_adjacenties.items()))}
            left_diagonal_adjacent_avaialable_slot = left_adjacenties.get(slot)
            # print(f'Left Diagonal Row Adjacent {left_diagonal_adjacent_avaialable_slot}')
            if self.characters.get(left_diagonal_adjacent_avaialable_slot, '') is None:
                self.characters[left_diagonal_adjacent_avaialable_slot] = character
                character.position = left_diagonal_adjacent_avaialable_slot
                summoned_characters.append((left_diagonal_adjacent_avaialable_slot, character))
                continue

            any_available_slot = next((i for i, m in self.characters.items() if m is None), None)
            if any_available_slot:
                self.characters[any_available_slot] = character
                character.position = any_available_slot
                summoned_characters.append((any_available_slot, character))
                continue


        # TODO Summong Portal

        return summoned_characters