import random
import time
import traceback
from copy import deepcopy

from sbbbattlesim.combat import fight


class Board:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        self.p1.id = True
        self.p2.id = False

    def simulate(self, k=1):
        start = time.time()

        # Determine Setup and Turn Order
        if self.p1.treasures.get('hermes_boots') and not self.p2.treasures.get('hermes_boots'):
            attacking, defending = self.p1, self.p2
            random_attacker = False
        elif self.p1.treasures.get('hermes_boots') and not self.p2.treasures.get('hermes_boots'):
            attacking, defending = self.p1, self.p2
            random_attacker = False
        else:
            attacking, defending = random.sample((self.p1, self.p2), 2)
            random_attacker = True

        print(attacking, defending)

        endings = []
        for _ in range(k):
            try:
                if random_attacker:
                    attacking, defending = defending, attacking

                endings.append(fight(deepcopy(attacking), deepcopy(defending)))
            except:
                traceback.print_exc()

        player_one_win_percent = (endings.count(True) / k) * 100
        player_two_win_percent = (endings.count(False) / k) * 100
        ties = 100 - player_two_win_percent - player_one_win_percent

        return player_one_win_percent, player_two_win_percent, ties, time.time() - start
