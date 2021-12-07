import collections
from dataclasses import dataclass
from typing import Dict, List

from sbbbattlesim import Board
from sbbbattlesim.player import Player


def win_rate(results: Dict[str, List[Board]], player1_id: str, player2_id: str) -> Dict[str, float]:
    rates = collections.defaultdict(float)
    for pid, boards in results.items():
        total = sum(len(v) for v in results.values())
        rates[pid] = round(((len(results.get(pid, [])) / total) * 100), 2)

    for player_id in [player1_id, player2_id]:
        if player_id not in rates:
            rates[player_id] = 0

    return rates


def calculate_damage(player: Player) -> int:
    if player is None:
        return 0

    damage = player.level
    for char in player.valid_characters():
        damage += 3 if char.golden else 1

    return damage


def average_damage(results: Dict[str, List[Board]], player1_id: str, player2_id: str) -> Dict[str, float]:
    avg_damage = collections.defaultdict(float)
    for pid, boards in results.items():
        damage = [calculate_damage(board.get_player(pid)) for board in boards]
        avg_damage[pid] = (sum(damage) / len(damage)) if damage else 0

    for player_id in [player1_id, player2_id]:
        if player_id not in avg_damage:
            avg_damage[player_id] = 0
    return avg_damage


@dataclass
class SimulationStats:
    win_rate: Dict[str, float]
    avg_damage: Dict[str, float]


def calculate_stats(results, player1_id, player2_id):
    return SimulationStats(
        win_rate=win_rate(results, player1_id, player2_id),
        avg_damage=average_damage(results, player1_id, player2_id)
    )
