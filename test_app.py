import asyncio
import json
import logging
import threading
from queue import Queue

import log_parser
from sbbbattlesim import simulate, SBBBSCrocException

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.debug(f'Starting...')
    queue = Queue()
    threading.Thread(target=log_parser.run,
                     args=(queue,),
                     daemon=True).start()

    while True:
        update = queue.get()
        job = update.job
        state = update.state
        if job == log_parser.JOB_BOARDINFO:
            try:
                simulation = simulate(state, t=4, k=250, timeout=30)
            except SBBBSCrocException:
                exit()

            p1id, p2id = simulation.starting_board.p1.id, simulation.starting_board.p2.id

            logger.debug(f'RESULT KEYS {simulation.results.keys()}')

            logger.debug(
                f'Simulation Results ({simulation.run_time} - {sum(len(v) for v in simulation.results.values())})')
            logger.debug(f'{simulation.starting_board.p1}')
            logger.debug(f'{simulation.starting_board.p2}')

            logger.debug(f'{p1id} {simulation.stats.win_rate[p1id]}% {simulation.stats.avg_damage[p1id]}')
            logger.debug(f'{p2id} {simulation.stats.win_rate[p2id]}% {simulation.stats.avg_damage[p2id]}')
            logger.debug(f'Tie {simulation.stats.win_rate[None]}%')
