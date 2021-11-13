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

    player = board.p1

    generic = player.characters.get(1)

    assert generic
    assert generic.attack == 3 and generic.health == 2


def test_potion_master():
    player = make_player(
        characters=[
            make_character(id='GENERIC', position=1, keywords=[kw.value for kw in Keyword], tribes=[tribe.value for tribe in Tribe])
        ],
        hero='SBB_HERO_POTIONMASTER',
        spells=[
            'SBB_SPELL_TESTYOURMIGHT'
        ]
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()

    player = board.p1

    generic = player.characters.get(1)

    assert generic
    assert generic.attack == 4 and generic.health == 3

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

    player = board.p1

    generic = player.characters.get(1)

    assert generic
    assert generic.health == 2




