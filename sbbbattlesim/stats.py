import collections
from dataclasses import dataclass
from typing import Dict, List

from sbbbattlesim import Board
from sbbbattlesim.player import Player


@dataclass
class BoardStats:
    win_id: (str, None)
    damage: int


def win_rate(results: List[BoardStats]) -> Dict[str, float]:
    win_rate = collections.defaultdict(float)
    for pid, boards in results.items():
        total = sum(len(v) for v in results.values())
        win_rate[pid] = round(((len(results.get(pid, [])) / total) * 100), 2)

    return win_rate


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
            damage=calculate_damage(player)
        )
    else:
        return BoardStats(
            win_id=None,
            damage=0
        )
