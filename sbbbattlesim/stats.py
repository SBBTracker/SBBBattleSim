import collections
from typing import Dict, List

from sbbbattlesim import Board
from sbbbattlesim.player import Player


async def win_rate(results: Dict[str, List[Board]]) -> Dict[str, float]:
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


async def average_damage(results: Dict[str, List[Board]]) -> Dict[str, float]:
    avg_damage = collections.defaultdict(float)
    for pid, boards in results.items():
        damage = [calculate_damage(board.get_player(pid)) for board in boards]
        avg_damage[pid] = (sum(damage) / len(damage)) if damage else 0

    return avg_damage


class SimulationStats:
    @classmethod
    async def create(cls, results):
        self = SimulationStats()
        self.win_rate = await win_rate(results)
        self.avg_damage = await average_damage(results)
        return self
