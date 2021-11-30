from sbbbattlesim import Board
from tests import make_character, make_player
from sbbbattlesim.utils import Tribe

def test_echowood_queenofhearts():
    player = make_player(
        hero = "SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT",position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER",position=5, attack=1, health=1),
            make_character(id="SBB_CHARACTER_QUEENOFHEARTS", position=6, attack=1, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1, golden=True),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(health=2)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    golden_final_stats = (9, 9)

    final_stats = (5, 5)

    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == final_stats
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == golden_final_stats


def test_echowood_supported_token():
    player = make_player(
        # hero = "SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT", position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=0, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(attack=10, health=2)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (1, 4)

# TODO test echowood with storm king, puff puff, and crafty emerging from some spawning mechanic