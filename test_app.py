import logging
import os
import threading
from queue import Queue

import numpy as numpy

from sbbbattlesim import simulate_from_state
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
            k = 1000
            sim_results = simulate_from_state(state, k=k)

            logger.error(f'Simulation Results ({sim_results.run_time})')
            logger.error(f'{sim_results.starting_board.p1}')
            logger.error(f'{sim_results.starting_board.p2}')


            p1id, p2id = list(state)

            def calculate_damage(player):
                if player is None:
                    return 0

                damage = player.level
                for char in player.valid_characters():
                    damage += 3 if char.golden else 1

                return damage

            win_perc = {pid: round(((len(sim_results.results[pid]) / k) * 100), 2) for pid in (p1id, p2id, None)}

            avg_damage = {}
            for pid in (p1id, p2id, None):
                damage = [calculate_damage(board.get_player(pid)) for board in sim_results.results[pid]]
                avg_damage[pid] = (sum(damage) / len(damage)) if damage else 0

            logger.error(f'{p1id} {win_perc[p1id]}% {avg_damage[p1id]}')
            logger.error(f'{p2id} {win_perc[p2id]}% {avg_damage[p2id]}')
            logger.error(f'Tie {win_perc[None]}%')

