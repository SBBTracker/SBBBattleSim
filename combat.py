import sys

import random
from functools import lru_cache

sys.setrecursionlimit(100)


def setup(board):
    if board.player_one.treasures.get('hermes_boots') and not board.player_two.treasures.get('hermes_boots'):
        board.turn = 1
    elif board.player_one.treasures.get('hermes_boots') and not board.player_two.treasures.get('hermes_boots'):
        board.turn = 0
    else:
        board.turn = random.getrandbits(1)

    attacking, defending = board.get_attack_defense()
    attacking.player_number = 1
    defending.player_number = 2

    return fight(board, attacking, defending)


@lru_cache(maxsize=512)
def fight(board, attacker, defender, turn=0):
    try:

        attacker.resolve_board()
        defender.resolve_board()

        # Get Attacker
        attack_minion = attacker.attack_minion
        if attack_minion is not None:

            # Get valid defending
            valid_defenders = defender.front
            if getattr(attack_minion, 'flying', False) and next((True for m in defender.back.values() if m is not None), False):
                valid_defenders = defender.back
            slot = random.choice(list({i for i, m in valid_defenders.items() if m is not None}))
            defender_minion = defender.minions[slot]

            event_kwargs = dict(board=board, attacker=attacker, defender=defender, attack_minion=attack_minion, defender_minion=defender_minion)

            attack(**event_kwargs) #Run the attack

        print(f'Board {turn}\n{board}\n')

        # Endgame Check
        winner = board.winner()
        if winner:
            return winner

        board.turn = not board.turn

        return fight(
            board=board,
            attacker=defender,
            defender=attacker,
            turn=turn+1
        )
    except Exception as e:
        print(f'ERROR STATE WITH BOARD ON TURN {turn}\n{board}')
        raise e


def attack(attack_minion, defend_minion, **event_kwargs):
    print(f'{attacker_minion} is attacking {defender_minion}')

    # TODO On Attack Trigger

    if not getattr(attack_minion, 'ranged', False):
        attack.damage(defend_minion.attack, damaged_by=defend_minion, **event_kwargs)

    defender_died = defend_minion.damage(attack_minion.attack, damaged_by=attack_minion, **event_kwargs)

    if defender_died:
        attack_minion.slay_event(**event_kwargs)
