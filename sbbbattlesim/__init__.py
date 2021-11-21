import collections
import hashlib
import logging
import time
import traceback
from copy import deepcopy
from dataclasses import dataclass

from sbbbattlesim.board import Board

from sbbbattlesim.config import configure_logging

SUMMONING_PRIORITY = 10

configure_logging()

logger = logging.getLogger(__name__)


@dataclass
class SimulationResult:
    hash_id: hash
    results: dict
    run_time: float
    starting_board: Board


def simulate(data, k=1):
    start = time.perf_counter()

    results = collections.defaultdict(list)
    for _ in range(k):
        board = Board(deepcopy(data))
        try:
            winner, _ = board.fight()
            results[winner.id if winner else None].append(board)
        except Exception as e:
            logger.error(board.p1)
            logger.error(board.p2)
            traceback.print_exc()
            raise e

    starting_board = Board(deepcopy(data))
    return SimulationResult(
        hash_id=hashlib.sha256(f'{starting_board.p1}{starting_board.p2}'.encode('utf-8')),
        results=results,
        run_time=time.perf_counter() - start,
        starting_board=starting_board
    )

def simulate_from_state(state, k=1):
    sim_data = {}
    for player, player_data in state.items():

        characters = []
        treasures = []
        hero = None
        spells = []
        level = 0
        hand = []

        for data in player_data:
            if data.zone == 'Character':
                characters.append({
                    'id': data.content_id,
                    'attack': int(data.cardattack),
                    'health': int(data.cardhealth),
                    'golden': bool(data.is_golden),
                    'cost': int(data.cost),
                    'position': int(data.slot) + 1,  # This is done to match slot to normal board positions
                    'tribes': [subtype.lower() for subtype in data.subtypes],
                    'raw': True
                })
            elif data.zone == 'Treasure':
                treasures.append(data.content_id)
            elif data.zone == 'Hero':
                hero = data.content_id
                level = int(data.level)
            elif data.zone == 'Spell':
                spells.append(data.content_id)

        sim_data[player] = {
            'characters': characters,
            'treasures': treasures,
            'hero': hero,
            'spells': spells,
            'level': level,
            'hand': hand
        }

    return simulate(sim_data, k=k)


