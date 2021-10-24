import random

from sbbbattlesim import Player, Board, character_registry, keywords, tribes


def random_character():
    return random.choice(list(character_registry.characters.values()))(
        attack=random.randint(0, 10),
        health=random.randint(1, 20),
        golden=bool(random.getrandbits(1)),
        keywords=[random.choice(keywords) for i in range(random.randint(0, 2))],
        tribes=[random.choice(tribes) for i in range(random.randint(0, 2))]
    )


def generate_player(char_num=5, treasures=2):
    mad_mim = character_registry['SBB_CHARACTER_MADMADAMMIM']

    return Player(
        characters=[random_character() for _ in range(5)],
        treasures=[],
        hero=[],
        hand=[]
    )


if __name__ == '__main__':
    board = Board(p1=generate_player(), p2=generate_player())
    powp, ptwp, t, rt = board.simulate(k=1)

    print(f'Outcomes'
          f'\n\tPlayer One Win Percent {powp}'
          f'\n\tPlayer Two Win Percent {ptwp}'
          f'\n\tTies {t}')

    print(f'Runtime {rt}')




