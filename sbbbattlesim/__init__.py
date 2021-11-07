import json
import random
import time
import traceback
from copy import deepcopy

from sbbbattlesim.board import Board
from sbbbattlesim.combat import fight_initialization
from sbbbattlesim.config import configure_logging

SUMMONING_PRIORITY = 10

configure_logging()


def simulate(data, k=1):

    json_data = json.loads(data)

    start = time.time()

    endings = []
    for _ in range(k):
        try:
            winner, _ = Board(deepcopy(json_data)).fight()
            endings.append(winner)
        except:
            traceback.print_exc()

    p1id, p2id = list(json_data)

    player_one_win_percent = round((endings.count(p1id) / k) * 100, 2)
    player_two_win_percent = round((endings.count(p2id) / k) * 100, 2)
    ties = round(100 - player_two_win_percent - player_one_win_percent, 2)

    return player_one_win_percent, player_two_win_percent, ties, time.time() - start
