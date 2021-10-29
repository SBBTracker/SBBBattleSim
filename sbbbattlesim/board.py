import random
import time
import traceback
from copy import deepcopy
from sbbbattlesim.player import Player
from sbbbattlesim.combat import fight
import logging

logger = logging.getLogger(__name__)

class Board:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    @classmethod
    def from_json(cls, data):
        assert isinstance(data, dict)
        p1id, p2id = list(data)
        p1data, p2data = data[p1id], data[p2id]

        def get_player(pdat):
            return Player(
                characters=pdat['characters'],
                treasures=pdat['treasures'],
                hero=pdat['hero'],
                hand=pdat['hand']
            )

        p1, p2 = get_player(p1data), get_player(p2data)
        p1.id, p2.id = p1id, p2id
        p1.opponent = p2
        p2.opponent = p1

        return cls(p1=p1, p2=p2)

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

        endings = []
        for _ in range(k):
            try:
                if random_attacker:
                    attacking, defending = defending, attacking

                _attacking = deepcopy(attacking)
                _defending = deepcopy(defending)
                _attacking.opponent = _defending
                _defending.opponent = _attacking
                endings.append(fight(_attacking, _defending))
            except:
                traceback.print_exc()

        player_one_win_percent = (endings.count(True) / k) * 100
        player_two_win_percent = (endings.count(False) / k) * 100
        ties = 100 - player_two_win_percent - player_one_win_percent

        return player_one_win_percent, player_two_win_percent, ties, time.time() - start
