from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from sbbbattlesim.events import OnDamagedAndSurvived, OnSummon
from tests import make_character, make_player
from sbbbattlesim.characters import registry as character_registry

import pytest


def test_echowood_queenofhearts():
    player = make_player(
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT", position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=5, attack=1, health=1),
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


def test_bearstain_echowood():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PROSPERO', position=5),
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert board.p1.characters[7].attack, board.p1.characters[7].health == (6, 6)


def test_echowood_evil_queen():
    player = make_player(
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT", position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_QUEENOFHEARTS", position=6, attack=1, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(health=3)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (5, 5)


def test_echowood_pumpkin():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_PUMPKINKING", position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
            "SBB_TREASURE_SUMMONINGCIRCLE"
        ]
    )
    enemy = make_player(
        characters=[
            make_character(health=3)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (2, 2)


def test_echowood_pumpkin_support():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_PUMPKINKING", position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=0, health=3)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=int(1e100), health=3)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (1, 4)


def test_echowood_romeo():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=2, attack=1, health=1),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=7, health=8)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    juliet = board.p1.characters[2]
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (8, 8)


@pytest.mark.parametrize('survives', (True, False))
@pytest.mark.parametrize('phoenix_feather', (True, False))
def test_echowood_slay_vainpire(survives, phoenix_feather):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_NIGHTSTALKER', position=2, attack=5, health=5),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
            "SBB_TREASURE_PHOENIXFEATHER" if phoenix_feather else ''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=0 if survives else 5, health=5)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    juliet = board.p1.characters[2]
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == ((2, 2) if (survives or phoenix_feather) else (1, 1))


@pytest.mark.parametrize('survives', (True, False))
def test_echowood_slay_lancelot(survives):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_LANCELOT', position=2, attack=5, health=5),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=0 if survives else 5, health=5)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    juliet = board.p1.characters[2]
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == ((3, 3) if survives else (1, 1))


def test_echowood_romeo_juliet():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=2, attack=1, health=1),
            make_character(id='SBB_CHARACTER_JULIET', attack=1, health=1, position=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=5)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    juliet = board.p1.characters[2]
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (8, 8)


def test_multiple_echowoods_with_summon():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=3, attack=2, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=4, attack=2, health=1),
            make_character(position=1, attack=2, health=2),
        ],
        treasures=[
            "SBB_TREASURE_WHIRLINGBLADES",
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=1),
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
                summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                    owner=self.manager.owner,
                    position=self.manager.position,
                    golden=False
                )
                self.manager.owner.summon(self.manager.position, [summon])

    board.p1.characters[1].register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[3].attack, board.p1.characters[3].health) == (4, 1)
    assert (board.p1.characters[4].attack, board.p1.characters[4].health) == (4, 1)
    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (2, 1)

def test_multiple_echowoods_with_summon():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=3, attack=2, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=4, attack=2, health=1),
            make_character(position=1, attack=2, health=2),
        ],
        treasures=[
            "SBB_TREASURE_WHIRLINGBLADES",
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=1),
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
                summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                    owner=self.manager.owner,
                    position=self.manager.position,
                    golden=False
                )
                self.manager.owner.summon(self.manager.position, [summon])

    board.p1.characters[1].register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[3].attack, board.p1.characters[3].health) == (4, 1)
    assert (board.p1.characters[4].attack, board.p1.characters[4].health) == (4, 1)
    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (2, 1)


def test_multiple_echowoods_with_summon_and_health_support():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=3, attack=2, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=4, attack=2, health=1),
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=1, health=1),
            make_character(position=1, attack=2, health=4),
        ],
        treasures=[
            "SBB_TREASURE_WHIRLINGBLADES",
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=1),
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
                summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                    owner=self.manager.owner,
                    position=self.manager.position,
                    golden=False
                )
                self.manager.owner.summon(self.manager.position, [summon])

    board.p1.characters[1].register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[3].attack, board.p1.characters[3].health) == (4, 4)
    assert (board.p1.characters[4].attack, board.p1.characters[4].health) == (4, 4)
    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (2, 4)


def test_multiple_echowoods_with_summon_and_health_support():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=3, attack=2, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=4, attack=2, health=1),
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=1, health=1),
            make_character(position=1, attack=2, health=4),
        ],
        treasures=[
            "SBB_TREASURE_WHIRLINGBLADES",
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=1),
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
                summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                    owner=self.manager.owner,
                    position=self.manager.position,
                    golden=False
                )
                self.manager.owner.summon(self.manager.position, [summon])

    board.p1.characters[1].register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[3].attack, board.p1.characters[3].health) == (4, 4)
    assert (board.p1.characters[4].attack, board.p1.characters[4].health) == (4, 4)
    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (2, 4)


def test_multiple_echowoods_with_summon_and_health_support_not_raw():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=3, attack=1, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=4, attack=1, health=1),
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=1, health=1),
            make_character(position=1, attack=2, health=4),
        ],
        treasures=[
            "SBB_TREASURE_WHIRLINGBLADES",
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=1),
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
                summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                    owner=self.manager.owner,
                    position=self.manager.position,
                    golden=False
                )
                self.manager.owner.summon(self.manager.position, [summon])

    board.p1.characters[1].register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[3].attack, board.p1.characters[3].health) == (4, 4)
    assert (board.p1.characters[4].attack, board.p1.characters[4].health) == (4, 4)
    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (2, 4)


def test_multiple_echowoods_with_summoningportal():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=3, attack=1, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=4, attack=1, health=1),
            make_character(position=1, attack=2, health=4),
        ],
        treasures=[
            "SBB_TREASURE_SUMMONINGCIRCLE",
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=1),
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
                summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                    owner=self.manager.owner,
                    position=self.manager.position,
                    golden=False
                )
                self.manager.owner.summon(self.manager.position, [summon])

    board.p1.characters[1].register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[3].attack, board.p1.characters[3].health) == (2, 2)
    assert (board.p1.characters[4].attack, board.p1.characters[4].health) == (2, 2)
    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (2, 2)


@pytest.mark.parametrize('r', range(8))
def test_multiple_echowoods_with_summoningportal_summontwo(r):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=6, attack=1, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
            make_character(position=1, attack=2, health=4),
            make_character(position=2, attack=2, health=4),
            make_character(position=5, attack=2, health=4),
        ],
        treasures=[
            "SBB_TREASURE_SUMMONINGCIRCLE",
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=1),
            make_character(position=6, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
                summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                    owner=self.manager.owner,
                    position=self.manager.position,
                    golden=False
                )
                self.manager.owner.summon(self.manager.position, [summon])

    board.p1.characters[1].register(FakeTrojanDonkeySummon)
    board.p1.characters[2].register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[3].attack, board.p1.characters[3].health) == (4, 4)
    assert (board.p1.characters[4].attack, board.p1.characters[4].health) == (3, 3)
    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == (4, 4)
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (4, 4)


@pytest.mark.parametrize('r', range(8))
def test_multiple_echowoods_with_summoningportal_summontwo_nonechowood(r):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=6, attack=1, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
            make_character(position=1, attack=2, health=4),
            make_character(position=2, attack=2, health=4),
            make_character(position=5, attack=2, health=4),
        ],
        treasures=[
            "SBB_TREASURE_SUMMONINGCIRCLE",
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=1),
            make_character(position=6, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
                summon = character_registry["SBB_CHARACTER_BLACKCAT"].new(
                    owner=self.manager.owner,
                    position=self.manager.position,
                    golden=False,
                )
                self.manager.owner.summon(self.manager.position, [summon])

    board.p1.characters[1].register(FakeTrojanDonkeySummon)
    board.p1.characters[2].register(FakeTrojanDonkeySummon)

    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[3].attack, board.p1.characters[3].health) == (2, 2)
    assert (board.p1.characters[4].attack, board.p1.characters[4].health) == (3, 3)
    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == (4, 4)
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (4, 4)


@pytest.mark.parametrize('r', range(8))
def test_multiple_echowoods_with_summoningportal_summontwo_nonechowood_onspawn(r):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=6, attack=1, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
            make_character(position=1, attack=2, health=4),
            make_character(position=2, attack=2, health=4),
            make_character(position=5, attack=2, health=4),
        ],
        treasures=[
            "SBB_TREASURE_SUMMONINGCIRCLE",
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=1),
            make_character(position=6, attack=1, health=1),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
                summon = character_registry["SBB_CHARACTER_BLACKCAT"].new(
                    owner=self.manager.owner,
                    position=self.manager.position,
                    golden=False,
                )
                self.manager.owner.summon(self.manager.position, [summon])

    class FakeTrojanDonkeyOnSummonSummon(OnSummon):
        donkey = board.p1.characters[1]
        triggered = False

        def handle(self, *args, **kwargs):
                if not self.triggered:
                    self.triggered=True
                    summon = character_registry["SBB_CHARACTER_BLACKCAT"].new(
                        owner=self.manager,
                        position=self.donkey.position,
                        golden=False,
                    )
                    self.manager.summon(self.donkey.position, [summon])

    board.p1.characters[1].register(FakeTrojanDonkeySummon)
    board.p1.register(FakeTrojanDonkeyOnSummonSummon)

    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[3].attack, board.p1.characters[3].health) == (2, 2)
    assert (board.p1.characters[4].attack, board.p1.characters[4].health) == (3, 3)
    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == (4, 4)
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (4, 4)



def test_medusa_echowood():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_MEDUSA', position=6, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1, position=2),
            make_character(id="SBB_CHARACTER_BABYROOT", attack=0, health=1, position=5),
            make_character(id="SBB_CHARACTER_MADMADAMMIM", attack=0, health=1, position=6),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", attack=1, health=1, position=7),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    creature = board.p2.characters[1]
    winner, loser = board.fight(limit=1)
    echo = board.p2.characters[7]

    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (echo.attack, echo.health) == (4, 4)


