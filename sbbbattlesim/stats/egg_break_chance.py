import typing

from sbbbattlesim.action import ActionReason
from sbbbattlesim.characters.SBB_CHARACTER_HUMPTYDUMPTY import HumptyDumptyOnDeath
from sbbbattlesim.characters.SBB_CHARACTER_POLYWOGGLE import PolyWoggleSlay
from sbbbattlesim.characters.SBB_CHARACTER_QUESTINGPRINCESS import BravePrincessSlay
from sbbbattlesim.player import Player
from sbbbattlesim.stats import StatBase


class StatType(StatBase):
    display_name = 'Scrambled Egg Chance'
    display_format = '{}%'
    unit_ids = (
        'SBB_CHARACTER_HUMPTYDUMPTY',
    )

    @staticmethod
    def calculate(player: Player) -> int:
        return sum(
            1 for record in player.combat_records
            if isinstance(record.event, HumptyDumptyOnDeath)
        )

    @staticmethod
    def merge(stats: typing.List[typing.Union[str, int, float]]):
        return (sum(stats) / len(stats)) * 100