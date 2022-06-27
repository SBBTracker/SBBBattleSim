import typing

from sbbbattlesim.player import Player
from sbbbattlesim.stats import StatBase


class StatType(StatBase):
    display_name = 'Prized Pig Survival'
    display_format = '{}%'
    unit_id = 'SBB_CHARACTER_PRIZEDPIG'

    @staticmethod
    def calculate(player: Player) -> int:
        return len(
            player.valid_characters(_lambda=lambda char: char.id == 'SBB_CHARACTER_PRIZEDPIG')
        )

    @staticmethod
    def merge(stats: typing.List[typing.Union[str, int, float]]):
        return (sum(stats)/len(stats)) * 100
