import logging

import pytest

from sbbbattlesim.action import Action, ActionReason, ActionState
from sbbbattlesim.characters import Character
from sbbbattlesim.events import SSBBSEvent
from sbbbattlesim.player import Player
from tests import PLAYER, TestEvent, create_test_setup, make_player, make_character


logger = logging.getLogger(__name__)


class TestAction(Action):
    def __init__(self, **kwargs):
        super().__init__(reason=ActionReason.TEST, **kwargs)


BUFF_PARAMS = (
    (1, 1, 1, 1, 2, 2),
    (1, 1, -2, -2, -1, -1),
    (1, 1, 1, -2, 2, -1),
    (1, 1, -2, 1, -1, 2),
)


@pytest.mark.parametrize('attack_start, health_start, attack_buff, health_buff, attack_final, health_final', BUFF_PARAMS)
def test_apply_buff(attack_start, health_start, attack_buff, health_buff, attack_final, health_final):
    board, player = create_test_setup(
        PLAYER=make_player(
            characters=[
                make_character(attack=attack_start, health=health_start)
            ]
        )
    )
    char = player.characters[1]
    action = TestAction(source=char, attack=attack_buff, health=health_buff)

    assert (char._base_attack, char._base_health) == (attack_start, health_start)
    action._apply(char)
    assert (char._base_attack, char.health) == (attack_final, health_final)
    action._clear(char)
    assert (char._base_attack, char._base_health) == (attack_start, health_start)


DMG_HEAL_PARAMS = (
    (0, 0, 1),
    (1, 0, 0),
    (1, 1, 1),
    (1, -1, 1),
    (-1, 0, 1),
)


@pytest.mark.parametrize('damage, heal, health_final', DMG_HEAL_PARAMS)
def test_apply_buff(damage, heal, health_final):
    attack_start, health_start = 1, 1
    attack_final = attack_start

    board, player = create_test_setup(
        PLAYER=make_player(
            characters=[
                make_character(attack=attack_start, health=health_start)
            ]
        )
    )
    char = player.characters[1]
    action = TestAction(source=char, damage=damage, heal=heal)

    assert (char._base_attack, char._base_health) == (attack_start, health_start)
    action._apply(char)
    assert (char._base_attack, char.health) == (attack_final, health_final)
    action._clear(char)
    assert (char._base_attack, char._base_health) == (attack_start, health_start)


def test_apply_debuff():
    attack_buff, health_buff = 1, 1
    attack_start, health_start = -10, -10
    attack_final, health_final = attack_start + attack_buff, health_start + health_buff

    board, player = create_test_setup(
        PLAYER=make_player(
            characters=[
                make_character(attack=attack_start, health=health_start)
            ]
        )
    )
    char = player.characters[1]
    action = TestAction(source=char, attack=attack_buff, health=health_buff)

    assert (char._base_attack, char._base_health) == (attack_start, health_start)
    action._apply(char)
    assert (char._base_attack, char.health) == (attack_final, health_final)
    action._clear(char)
    assert (char._base_attack, char._base_health) == (attack_start, health_start)


@pytest.mark.parametrize('_lambda', (True, False))
def test_execute(_lambda):
    attack_buff, health_buff = 1, 1
    attack_start, health_start = 1, 1
    attack_final, health_final = attack_start + attack_buff, health_start + health_buff

    board, player = create_test_setup(
        PLAYER=make_player(
            characters=[
                make_character(attack=attack_start, health=health_start)
            ]
        )
    )
    char = player.characters[1]
    action = TestAction(source=char, attack=attack_buff, health=health_buff, _lambda=lambda _: _lambda)

    assert (char._base_attack, char._base_health) == (attack_start, health_start)

    if not _lambda:
        action.execute(char)
        assert (char._base_attack, char._base_health) == (attack_start, health_start)
        return

    # Execute with setup=True
    # This should NOT change stats
    action.execute(char)
    assert (char._base_attack, char._base_health) == (attack_final, health_final)

    # Execute on the same character
    # This should NOT change stats
    action.execute(char)
    assert (char._base_attack, char._base_health) == (attack_final, health_final)


@pytest.mark.parametrize('setup', (True, False))
def test_setup(setup):
    attack_buff, health_buff = 1, 1
    attack_start, health_start = 2, 2

    board, player = create_test_setup(
        PLAYER=make_player(
            characters=[
                make_character(attack=attack_start, health=health_start)
            ]
        )
    )
    char = player.characters[1]
    action = TestAction(source=char, attack=attack_buff, health=health_buff)

    assert (char._base_attack, char._base_health) == (attack_start, health_start)

    action.execute(char, setup=setup)
    if setup:
        assert (char._base_attack, char._base_health) == (attack_start, health_start)
        action.roll_back()
        assert (char._base_attack, char._base_health) == (attack_start - attack_buff, health_start - health_buff)
    else:
        assert (char._base_attack, char._base_health) == (attack_start + attack_buff, health_start + health_buff)
        action.roll_back()
        assert (char._base_attack, char._base_health) == (attack_start, health_start)

def test_rollback():
    attack_buff, health_buff = 1, 1
    attack_start, health_start = 1, 1
    attack_final, health_final = attack_start + attack_buff, health_start + health_buff

    attack_start, health_start = 1, 1
    board, player = create_test_setup(
        PLAYER=make_player(
            characters=[
                make_character(attack=attack_start, health=health_start)
            ]
        )
    )
    char = player.characters[1]
    action = TestAction(source=char, attack=attack_buff, health=health_buff)
    assert (char._base_attack, char._base_health) == (attack_start, health_start)

    assert (char._base_attack, char._base_health) == (attack_start, health_start)
    action.execute(char)
    assert (char._base_attack, char._base_health) == (attack_final, health_final)
    action.roll_back()
    assert (char._base_attack, char._base_health) == (attack_start, health_start)


def test_resolve_damage():
    attack_start, health_start = 1, 1
    board, player = create_test_setup(
        PLAYER=make_player(
            characters=[
                make_character(attack=attack_start, health=health_start)
            ]
        )
    )
    char = player.characters[1]
    assert (char._base_attack, char._base_health) == (attack_start, health_start)


    action = TestAction(source=char, damage=1, targets=[char])
    action.resolve()
    assert char.dead


def test_resolve_minus_health():
    attack_start, health_start = 1, 1
    board, player = create_test_setup(
        PLAYER=make_player(
            characters=[
                make_character(attack=attack_start, health=health_start)
            ]
        )
    )
    char = player.characters[1]
    assert (char._base_attack, char._base_health) == (attack_start, health_start)

    action = TestAction(source=char, health=-2)

    action.execute(char)
    assert (char._base_attack, char._base_health) == (1, -1)
    assert char.dead

    action.resolve()
    assert char in char.player.graveyard


def test_event():
    board, player = create_test_setup(
        PLAYER=make_player(
            characters=[make_character()]
        )
    )
    char = player.characters[1]
    action = TestAction(source=char, event=TestEvent)
    action._register(char)

    assert char._events['SSBBSEvent']
    registered = list(char._events['SSBBSEvent'])[0]
    assert isinstance(registered, TestEvent)

    char('SSBBSEvent')
    assert registered.triggered

    action._unregister(char)

    assert not char._events['SSBBSEvent']
