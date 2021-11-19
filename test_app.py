import logging
import os
import threading
from queue import Queue

import numpy as numpy

from sbbbattlesim import Board, simulate
import log_parser

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    queue = Queue()
    threading.Thread(target=log_parser.run,
                     args=(queue,),
                     daemon=True).start()

    while True:
        update = queue.get()
        job = update.job
        state = update.state
        if job == log_parser.JOB_BOARDINFO:
            sim_data = {}
            for player, player_data in state.items():

                characters = []
                treasures = []
                hero = None
                spells = []
                level = 0
                
                for data in player_data:
                    if data.zone == 'Character':
                        characters.append({
                            'id': data.content_id,
                            'attack': int(data.cardattack),
                            'health': int(data.cardhealth),
                            'golden': data.is_golden,
                            'cost': int(data.cost),
                            'position': int(data.slot) + 1,  # This is done to match slot to normal board positions
                            'tribes': []
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
                    'level': level
                }

            k = 1000
            results, run_time = simulate(sim_data, k=k)
            logger.error(f'\t\tSimulation Results\t({run_time})')

            p1id, p2id = list(state)

            def calculate_damage(player):
                if player is None:
                    return 0

                damage = player.level
                for char in player.valid_characters():
                    damage += 3 if char.golden else 1

                return damage

            avg_damage = {pid: [calculate_damage(board.get_player(pid)) for board in results[pid]] for pid in (p1id, p2id, None)}
            win_perc = {pid: ((len(results[pid]) / k) * 100) for pid in (p1id, p2id, None)}

            logger.error(f'{p1id} {win_perc[p1id]}% {(sum(avg_damage[p1id])/len(avg_damage[p1id])) if avg_damage[p1id] else 0}')
            logger.error(f'{p2id} {win_perc[p2id]}% {(sum(avg_damage[p2id])/len(avg_damage[p2id])) if avg_damage[p2id] else 0}')
            logger.error(f'Tie {win_perc[None]}%')

