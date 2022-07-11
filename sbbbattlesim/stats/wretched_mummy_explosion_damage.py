import typing

from sbbbattlesim.action import ActionReason
from sbbbattlesim.player import Player
from sbbbattlesim.stats import StatBase


class StatType(StatBase):
    display_name = 'Average Wretched Mummy Explosion Damage'
    display_format = '{}'
    unit_ids = ('SBB_CHARACTER_WRETCHEDMUMMY',)
    disabled = True

    @staticmethod
    def calculate(player: Player) -> int:
        return sum(
            record.damage for record in player.combat_records
            if record.reason == ActionReason.WRETCHED_MUMMY_EXPLOSION
        )

    @staticmethod
    def merge(stats: typing.List[typing.Union[str, int, float]]):
        return sum(stats) / len(stats)