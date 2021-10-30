import json
import os

from sbbbattlesim import Board


if __name__ == '__main__':
    board = Board.from_json(json.loads(open(os.path.join(os.path.dirname(__file__), 'tests', 'echowood.json')).read()))
    powp, ptwp, t, rt = board.simulate(k=1)

    print(f'Outcomes'
          f'\n\tPlayer One Win Percent {powp}'
          f'\n\tPlayer Two Win Percent {ptwp}'
          f'\n\tTies {t}')

    print(f'Runtime {rt}')
