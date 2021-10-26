import random
import time
import traceback
from copy import deepcopy
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.player import Player
from sbbbattlesim.combat import fight


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
            characters = {}
            for slot, char_data in pdat['characters'].items():
                char_cls = character_registry[char_data['id']]
                characters[int(slot)] = char_cls(
                    attack=char_data['attack'],
                    health=char_data['health'],
                    golden=char_data['golden'],
                    keywords=char_data['keywords'],
                    tribes=char_data['tribes'],
                )

            hand = []
            for char_data in pdat['hand']:
                char_cls = character_registry[char_data['id']]
                hand.append(char_cls(
                    attack=char_data['attack'],
                    health=char_data['health'],
                    golden=char_data['golden'],
                    keywords=char_data['keywords'],
                    tribes=char_data['tribes'],
                ))

            return Player(
                characters=characters,
                treasures=pdat['treasures'],
                hero=pdat['hero'],
                hand=hand
            )

        p1, p2 = get_player(p1data), get_player(p2data)
        p1.id, p2.id = p1id, p2id

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

                endings.append(fight(deepcopy(attacking), deepcopy(defending)))
            except:
                traceback.print_exc()

        player_one_win_percent = (endings.count(True) / k) * 100
        player_two_win_percent = (endings.count(False) / k) * 100
        ties = 100 - player_two_win_percent - player_one_win_percent

        return player_one_win_percent, player_two_win_percent, ties, time.time() - start
