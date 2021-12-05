import asyncio
import logging
import threading
from queue import Queue

import log_parser
from sbbbattlesim import simulate

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.error(f'Starting...')
    queue = Queue()
    threading.Thread(target=log_parser.run,
                     args=(queue,),
                     daemon=True).start()

    while True:
        update = queue.get()
        job = update.job
        state = update.state
        if job == log_parser.JOB_BOARDINFO:
            simulation = asyncio.run(simulate(state, t=4, k=250, timeout=30))

            p1id, p2id = simulation.starting_board.p1.id, simulation.starting_board.p2.id

            logger.error(f'RESULT KEYS {simulation.results.keys()}')

            logger.error(f'Simulation Results ({simulation.run_time} - {sum(len(v) for v in simulation.results.values())})')
            logger.error(f'{simulation.starting_board.p1}')
            logger.error(f'{simulation.starting_board.p2}')

            logger.error(f'{p1id} {simulation.stats.win_rate[p1id]}% {simulation.stats.avg_damage[p1id]}')
            logger.error(f'{p2id} {simulation.stats.win_rate[p2id]}% {simulation.stats.avg_damage[p2id]}')
            logger.error(f'Tie {simulation.stats.win_rate[None]}%')

            exit()