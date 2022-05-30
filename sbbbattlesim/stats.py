from dataclasses import dataclass

from sbbbattlesim.player import Player


@dataclass
class CombatStats:
    win_id: (str, None)
    damage: int
    first_attacker: (str, None)


def calculate_damage(player: Player) -> int:
    if player is None:
        return 0

    damage = player.level
    for char in player.valid_characters():
        damage += 3 if char.golden else 1

    return damage
