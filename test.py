import json
import os

from sbbbattlesim import simulate


if __name__ == '__main__':
    data = open(os.path.join(os.path.dirname(__file__), 'tests', 'sugarandspice.json')).read()
    powp, ptwp, t, rt = simulate(data, k=1)

    print(f'Outcomes'
          f'\n\tPlayer One Win Percent {powp}'
          f'\n\tPlayer Two Win Percent {ptwp}'
          f'\n\tTies {t}')

    print(f'Runtime {rt}')
