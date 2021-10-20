import time
import traceback

from board import Board
from player import Player
from combat import setup
from characters import registry as character_registry


if __name__ == '__main__':

    character_registry.autoregister()

    start = time.time()

    sim_num = 10000
    endings = []
    for _ in range(sim_num):
        try:
            player_one = Player(
                characters={
                    2: character_registry['baby_dragon'](3, 2),
                    3: character_registry['gruff_billy_goat'](2, 3),
                    4: character_registry['sherwood_sureshot'](2, 1),
                    1: character_registry['vain_pire'](3, 3),
                    5: character_registry['baby_root'](0, 3),
                },
                treasures=[],
                hero=None,
                hand=[]
            )

            player_two = Player(
                characters={
                    1: character_registry['black_cat'](1, 1),
                    2: character_registry['princess_peep'](1, 1),
                    3: character_registry['princess_peep'](1, 1),
                    4: character_registry['princess_peep'](1, 1),
                    5: character_registry['mad_mim'](0, 3),
                    # 5: character_registry['mad_mim']
                },
                treasures=[],
                hero=None,
                hand=[]
            )

            board = Board(player_one=player_one, player_two=player_two)
            endings.append(setup(board=board))
        except:
            traceback.print_exc()

    player_one_win_percent = (endings.count(1)/sim_num) * 100
    player_two_win_percent = (endings.count(2)/sim_num) * 100
    ties = 100 - player_two_win_percent - player_one_win_percent

    print(f'Outcomes'
          f'\n\tPlayer One Win Percent {player_one_win_percent}'
          f'\n\tPlayer Two Win Percent {player_two_win_percent}'
          f'\n\tTies {ties}')

    print(f'Runtime {time.time() - start}')