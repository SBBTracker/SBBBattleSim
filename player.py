from collections import OrderedDict
from treasures import registry as treasure_registry


class Player:
    def __init__(self, minions, treasures, hero, hand):
        self.player_num = None
        self.minions = OrderedDict({i: None for i in range(1, 8)})

        for slot, minion in minions.items():
            minion.position = slot
            minion.owner = self
            self.minions[slot] = minion

        self.treasures = {treasure: treasure_registry[treasure] for treasure in treasures}
        self._attack_slot = 1
        # self.hero = hero
        # self.hand = OrderedDict({i: minion for i, minion in enumerate(hand)})
        # self.graveyard = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'{self.minions}'

    @property
    def front(self):
        return dict(list(self.minions.items())[:4])

    @property
    def back(self):
        return dict(list(self.minions.items())[4:])

    @property
    def attack_minion(self):
        for _ in range(7):
            minion = self.minions[self._attack_slot]
            if minion is not None:
                if minion.attack > 0:
                    break
            self._attack_slot += 1

        return self.minions.get(self._attack_slot)

    def resolve_board(self):
        # Remove all bonus'
        for i, m in self.minions.items():
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
                buffed_minion = self.minions[i]
                if buffed_minion:
                    buffed_minion.buff_funcs.extend(m.buffs)

        for i, m in self.minions.items():
            if m is None:
                continue
            for buff in m.buff_funcs:
                buff(buff_target=m)

            # TODO Add On Buff Trigger

        #TODO Add treasure effects


    def summon(self, slot, *minions):
        # TODO How do things summon
        summoned_minions = []
        front_row_check = slot <= 4

        # print(f'Minions to Summon {minions}')

        for minion in minions:
            #Fill current slot
            # print(f'Current Slot {self.minions[slot] is None}')
            if self.minions[slot] is None:
                self.minions[slot] = minion
                minion.position = slot
                summoned_minions.append((slot, minion))
                continue

            #Right row adjacent
            right_row_avaiable_slot = next((i for i in range(slot, 4 if front_row_check else 7) if self.minions[i] is None), None)
            # print(f'Right Row Adjacent {right_row_avaiable_slot}')
            if right_row_avaiable_slot:
                self.minions[right_row_avaiable_slot] = minion
                minion.position = right_row_avaiable_slot
                summoned_minions.append((right_row_avaiable_slot, minion))
                continue

            #Left row adjacent
            left_row_available_slot = next((i for i in range(slot, 1 if front_row_check else 4, -1) if self.minions[i] is None), None)
            # print(f'Left Row Adjacent {left_row_available_slot}')
            if left_row_available_slot:
                self.minions[left_row_available_slot] = minion
                minion.position = left_row_available_slot
                summoned_minions.append((left_row_available_slot, minion))
                continue

            #Right diagonal adjacent
            right_adjacenties = {0: 4, 1: 5, 2: 6, 4: 2, 5: 2, 6: 3}
            right_diagonal_adjacent_avaialable_slot = right_adjacenties.get(slot)
            # print(f'Right Diagonal Row Adjacent {right_diagonal_adjacent_avaialable_slot}')
            if self.minions.get(right_diagonal_adjacent_avaialable_slot, '') is None:
                self.minions[right_diagonal_adjacent_avaialable_slot] = minion
                minion.position = right_diagonal_adjacent_avaialable_slot
                summoned_minions.append((right_diagonal_adjacent_avaialable_slot, minion))
                continue

            #Left diagonal adjacent
            left_adjacenties = {v: k for k, v in reversed(list(right_adjacenties.items()))}
            left_diagonal_adjacent_avaialable_slot = left_adjacenties.get(slot)
            # print(f'Left Diagonal Row Adjacent {left_diagonal_adjacent_avaialable_slot}')
            if self.minions.get(left_diagonal_adjacent_avaialable_slot, '') is None:
                self.minions[left_diagonal_adjacent_avaialable_slot] = minion
                minion.position = left_diagonal_adjacent_avaialable_slot
                summoned_minions.append((left_diagonal_adjacent_avaialable_slot, minion))
                continue

            any_available_slot = next((i for i, m in self.minions.items() if m is None), None)
            if any_available_slot:
                self.minions[any_available_slot] = minion
                minion.position = any_available_slot
                summoned_minions.append((any_available_slot, minion))
                continue


        # TODO Summong Portal

        # for (i, m) in summoned_minions:
        #     print(f'Summoned {m} in {i} slot')

        return summoned_minions