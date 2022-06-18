from sbbbattlesim.action import ActionReason
from sbbbattlesim.player import Player


class StatType:
    display_name = 'Wretched Mummy Explosion Damage'

    @classmethod
    def calculate(cls, player: Player) -> int:
        return sum(
            record.damage for record in player.combat_records
            if record.reason == ActionReason.WRETCHED_MUMMY_EXPLOSION
        )