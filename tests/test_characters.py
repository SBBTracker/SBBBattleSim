import logging

import pytest

from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('char', character_registry.filter())
def test_valid_character(char):
    char = character_registry[char.id]
    assert char.valid()
    assert char.display_name
    assert next(character_registry.filter(_lambda=lambda char_cls: char_cls.id != char.id and char_cls.display_name == char.display_name), True)


@pytest.mark.parametrize('attack', (True, False))
@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', character_registry.filter())
def test_character(char, attack, golden):
    logger = logging.getLogger(__name__)
    '''Run a combat, results dont matter. This will either crash or pass'''
    char = make_character(id=char.id, golden=golden)
    generic_char = make_character(position=7, tribes=[tribe.value for tribe in Tribe])
    player = make_player(
        raw=True,
        level=2,
        characters=[char, generic_char],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if attack else []
    )
    enemy = make_player(
        raw=True,
        characters=[make_character()],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if not attack else []
    )

    try:
        fight(player, enemy, limit=5)
    except:
        logger.error(f"{char['id']}")
        raise


SUPPORT_EXCLUSION = (
    'SBB_CHARACTER_RIVERWISHMERMAID',
    'SBB_CHARACTER_ELDERTREANT',
    'SBB_CHARACTER_BABAYAGA'
)


# TODO write tests that iterate over SUPPORT_EXCLUSION for sanitys sake

@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('horn', (True, False))
@pytest.mark.parametrize('char', character_registry.filter(_lambda=lambda char: char.support))
def test_support(char, golden, horn):
    '''Support units that apply buffs get tested to make sure that literally any buff is getting applied'''
    # Riverwish is a support but doesn't give stats so it won't be tested here
    if char.id in SUPPORT_EXCLUSION:
        return

    player = make_player(
        raw=True,
        characters=[
            make_character(id=char.id, position=7 if horn else 5, golden=golden),
            make_character(tribes=[tribe.value for tribe in Tribe])
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
            "SBB_TREASURE_BANNEROFCOMMAND" if horn else '',
        ]
    )
    enemy = make_player(raw=True)
    fight(player, enemy, limit=0)

    assert player.characters[1]._action_history[0].reason == ActionReason.SUPPORT_BUFF


class FakePlayer:
    stateful_effects = dict()
    id = "Fake"

    def register(self, *args, **kwargs):
        pass


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', character_registry.filter(_lambda=lambda char: char.slay is True))
def test_slay(char, golden):
    '''Triggers a slay, checks success by measuring against a shadow assassin. Liable to fail in the future... '''

    player = make_player(
        raw=True,
        level=2,
        characters=[
            make_character(id=char.id, position=1, golden=golden),
            make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=7, golden=False, attack=2, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(position=1, attack=0, health=1)],
    )
    fight(player, enemy, limit=-1)

    if char.id == '''SBB_CHARACTER_QUESTINGPRINCESS''' and golden:
        return

    assert (player.characters[7].attack, player.characters[7].health) == (3, 1)


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', character_registry.filter(_lambda=lambda char: char.last_breath is True))
def test_last_breath(char, golden):
    '''Loads in every last breath and makes sure it triggers muerte'''
    last_breath = make_character(id=char.id, position=1, attack=0, health=1, golden=golden)
    player = make_player(
        raw=True,
        hero='SBB_HERO_MUERTE',
        characters=[last_breath],
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=50, health=50)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy)

    assert player.hero.triggered


@pytest.mark.parametrize('golden', (True, False))
def test_baba_yaga(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_LANCELOT', position=1, attack=7 if golden else 4, health=1),
            make_character(id='SBB_CHARACTER_BABAYAGA', position=5, attack=0, health=1, golden=golden)
        ],
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=0, health=1)],
    )
    fight(player, enemy)

    if golden:
        assert player.characters[1].attack == 13
        assert player.characters[1].health == 7
    else:
        assert player.characters[1].attack == 8
        assert player.characters[1].health == 5


def test_soltak():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_SOLTAKANCIENT', position=1, attack=0, health=1),
            make_character(id='PROTECTED', position=5)
        ],
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(id='SBB_CHARACTER_BABYDRAGON', health=2)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy)

    assert player.characters[5] is None
    assert player.characters[1] is not None


def test_trojan_donkey():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_TROJANDONKEY', position=1, attack=1, health=2)
        ],
        level=3
    )
    enemy = make_player(
        raw=True,
        characters=[make_character()],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy)

    assert player.characters[2] is not None


def test_wombats_in_disguise():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_WOMBATSINDISGUISE')
        ],
        level=3
    )
    enemy = make_player(
        raw=True,
        characters=[make_character()],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy)

    wombat_spawn = player.characters.get(1)

    assert wombat_spawn
    assert ActionReason.WOMBATS_IN_DISGUISE_BUFF in [r.reason for r in wombat_spawn._action_history]


def test_doombreath():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_RIVERWISHMERMAID', position=5),
            make_character(id='SBB_CHARACTER_DOOMBREATH', health=2)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=2),
            make_character(position=5),
            make_character(position=6),
            make_character(position=7),
        ],
    )
    fight(player, enemy, limit=1)

    for i in (2, 5, 6):
        assert enemy.characters[i] is None

    assert enemy.characters[7] is not None

    doombreath = player.characters[1]
    riverwish = player.characters[5]
    assert doombreath.attack == 4
    assert doombreath.health == 4

    buffs = [r for r in doombreath._action_history if r.source is riverwish and r.event is None]

    assert len(buffs) == 3
    assert sum([b.attack for b in buffs]) == 3
    assert sum([b.health for b in buffs]) == 3
