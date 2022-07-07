import typing

from sbbbattlesim.characters.SBB_CHARACTER_POLYWOGGLE import PolyWoggleSlay
from sbbbattlesim.player import Player
from sbbbattlesim.stats import StatBase


class StatType(StatBase):
    display_name = 'Poly Woggle Slay'
    display_format = '{}%'
    unit_ids = ('SBB_CHARACTER_POLYWOGGLE',)

    @staticmethod
    def calculate(player: Player) -> int:
        return sum(
            1 for record in player.combat_records
            if isinstance(record.event, PolyWoggleSlay)
        )

    @staticmethod
    def merge(stats: typing.List['StatBase']):
        return (sum(stats) / len(stats)) * 100