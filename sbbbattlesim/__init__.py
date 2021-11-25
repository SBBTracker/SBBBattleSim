import asyncio
import collections
import hashlib
import logging
import threading
import time
import traceback
from copy import deepcopy
from dataclasses import dataclass

from sbbbattlesim.board import Board

from sbbbattlesim.config import configure_logging

from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.heros import registry as hero_registry
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.treasures import registry as treasure_registry

SUMMONING_PRIORITY = 10


logger = logging.getLogger(__name__)


def setup():
    configure_logging()
    character_registry.autoregister()
    hero_registry.autoregister()
    spell_registry.autoregister()
    treasure_registry.autoregister()


setup()


@dataclass
class SimulationResult:
    hash_id: hash
    results: dict
    run_time: float
    starting_board: Board


def simulate(data, results, k=1):
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

def simulate_from_state(state, t=1, k=1):
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

    logger.error(sim_data)
    assert isinstance(sim_data, dict)

    results = collections.defaultdict(list)
    start = time.perf_counter()
    for _ in range(t):
        simulate(sim_data, results, k)
        # threading.Thread(target=simulate, args=(sim_data, results, k), daemon=True).start()

    starting_board = Board(deepcopy(sim_data))

    return SimulationResult(
            hash_id=hashlib.sha256(f'{starting_board.p1}{starting_board.p2}'.encode('utf-8')),
            results=results,
            run_time=time.perf_counter() - start,
            starting_board=starting_board
        )


