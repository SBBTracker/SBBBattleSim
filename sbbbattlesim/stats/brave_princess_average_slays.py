import typing

from sbbbattlesim.characters.SBB_CHARACTER_POLYWOGGLE import PolyWoggleSlay
from sbbbattlesim.characters.SBB_CHARACTER_QUESTINGPRINCESS import BravePrincessSlay
from sbbbattlesim.player import Player
from sbbbattlesim.stats import StatBase


class StatType(StatBase):
    display_name = 'Brave Princess Slays'
    display_format = '{}'
    unit_ids = ('SBB_CHARACTER_QUESTINGPRINCESS',)

    quest = True

    @staticmethod
    def calculate(player: Player) -> int:
        return sum(
            1 for record in player.combat_records
            if isinstance(record.event, BravePrincessSlay)
        )

    @staticmethod
    def merge(stats: typing.List[typing.Union[str, int, float]]):
        return (sum(stats) / len(stats))