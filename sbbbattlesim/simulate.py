import collections
import concurrent.futures
import hashlib
import logging
import multiprocessing
import time
import traceback
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List
import json

from sbbbattlesim import fight
from sbbbattlesim.player import Player
from sbbbattlesim.stats import calculate_stats, CombatStats

logger = logging.getLogger(__name__)


def from_state(state: dict):
    sim_data = {}
    for player, player_data in state.items():

        characters = []
        treasures = []
        hero = None
        spells = []
        level = 0
        hand = []
        counter = 0

        for data in player_data:
            if data.zone == 'Character':
                content_id = data.content_id.replace('GOLDEN_', '')

                characters.append({
                    'id': content_id,
                    'attack': int(data.cardattack),
                    'health': int(data.cardhealth),
                    'golden': data.is_golden if isinstance(data.is_golden, bool) else data.is_golden.lower() == "true",
                    'cost': int(data.cost),
                    'position': int(data.slot) + 1,  # This is done to match slot to normal board positions
                    'tribes': [subtype.lower() for subtype in data.subtypes],
                })
            elif data.zone == 'Treasure':
                treasures.append(data.content_id)
            elif data.zone == 'Hero':
                hero = data.content_id
                counter = data.counter
                level = int(data.level) if hasattr(data, "level") else 0
            elif data.zone == 'Spell':
                spells.append(data.content_id)
            elif data.zone == 'Hand':
                content_id = data.content_id.replace('GOLDEN_', '')
                hand.append({
                    'id': content_id,
                    'attack': int(data.cardattack),
                    'health': int(data.cardhealth),
                    'golden': data.is_golden if isinstance(data.is_golden, bool) else data.is_golden.lower() == "true",
                    'cost': int(data.cost),
                    'position': int(data.slot) + 1,  # This is done to match slot to normal board positions
                    'tribes': [subtype.lower() for subtype in data.subtypes],
                })
            elif data.zone == 'None' and 'SBB_SPELL' in data.content_id:
                spells.append(data.content_id)

        sim_data[player] = {
            'characters': characters,
            'treasures': treasures,
            'hero': hero,
            'spells': spells,
            'level': level,
            'hand': hand
        }
        if hero == "SBB_HERO_KINGLION":
            sim_data[player]['mihri_buff'] = int(counter)

    assert isinstance(sim_data, dict)

    logger.info(json.dumps(sim_data))

    return sim_data


def simulate_brawl(data: dict, k: int) -> List[CombatStats]:
    logger.debug(f'Simulation Process Starting (k={k})')
    return [fight(*(Player(id=i, **d) for i, d in deepcopy(data).items()), limit=1) for _ in range(k)]


def _process(data: dict, t: int = 1, k: int = 1, timeout: int = 30) -> list:
    raw = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=t) as executor:
        futures = [executor.submit(simulate_brawl, data, k) for _ in range(t)]
        for future in concurrent.futures.as_completed(futures, timeout=timeout):
            raw.extend(future.result())

    return raw


@dataclass
class SimulationStats:
    _id: hash
    run_time: float
    # starting_board: Board
    results: List[CombatStats]
    raw: dict


def simulate(state: dict, t: int = 1, k: int = 1, timeout: int = 30) -> SimulationStats:
    data = from_state(state)
    start = time.perf_counter()
    results = _process(data, t, k, timeout)
    return SimulationStats(
        run_time=time.perf_counter() - start,
        results=results,
        raw=data
    )
