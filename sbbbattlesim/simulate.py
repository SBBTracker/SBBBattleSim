import collections
import hashlib
import logging
import multiprocessing
import time
import traceback
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List

from sbbbattlesim import Board
from sbbbattlesim.stats import SimulationStats, calculate_stats

logger = logging.getLogger(__name__)


@dataclass
class SimulationResult:
    hash_id: hash
    results: Dict[str, List[Board]]
    run_time: float
    starting_board: Board
    stats: SimulationStats


def from_state(state: dict):
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
                content_id = data.content_id.replace('GOLDEN_', '')

                characters.append({
                    'id': content_id,
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

    assert isinstance(sim_data, dict)

    return sim_data


def simulate_brawl(data: dict, k: int, raw: dict):
    logger.error(f'Simulation Starting (k={k})')
    for _ in range(k):
        board = Board(deepcopy(data))
        try:
            board.fight(limit=-1)
            raw.append(board)
        except Exception as e:
            traceback.print_exc()
            raise e


def simulate(state: dict, t: int = 1, k: int = 1, timeout: int = 30) -> SimulationResult:
    data = from_state(state)

    start = time.perf_counter()

    starting_board = Board(deepcopy(data))

    manager = multiprocessing.Manager()
    raw = manager.list()

    jobs = []
    for i in range(t):
        p = multiprocessing.Process(target=simulate_brawl, args=(data, k, raw))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()

    # with multiprocessing.Pool(processes=t) as pool:
    #     pool.map(simulate_brawl, args=((data, k, results) for _ in range(t)))

    results = collections.defaultdict(list)
    for board in raw:
        results[board.winner.id if board.winner else None].append(board)

    sim_results = SimulationResult(
        hash_id=hashlib.sha256(f'{starting_board.p1}{starting_board.p2}'.encode('utf-8')),
        results=results,
        run_time=time.perf_counter() - start,
        starting_board=starting_board,
        stats=calculate_stats(results)
    )

    return sim_results
