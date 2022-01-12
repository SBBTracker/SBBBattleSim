from sbbbattlesim import Board
from tests import make_character, make_player


def test_soltak():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_SOLTAKANCIENT", position=2, attack=0, health=20),
            make_character(position=5, attack=1, health=1),
        ]
    )
    enemy = make_player(
        characters=[make_character(id="SBB_CHARACTER_BABYDRAGON", attack=1, health=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    assert board.p1.characters[5] is not None
    assert board.p2.characters[1] is None


def test_doombreath():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_DOOMBREATH')
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_SOLTAKANCIENT", position=2, attack=0),
            make_character(position=5),
            make_character(position=6),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)

    player = board.p2

    assert player.characters[2] is None, player.characters[2].dead

    for i in (5, 6):
        assert player.characters[i] is not None, f'{[i.pretty_print() for i in player.valid_characters()]}'


def test_soltak_stops_defending():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_SOLTAKANCIENT", position=2, attack=0, health=20),
            make_character(id="SBB_CHARACTER_TIM", position=5, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(attack=100, health=100)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()


    assert winner.id == 'ENEMY'
