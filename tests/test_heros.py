import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Keyword, Tribe
from tests import make_character, make_player


def test_charon():
    player = make_player(
        characters=[make_character(id='TEST', position=1)],
        hero='SBB_HERO_CHARON'
    )
    enemy = make_player(
        characters=[make_character(id='TEST', position=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    dead = player.graveyard[0]
    assert dead
    assert dead.attack == 3 and dead.health + dead._damage == 2


def test_evella():
    player = make_player(
        characters=[
            make_character(id='ANIMAL', position=1, tribes=['animal']),
            make_character(id='EVIL', position=5, tribes=['evil'])
        ],
        hero='SBB_HERO_DARKONE'
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    buffed_animal = player.characters.get(5)

    assert buffed_animal
    assert buffed_animal.attack == 2 and buffed_animal.health == 1


def test_sad_dracula():
    player = make_player(
        characters=[
            make_character(id='GENERIC', position=1),
            make_character(id='SBB_CHARACTER_SHADOWASSASSIN', position=5)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
        hero='SBB_HERO_DRACULA'
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    shadow_assassin = player.characters.get(5)

    assert shadow_assassin
    assert shadow_assassin.attack == 2 and shadow_assassin.health == 2


def test_fate():
    player = make_player(
        characters=[
            make_character(id='GENERIC', position=1, golden=True),
        ],
        hero='SBB_HERO_FATE'
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    generic = player.characters.get(1)

    assert generic
    assert generic.attack == 6 and generic.health == 5


def test_gepetto():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
        ],
        hero='SBB_HERO_GEPETTO',
        level=3
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    cat = player.characters.get(1)

    assert cat
    assert cat.attack == 4 and cat.health == 4


def test_krampus():
    player = make_player(
        characters=[
            make_character(id='EVIL', position=1, tribes=['evil']),
        ],
        hero='SBB_HERO_KRAMPUS',
        level=3
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    evil = player.characters.get(1)

    assert evil
    assert evil.attack == 2 and evil.health == 1


def test_mrsclaus():
    player = make_player(
        characters=[
            make_character(id='GOOD', position=1, tribes=['good']),
        ],
        hero='SBB_HERO_MRSCLAUS',
        level=3
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    good = player.characters.get(1)

    assert good
    assert good.attack == 2 and good.health == 1


def test_merlin():
    player = make_player(
        characters=[
            make_character(id='GENERIC', position=1, keywords=[kw.value for kw in Keyword], tribes=[tribe.value for tribe in Tribe])
        ],
        hero='SBB_HERO_MERLIN',
        spells=[
            'SBB_SPELL_EARTHQUAKE'
        ]
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    generic = player.characters.get(1)

    assert generic
    assert generic.attack == 3 and generic.health == 2


def test_jacks_giant():
    player = make_player(
        characters=[
            make_character(id='GENERIC', position=1)
        ],
        hero='SBB_HERO_SIRPIPS-A-LOT',
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    generic = player.characters.get(1)

    assert generic
    assert generic.health == 2


def test_mirhi():
    player = make_player(
        characters=[
            make_character(id='ROYAL', position=1, tribes=['prince', 'princess'])
        ],
        hero='SBB_HERO_KINGLION',
        mirhi_buff=5
    )

    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    royal = player.characters.get(1)

    assert royal
    assert royal.attack == 6 and royal.health == 10


def test_trophy_hunter():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT')
        ],
        hero='SBB_HERO_MILITARYLEADER',
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )

    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    assert player.characters[1].id == 'Cat'
    assert player.characters[2].id == 'Cat'

def test_trophy_hunter():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT')
        ],
        hero='SBB_HERO_MILITARYLEADER',
        treasures=['''SBB_TREASURE_CLOAKOFTHEASSASSIN''']
    )

    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    assert (player.characters[1].attack, player.characters[1].health) == (4, 4)


def test_modred():
    player = make_player(
        characters=[
            make_character()
        ],
        hero='SBB_HERO_MORDRED',
        hand=[make_character(id=f'TEST{i}', attack=i) for i in range(4)]
    )

    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    assert player.characters[1].id == 'TEST3'


def test_beauty():
    player = make_player(
        characters=[
            make_character(position=1, tribes=['good']),
            make_character(position=2, tribes=['evil'])
        ],
        hero='SBB_HERO_PRINCESSBELLE',
        hand=[make_character(id=f'TEST{i}', attack=i) for i in range(4)]
    )

    enemy = make_player()

    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    assert Tribe.EVIL in player.characters[1].tribes
    assert Tribe.GOOD in player.characters[2].tribes


FALLEN_ANGEL_TESTS = (
    (['good'], 1, 3),
    (['evil'], 3, 1),
    (['good', 'evil'], 3, 3)
)

@pytest.mark.parametrize('tribes, attack, health', FALLEN_ANGEL_TESTS)
def test_fallen_angel(tribes, attack, health):
    player = make_player(
        characters=[make_character(position=i, tribes=tribes) for i in range(1, 4)],
        hero='SBB_HERO_FALLENANGEL',
    )

    enemy = make_player()

    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    for char in player.characters.values():
        if char:
            assert char.health == health
            assert char.attack == attack


def test_muerte():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT')
        ],
        hero='SBB_HERO_MUERTE',
    )

    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    assert player.characters[1].id == 'Cat'
    assert player.characters[2].id == 'Cat'
