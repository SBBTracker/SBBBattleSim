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
            board = Board(deepcopy(json_data))

            # Determine Setup and Turn Order
            if board.p1.treasures.get("SBB_TREASURE_HERMES'BOOTS") and not board.p2.treasures.get('hermes_boots'):
                attacking, defending = board.p1, board.p2
            elif board.p1.treasures.get("SBB_TREASURE_HERMES'BOOTS") and not board.p2.treasures.get('hermes_boots'):
                attacking, defending = board.p1, board.p2
            else:
                attacking, defending = random.sample((board.p1, board.p2), 2)

            endings.append(fight_initialization(attacking, defending))
        except:
            traceback.print_exc()

    p1id, p2id = list(json_data)

    player_one_win_percent = round((endings.count(p1id) / k) * 100, 2)
    player_two_win_percent = round((endings.count(p2id) / k) * 100, 2)
    ties = round(100 - player_two_win_percent - player_one_win_percent, 2)

    return player_one_win_percent, player_two_win_percent, ties, time.time() - start
