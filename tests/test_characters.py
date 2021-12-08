import pytest

from sbbbattlesim import Board
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.utils import Tribe, StatChangeCause
from tests import make_character, make_player


@pytest.mark.parametrize('char', character_registry.filter())
def test_valid_character(char):
    char = character_registry[char.id]
    assert char.valid()
    assert char.display_name
    assert next(character_registry.filter(
        _lambda=lambda char_cls: char_cls.id != char.id and char_cls.display_name == char.display_name), True)


@pytest.mark.parametrize('attack', (True, False))
@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', character_registry.filter())
def test_character(char, attack, golden):
    '''Run a combat, results dont matter. This will either crash or pass'''
    char = make_character(id=char.id, golden=golden)
    generic_char = make_character(position=7, tribes=[tribe.value for tribe in Tribe])
    player = make_player(
        level=2,
        characters=[char, generic_char],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if attack else []
    )
    enemy = make_player(
        characters=[make_character()],
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if not attack else []
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=5)


SUPPORT_EXCLUSION = (
    'SBB_CHARACTER_RIVERWISHMERMAID',
    'SBB_CHARACTER_ELDERTREANT',
    'SBB_CHARACTER_BABAYAGA'
)


# TODO write tests that iterate over SUPPORT_EXCLUSION for sanitys sake

@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('horn', (True, False))
@pytest.mark.parametrize('char', character_registry.filter(_lambda=lambda char: char.support is True))
def test_support(char, golden, horn):
    '''Support units that apply buffs get tested to make sure that literally any buff is getting applied'''
    # Riverwish is a support but doesn't give stats so it won't be tested here
    if char.id in SUPPORT_EXCLUSION:
        return

    player = make_player(
        characters=[
            make_character(id=char.id, position=7 if horn else 5, golden=golden),
            make_character(tribes=[tribe.value for tribe in Tribe])
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
            "SBB_TREASURE_BANNEROFCOMMAND" if horn else '',
        ]
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)

    assert board.p1.characters[1]._action_history[0].reason == StatChangeCause.SUPPORT_BUFF


class FakePlayer:
    stateful_effects = dict()
    id = "Fake"
    class FakeBoard:
        def register(self, *args, **kwargs):
            pass

    board = FakeBoard()

    def register(self, *args, **kwargs):
        pass


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', character_registry.filter(
    _lambda=lambda char: any([e.slay for e in char(FakePlayer(), 0, 0, 0, False, set(), 0).get('OnAttackAndKill')])))
def test_slay(char, golden):
    '''Triggers a slay, checks success by measuring against a shadow assassin. Liable to fail in the future... '''

    player = make_player(
        level=2,
        characters=[
            make_character(id=char.id, position=1, golden=golden),
            make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=7, golden=False, attack=2, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(position=1, attack=0, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (3, 2)


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', character_registry.filter(_lambda=lambda char: char.last_breath is True))
def test_last_breath(char, golden):
    '''Loads in every last breath and makes sure it triggers muerte'''
    last_breath = make_character(id=char.id, position=1, attack=0, health=1, golden=golden)
    player = make_player(
        hero='SBB_HERO_MUERTE',
        characters=[last_breath],
    )
    enemy = make_player(
        characters=[make_character(attack=50, health=50)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()

    assert board.p1.hero.triggered


@pytest.mark.parametrize('golden', (True, False))
def test_baba_yaga(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_LANCELOT', position=1, attack=1, health=1),
            make_character(id='SBB_CHARACTER_BABAYAGA', position=5, attack=0, health=1, golden=golden)
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=0, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()

    player = board.p1

    if golden:
        assert player.characters[1].attack == 7
    else:
        assert player.characters[1].attack == 5


def test_soltak():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_SOLTAKANCIENT', position=1, attack=0, health=1),
            make_character(id='PROTECTED', position=5)
        ],
    )
    enemy = make_player(
        characters=[make_character(id='SBB_CHARACTER_BABYDRAGON', health=2)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()

    player = board.p1

    assert player.characters[5] is None
    assert player.characters[1] is not None


def test_trojan_donkey():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_TROJANDONKEY', position=1, attack=1, health=2)
        ],
        level=3
    )
    enemy = make_player(
        characters=[make_character()],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()

    player = board.p1

    assert player.characters[2] is not None


def test_wombats_in_disguise():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_WOMBATSINDISGUISE')
        ],
        level=3
    )
    enemy = make_player(
        characters=[make_character()],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()

    player = board.p1

    wombat_spawn = player.characters.get(1)

    assert wombat_spawn
    assert StatChangeCause.WOMBATS_IN_DISGUISE_BUFF in [r.reason for r in wombat_spawn._action_history]


def test_doombreath():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_DOOMBREATH')
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(position=2),
            make_character(position=5),
            make_character(position=6),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()

    player = board.p2

    for i in (2, 5, 6):
        assert player.characters[i] is None
