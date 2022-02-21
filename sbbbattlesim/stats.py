import collections
from dataclasses import dataclass
from typing import Dict, List

from sbbbattlesim import Board
from sbbbattlesim.player import Player


@dataclass
class BoardStats:
    win_id: (str, None)
    damage: int
    first_attacker: str


def calculate_damage(player: Player) -> int:
    if player is None:
        return 0

    damage = player.level
    for char in player.valid_characters():
        damage += 3 if char.golden else 1

    return damage


def calculate_stats(board: Board) -> BoardStats:
    player = board.winner
    if player:
        return BoardStats(
            win_id=player.id,
            damage=calculate_damage(player),
            first_attacker=board.first_attacker
        )
    else:
        return BoardStats(
            win_id=None,
            damage=0,
            first_attacker=board.first_attacker
        )
