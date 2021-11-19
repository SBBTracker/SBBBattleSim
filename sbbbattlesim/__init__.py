import collections
import json
import logging
import random
import time
import traceback
from copy import deepcopy

from sbbbattlesim.board import Board
from sbbbattlesim.combat import fight_initialization
from sbbbattlesim.config import configure_logging

SUMMONING_PRIORITY = 10

configure_logging()

logger = logging.getLogger(__name__)


def simulate(data, k=1):
    start = time.time()

    results = collections.defaultdict(list)
    for _ in range(k):
        try:
            board = Board(deepcopy(data))
            winner, _ = board.fight()
            results[winner.id if winner else None].append(board)
        except Exception as e:
            logger.error(board.p1)
            logger.error(board.p2)
            traceback.print_exc()
            raise e

    return results, time.time() - start
