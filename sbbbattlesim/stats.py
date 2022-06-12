import typing
from dataclasses import dataclass

from sbbbattlesim.action import ActionReason
from sbbbattlesim.player import Player


@dataclass
class CombatStats:
    win_id: (str, None)
    damage: int
    action_counters: typing.Dict[str, typing.Dict[str, int]]
    first_attacker: (str, None)


def calculate_damage(player: Player) -> int:
    if player is None:
        return 0

    damage = player.level
    for char in player.valid_characters():
        damage += 3 if char.golden else 1

    return damage


def clean_action_counters(counters: dict):
    cleaned_counters = {}

    for reason, counter in counters.items():
        if isinstance(reason, tuple):
            cleaned_counters[f'{reason[0]} {reason[1].pretty_print()}'] = counter
        elif isinstance(reason, ActionReason) and reason.value > 100:  # TODO is reason.value > 100 enough to chop out uninteresting data
            cleaned_counters[reason.pretty_print()] = counter

    return cleaned_counters
