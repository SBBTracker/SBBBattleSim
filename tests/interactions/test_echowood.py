import pytest

from sbbbattlesim import fight
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDamagedAndSurvived, OnSummon
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


def test_echowood_queenofhearts():
    player = make_player(
        raw=True,
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
        raw=True,
        characters=[
            make_character(health=2)
        ],
    )
    fight(player, enemy, limit=2)

    golden_final_stats = (9, 9)

    final_stats = (5, 5)

    assert (player.characters[5].attack, player.characters[5].health) == final_stats
    assert (player.characters[7].attack, player.characters[7].health) == golden_final_stats


def test_echowood_supported_token():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT", position=2, attack=1, health=4, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=0, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(attack=10, health=2)
        ],
    )
    fight(player, enemy, limit=2)

    assert (player.characters[7].attack, player.characters[7].health) == (1, 4)


def test_bearstain_echowood():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_PROSPERO', position=5),
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=500, health=500)],
    )
    fight(player, enemy, limit=1)

    assert player.characters[7].attack, player.characters[7].health == (6, 6)


def test_echowood_evil_queen():
    player = make_player(
        raw=True,
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT", position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_QUEENOFHEARTS", position=6, attack=1, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(health=3)
        ],
    )
    fight(player, enemy, limit=2)

    assert (player.characters[7].attack, player.characters[7].health) == (5, 5)


@pytest.mark.parametrize('r', range(30))
def test_echowood_pumpkin(r):
    player = make_player(
        raw=True,
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
        raw=True,
        characters=[
            make_character(health=3)
        ],
    )
    fight(player, enemy, limit=1)


    assert (player.characters[7].attack, player.characters[7].health) == (2, 2) if player.characters[2].id != 'SBB_CHARACTER_BURNINGTREE' else (2, 3)


def test_echowood_pumpkin_support():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_PUMPKINKING", position=2, attack=1, health=4, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=0, health=3)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(attack=int(1e100), health=3)
        ],
    )
    fight(player, enemy, limit=1)

    assert (player.characters[7].attack, player.characters[7].health) == (1, 4)


def test_echowood_romeo():
    player = make_player(
        raw=True,
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
        raw=True,
        characters=[make_character(attack=7, health=8)],
    )
    juliet = player.characters[2]
    fight(player, enemy, limit=2)

    assert (player.characters[7].attack, player.characters[7].health) == (8, 8)


@pytest.mark.parametrize('survives', (True, False))
@pytest.mark.parametrize('phoenix_feather', (True, False))
def test_echowood_slay_vainpire(survives, phoenix_feather):
    player = make_player(
        raw=True,
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
        raw=True,
        characters=[make_character(attack=0 if survives else 5, health=5)],
    )
    juliet = player.characters[2]
    fight(player, enemy, limit=2)

    assert (player.characters[7].attack, player.characters[7].health) == ((2, 2) if (survives or phoenix_feather) else (1, 1))


@pytest.mark.parametrize('last_treasure', ("SBB_TREASURE_REDUPLICATOR", "SBB_TREASURE_TREASURECHEST", ''))
def test_echowood_phoenix_singingswords(last_treasure):
    player = make_player(
        raw=True,
        characters=[
            make_character(position=2, attack=6, health=6),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=2, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
            "SBB_TREASURE_PHOENIXFEATHER",
            last_treasure
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=6, health=6)],
    )
    fight(player, enemy, limit=1)

    echowood = player.characters[7]
    assert echowood
    assert echowood.health == 1
    if last_treasure == 'SBB_TREASURE_REDUPLICATOR':
        assert echowood.attack == 2, [i.pretty_print() for i in player.valid_characters()]
    elif last_treasure == "SBB_TREASURE_TREASURECHEST":
        assert echowood.attack == 2
    else:
        assert echowood.attack == 2


@pytest.mark.parametrize('survives', (True, False))
def test_echowood_slay_lancelot(survives):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_LANCELOT', position=2, attack=5, health=5),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=0 if survives else 5, health=5)],
    )
    juliet = player.characters[2]
    fight(player, enemy, limit=2)

    assert (player.characters[7].attack, player.characters[7].health) == ((3, 3) if survives else (1, 1))


def test_echowood_romeo_juliet():
    player = make_player(
        raw=True,
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
        raw=True,
        characters=[make_character(attack=1, health=5)],
    )
    juliet = player.characters[2]
    fight(player, enemy, limit=2)

    assert (player.characters[7].attack, player.characters[7].health) == (8, 8)


def test_multiple_echowoods_with_summon():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=3, attack=2, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=4, attack=2, health=1),
            make_character(position=1, attack=2, health=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=5, attack=1, health=1),
        ]
    )

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):
        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(self.manager.position, [summon])

    player.characters[1].register(FakeTrojanDonkeySummon)

    fight(player, enemy, limit=1)

    assert (player.characters[3].attack, player.characters[3].health) == (4, 1)
    assert (player.characters[4].attack, player.characters[4].health) == (4, 1)
    assert (player.characters[2].attack, player.characters[2].health) == (2, 1)


def test_multiple_echowoods_with_summon():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SPAWN_TEST', position=1, spawn_char=character_registry['SBB_CHARACTER_ECHOWOODSHAMBLER'], spawn_pos=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=3, attack=2, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=4, attack=2, health=1),
        ],
    )
    enemy = make_player(raw=True)

    fight(player, enemy, limit=1)

    assert (player.characters[3].attack, player.characters[3].health) == (2, 1)
    assert (player.characters[4].attack, player.characters[4].health) == (2, 1)
    assert (player.characters[2].attack, player.characters[2].health) == (1, 1)


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
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=5, attack=1, health=1),
        ]
    )

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):
        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(self.manager.position, [summon])

    player.characters[1].register(FakeTrojanDonkeySummon)

    fight(player, enemy, limit=1)

    assert (player.characters[3].attack, player.characters[3].health) == (4, 4)
    assert (player.characters[4].attack, player.characters[4].health) == (4, 4)
    assert (player.characters[2].attack, player.characters[2].health) == (2, 4)


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
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=5, attack=1, health=1),
        ]
    )

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):
        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(self.manager.position, [summon])

    player.characters[1].register(FakeTrojanDonkeySummon)

    fight(player, enemy, limit=1)

    assert (player.characters[3].attack, player.characters[3].health) == (2, 4)
    assert (player.characters[4].attack, player.characters[4].health) == (2, 4)
    assert (player.characters[2].attack, player.characters[2].health) == (1, 4)


def test_multiple_echowoods_with_summon_and_health_support_not_raw():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=3, attack=2, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=4, attack=2, health=1),
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=2, health=1),
            make_character(position=1, attack=2, health=4),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=5, attack=1, health=1),
        ]
    )

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):
        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(self.manager.position, [summon])

    player.characters[1].register(FakeTrojanDonkeySummon)

    fight(player, enemy, limit=1)

    assert (player.characters[3].attack, player.characters[3].health) == (2, 4)
    assert (player.characters[4].attack, player.characters[4].health) == (2, 4)
    assert (player.characters[2].attack, player.characters[2].health) == (1, 4)


def test_multiple_echowoods_with_summoningportal():
    player = make_player(
        raw=True,
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
        raw=True,
        characters=[
            make_character(position=5, attack=1, health=1),
        ]
    )

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):
        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(self.manager.position, [summon])

    player.characters[1].register(FakeTrojanDonkeySummon)

    fight(player, enemy, limit=1)

    assert (player.characters[3].attack, player.characters[3].health) == (2, 2)
    assert (player.characters[4].attack, player.characters[4].health) == (2, 2)
    assert (player.characters[2].attack, player.characters[2].health) == (2, 2)


@pytest.mark.parametrize('r', range(8))
def test_multiple_echowoods_with_summoningportal_summontwo(r):
    player = make_player(
        raw=True,
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
        raw=True,
        characters=[
            make_character(position=5, attack=1, health=1),
            make_character(position=6, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):
        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_ECHOWOODSHAMBLER"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(self.manager.position, [summon])

    player.characters[1].register(FakeTrojanDonkeySummon)
    player.characters[2].register(FakeTrojanDonkeySummon)

    fight(player, enemy, limit=2)

    assert (player.characters[3].attack, player.characters[3].health) == (4, 4)
    assert (player.characters[4].attack, player.characters[4].health) == (3, 3)
    assert (player.characters[6].attack, player.characters[6].health) == (4, 4)
    assert (player.characters[7].attack, player.characters[7].health) == (4, 4)


@pytest.mark.parametrize('r', range(8))
def test_multiple_echowoods_with_summoningportal_summontwo_nonechowood(r):
    player = make_player(
        raw=True,
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
        raw=True,
        characters=[
            make_character(position=5, attack=1, health=1),
            make_character(position=6, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):
        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_BLACKCAT"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False,
            )
            self.manager.player.summon(self.manager.position, [summon])

    player.characters[1].register(FakeTrojanDonkeySummon)
    player.characters[2].register(FakeTrojanDonkeySummon)

    fight(player, enemy, limit=2)

    assert (player.characters[3].attack, player.characters[3].health) == (2, 2)
    assert (player.characters[4].attack, player.characters[4].health) == (3, 3)
    assert (player.characters[6].attack, player.characters[6].health) == (4, 4)
    assert (player.characters[7].attack, player.characters[7].health) == (4, 4)


@pytest.mark.parametrize('r', range(8))
def test_multiple_echowoods_with_summoningportal_summontwo_nonechowood_onspawn(r):
    player = make_player(
        raw=True,
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
        raw=True,
        characters=[
            make_character(position=5, attack=1, health=1),
            make_character(position=6, attack=1, health=1),
        ],
    )

    class FakeTrojanDonkeySummon(OnDamagedAndSurvived):
        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_BLACKCAT"].new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False,
            )
            self.manager.player.summon(self.manager.position, [summon])

    class FakeTrojanDonkeyOnSummonSummon(OnSummon):
        donkey = player.characters[1]
        triggered = False

        def handle(self, *args, **kwargs):
            if not self.triggered:
                self.triggered = True
                summon = character_registry["SBB_CHARACTER_BLACKCAT"].new(
                    player=self.manager,
                    position=self.donkey.position,
                    golden=False,
                )
                self.manager.summon(self.donkey.position, [summon])

    player.characters[1].register(FakeTrojanDonkeySummon)
    player.register(FakeTrojanDonkeyOnSummonSummon)

    fight(player, enemy, limit=1)

    assert (player.characters[3].attack, player.characters[3].health) == (3, 3)
    assert (player.characters[4].attack, player.characters[4].health) == (2, 2)
    assert (player.characters[6].attack, player.characters[6].health) == (4, 4)
    assert (player.characters[7].attack, player.characters[7].health) == (4, 4)


def test_medusa_echowood():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_MEDUSA', position=6, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(attack=4, health=4, position=2),
            make_character(id="SBB_CHARACTER_BABYROOT", attack=0, health=1, position=5),
            make_character(id="SBB_CHARACTER_MADMADAMMIM", attack=0, health=1, position=6),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", attack=1, health=1, position=7),
        ],
    )
    creature = enemy.characters[1]
    fight(player, enemy, limit=1)
    echo = enemy.characters[7]

    assert (echo.attack, echo.health) == (4, 4)
