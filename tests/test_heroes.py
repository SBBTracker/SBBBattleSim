import logging

import pytest

from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnStart, EventManager
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player

logger = logging.getLogger(__name__)


@pytest.mark.parametrize('is_real', (True, False))
def test_charon(is_real):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='TEST', position=1),
            make_character(id='''SBB_CHARACTER_WIZARD'SFAMILIAR''' if is_real else '', position=5)
        ],
        hero='SBB_HERO_CHARON'
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(id='TEST', position=1),
            make_character(position=5)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy)



    dead = player.graveyard[0]
    assert dead
    assert dead.attack == 1 and dead.health + dead._damage == 1

    also_dead = player.graveyard[1]
    assert also_dead
    assert also_dead.attack == (3 if is_real else 1) and also_dead.health + dead._damage == (2 if is_real else 1)


@pytest.mark.parametrize('on', (True, False))
@pytest.mark.parametrize('evil_back', (True, False))
def test_evella(on, evil_back):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1, tribes=['animal', 'evil'] if on else []),
            make_character(id='EVIL', position=5, tribes=['evil'] if evil_back else [])
        ],
        hero='SBB_HERO_DARKONE'
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(id='GENERIC', position=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy)



    logger.debug(player.pretty_print())

    buffed_animal = player.characters.get(5)
    buffed_cat = player.characters.get(1)

    assert buffed_animal
    assert buffed_animal.attack == (2 if on and evil_back else 1) and buffed_animal.health == 1
    assert buffed_cat
    assert buffed_cat.attack == (3 if on else 2) and buffed_cat.health == 1


def test_evella_lots():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1, tribes=['animal', 'evil']),
            make_character(id='SBB_CHARACTER_BLACKCAT', position=5, tribes=['animal', 'evil']),
        ],
        hero='SBB_HERO_DARKONE'
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(id='GENERIC', position=1, attack=3, health=5)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy)



    buffed_cat = player.characters.get(5)

    assert buffed_cat
    assert buffed_cat.attack == 5


@pytest.mark.parametrize('on', (True, False))
def test_sad_dracula(on):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='GENERIC', position=1 if on else 2),
            make_character(id='SBB_CHARACTER_SHADOWASSASSIN', position=5)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
        hero='SBB_HERO_DRACULA'
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(id='GENERIC', position=2)],
    )
    fight(player, enemy)




    shadow_assassin = player.characters.get(5)

    assert shadow_assassin
    assert shadow_assassin.attack == (2 if on else 1) and shadow_assassin.health == 1


@pytest.mark.parametrize('on', (True, False))
def test_fate(on):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='GENERIC', position=1),
        ],
        hero='SBB_HERO_FATE'
    )
    enemy = make_player(raw=True)

    class FakeTrojanDonkeySummon(OnStart):

        def handle(self, *args, **kwargs):
            summon = character_registry["SBB_CHARACTER_BLACKCAT"].new(
                player=self.source,
                position=2,
                golden=on,
            )
            self.source.summon(2, [summon])

    player.register(FakeTrojanDonkeySummon)

    fight(player, enemy, limit=5)

    generic = player.characters.get(2)

    assert generic
    assert generic.attack == (5 if on else 1)
    assert generic.health == (5 if on else 1)


def test_gepetto():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
        ],
        hero='SBB_HERO_GEPETTO',
        level=3
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(id='GENERIC', position=1)],
    )
    fight(player, enemy)

    cat = player.characters.get(1)

    assert cat
    assert cat.attack == 4 and cat.health == 4


@pytest.mark.parametrize('on', (True, False))
def test_krampus(on):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1, tribes=['evil'] if on else [], attack=2 if on else 1, health = 2 if on else 1),
        ],
        hero='SBB_HERO_KRAMPUS',
        level=3
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(attack=10, health=10)
        ]
    )
    fight(player, enemy, limit=1)

    evil = player.characters.get(1)

    assert evil
    assert evil.attack, evil.health == ((2, 2) if on else (1, 1))


@pytest.mark.parametrize('on', (True, False))
def test_mrsclaus(on):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_PRINCESSPEEP', position=1),
        ],
        hero='SBB_HERO_MRSCLAUS',
        level=3
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(attack=10, health=10)
        ]
    )
    fight(player, enemy, limit=1)

    good = player.characters.get(1)

    assert good
    assert good.id == "SBB_CHARACTER_SHEEP"
    assert good.attack, good.health == ((2, 2) if on else (1, 1))


def test_merlin():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_MONSTERBOOK'),
            make_character(attack=0, position=7)
        ],
        hero='SBB_HERO_MERLIN',
        level=6
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(id='GENERIC', position=1)],
    )
    fight(player, enemy)



    char = player.characters.get(7)

    assert char
    for pos in [7]:
        wizardbuffs = [
            r for r in player.characters[pos]._action_history if r.reason == ActionReason.MERLIN_BUFF
        ]

        assert len(wizardbuffs) == 1


def test_merlin_not_activate():
    player = make_player(
        raw=True,
        characters=[
            make_character(attack=0, position=7)
        ],
        spells=[
            "SBB_SPELL_FIREBALL"
        ],
        hero='SBB_HERO_MERLIN',
        level=6
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(id='GENERIC', position=1)],
    )
    enemy_char = enemy.characters[1]

    fight(player, enemy)

    char = player.characters.get(7)

    assert char
    for pos in [7]:
        wizardbuffs = [
            r for r in player.characters[pos]._action_history if r.reason == ActionReason.MERLIN_BUFF
        ]

        assert len(wizardbuffs) == 0

    assert enemy_char
    assert enemy_char.dead


@pytest.mark.parametrize('on', (True, False))
def test_jacks_giant(on):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1 if on else 5)
        ],
        hero='SBB_HERO_SIRPIPS-A-LOT',
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(attack=10, health=10)
        ]
    )
    fight(player, enemy, limit=1)

    generic = player.characters.get(1 if on else 5)

    assert generic
    assert generic.id == "SBB_CHARACTER_CAT"
    assert generic.health == (3 if on else 1)


@pytest.mark.parametrize('on', (True, False))
def test_mihri(on):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='ROYAL', position=1, tribes=['royal'] if on else []),
            make_character(id='ROYAL', position=2, tribes=['royal'] if on else [])
        ],
        hero='SBB_HERO_KINGLION',
        mihri_buff=5
    )

    enemy = make_player(raw=True)
    fight(player, enemy)

    for pos in [1, 2]:
        royal = player.characters.get(pos)

        mihri_buff = None
        for action in royal._action_history:
            if action.reason == ActionReason.MIHRI_BUFF:
                mihri_buff = action
                break

        if on:
            assert mihri_buff.attack == 5
            assert mihri_buff.health == 10
        else:
            assert mihri_buff is None


@pytest.mark.parametrize('on', (True, False))
def test_mihri_rollback_safety(on):
    player = make_player(
        raw=False,
        characters=[
            make_character(id='ROYAL', position=1, health=30, tribes=['royal'] if on else []),
        ],
        hero='SBB_HERO_KINGLION',
        mihri_buff=5,
    )

    enemy = make_player(raw=True)

    fight_event_manager = EventManager()

    fight_event_manager._events['OnSetup'].update(player._events['OnSetup'])
    fight_event_manager._events['OnSetup'].update(enemy._events['OnSetup'])
    fight_event_manager("OnSetup")

    c1 = player.characters[1]
    player.despawn(c1, kill=False)
    player.spawn(c1, 1)

    assert c1.attack == 1
    assert c1.health == 30


def test_trophy_hunter():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT')
        ],
        hero='SBB_HERO_MILITARYLEADER',
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )

    enemy = make_player(
        raw=True,
        characters=[make_character(id='GENERIC', position=1)],
    )
    fight(player, enemy)

    assert player.characters[1].id == 'SBB_CHARACTER_CAT'
    assert player.characters[2].id == 'SBB_CHARACTER_CAT'


def test_trophy_hunter2():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_LOBO')
        ],
        hero='SBB_HERO_MILITARYLEADER',
        treasures=[
            '''SBB_TREASURE_CLOAKOFTHEASSASSIN''',
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )

    enemy = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT')
        ]
    )
    fight(player, enemy, limit=1)

    blackcat = player.characters[1]
    assert blackcat
    assert blackcat.id == "SBB_CHARACTER_BLACKCAT"
    assert blackcat.attack == 4
    assert blackcat.health == 4


def test_trophy_hunter_yaga():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', attack=4, position=1),
            make_character(id="SBB_CHARACTER_BABAYAGA", position=5)
        ],
        hero='SBB_HERO_MILITARYLEADER',
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
    )

    enemy = make_player(
        raw=True,
        characters=[
            make_character()
        ]
    )
    fight(player, enemy)

    for pos in [1, 2, 3]:
        assert player.characters[pos].id == "SBB_CHARACTER_CAT"


@pytest.mark.parametrize('limit', (1, 5, 9))
def test_trophy_hunter_friendlyspirit(limit):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_FRIENDLYGHOST', position=1, attack=5, health=10),
            make_character(position=6, attack=5, health=10)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
        hero='SBB_HERO_MILITARYLEADER',
    )

    enemy = make_player(
        raw=True,
        characters=[
            make_character(attack=0, health=1, position=1),
            make_character(attack=0, health=1, position=2),
            make_character(attack=0, health=1, position=3),
            make_character(attack=0, health=1, position=4),
            make_character(attack=0, health=1, position=5),
            make_character(attack=0, health=1, position=6),
            make_character(attack=0, health=1, position=7),
        ]
    )
    fight(player, enemy, limit=limit)

    ghost = player.characters[1]
    ally = player.characters[6]
    if limit == 1:
        final_stats = (10, 20)
    elif limit == 5:
        final_stats = (15, 30)
    elif limit == 9:
        final_stats = (20, 40)
    else:
        raise ValueError(f'Limit of {limit} is not configured in the test')

    assert (ghost.attack, ghost.health) == (5, 10)
    assert (ally.attack, ally.health) == final_stats


@pytest.mark.parametrize('on', (True, False))
def test_beauty(on):
    player = make_player(
        raw=True,
        characters=[
            make_character(position=1, tribes=['good'] if on else []),
            make_character(position=2, tribes=['evil'] if on else [])
        ],
        hero='SBB_HERO_PRINCESSBELLE',
        hand=[make_character(id=f'TEST{i}', attack=i) for i in range(4)]
    )

    enemy = make_player(raw=True,)

    fight(player, enemy)

    t1 = player.characters[1].tribes
    t2 = player.characters[2].tribes
    tribe_set = {Tribe.EVIL, Tribe.GOOD}
    assert t1 == tribe_set if on else t1 == set()
    assert t2 == tribe_set if on else t2 == set()


@pytest.mark.parametrize('treasure', ("SBB_TREASURE_CORRUPTEDHEARTWOOD", "SBB_TREASURE_CROWNOFATLAS"))
def test_beauty_withtreasure(treasure):
    player = make_player(
        raw=True,
        characters=[
            make_character(position=1, tribes=[Tribe.ANIMAL]),
        ],
        treasures=[
            treasure
        ],
        hero='SBB_HERO_PRINCESSBELLE',
        hand=[make_character(id=f'TEST{i}', attack=i) for i in range(4)]
    )

    enemy = make_player(raw=True)

    fight(player, enemy)

    assert player.characters[1].tribes == {Tribe.GOOD, Tribe.EVIL, Tribe.ANIMAL}


def test_beauty_spawnedanimal():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT", position=1, ),
        ],
        hero='SBB_HERO_PRINCESSBELLE',
        hand=[make_character(id=f'TEST{i}', attack=i) for i in range(4)]
    )

    enemy = make_player(
        raw=True,
        characters=[
            make_character()
        ]
    )

    fight(player, enemy)

    assert player.characters[1].tribes == {Tribe.GOOD, Tribe.EVIL, Tribe.ANIMAL}


FALLEN_ANGEL_TESTS = (
    (['good'], 1, 3),
    (['evil'], 3, 1),
    (['good', 'evil'], 3, 3),
    ([], 1, 1)
)

@pytest.mark.parametrize('tribes, attack, health', FALLEN_ANGEL_TESTS)
def test_fallen_angel(tribes, attack, health):
    player = make_player(
        raw=True,
        characters=[make_character(id="SBB_CHARACTER_BLACKCAT", health=health, attack=attack, position=i, tribes=tribes) for i in range(1, 4)],
        hero='SBB_HERO_FALLENANGEL',
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
    )

    enemy = make_player(
        raw=True,
        characters=[make_character(attack=10, health=10)]
    )

    fight(player, enemy, limit=1)



    for pos in [1, 2, 3]:
        char = player.characters.get(pos)
        assert char
        if pos == 1:
            assert char.id == "SBB_CHARACTER_CAT"
        assert char.health == health
        assert char.attack == attack


FALLEN_ANGEL_RAW_TESTS = (
    (['good'], 1, 3),
    (['evil'], 3, 1),
    (['good', 'evil'], 3, 3),
    ([], 1, 1)
)
@pytest.mark.parametrize('tribes, attack, health', FALLEN_ANGEL_RAW_TESTS)
def test_fallen_angel_raw(tribes, attack, health):
    player = make_player(
        raw=True,
        characters=[make_character(position=i, tribes=tribes, attack=attack, health=health) for i in range(1, 4)],
        hero='SBB_HERO_FALLENANGEL',
    )

    enemy = make_player()

    fight(player, enemy)

    fallen_angel_buff = player.hero.aura

    if 'good' in tribes:
        assert fallen_angel_buff.health == 2
    else:
        assert fallen_angel_buff.health == 0
    if 'evil' in tribes:
        assert fallen_angel_buff.attack == 2
    else:
        assert fallen_angel_buff.attack == 0

    for char in player.characters.values():
        if char:
            assert char.health == health
            assert char.attack == attack


def test_muerte():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT')
        ],
        hero='SBB_HERO_MUERTE',
    )

    enemy = make_player(
        raw=True,
        characters=[make_character(id='GENERIC', position=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy)

    assert player.characters[1].id == 'SBB_CHARACTER_CAT'
    assert player.characters[2].id == 'SBB_CHARACTER_CAT'


def test_pup():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT')
        ],
        hero='SBB_HERO_GANDALF',
    )

    enemy = make_player(
        raw=True,
        characters=[
            make_character()
        ]
    )

    fight(player, enemy, limit=1)

    assert player.characters[1].id == "SBB_CHARACTER_CAT"
    assert player.characters[1].attack == 1
    assert player.characters[1].health == 1


def test_pup_shouldntbuff():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT", position=1),
            make_character(id="SBB_CHARACTER_ANGRYDWARF", position=5)
        ],
        hero='SBB_HERO_GANDALF',
    )

    enemy = make_player(
        characters=[
            make_character()]
        ,
        raw=True
    )

    fight(player, enemy)

    assert player.characters[1].id == "SBB_CHARACTER_CAT"
    assert player.characters[1].attack == 1
    assert player.characters[1].health == 1


def test_pup_shouldbuff():
    player = make_player(
        raw=True,
        characters=[
            make_character(tribes=[Tribe.DWARF], attack=5, health=4, position=1),
            make_character(id="SBB_CHARACTER_ANGRYDWARF", position=5)
        ],
        hero='SBB_HERO_GANDALF',
    )

    enemy = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_BABYDRAGON")
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )

    fight(player, enemy)

    assert player.characters[1].attack == 1
    assert player.characters[1].health == 1
