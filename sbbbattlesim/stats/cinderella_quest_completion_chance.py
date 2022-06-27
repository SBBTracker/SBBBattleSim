import typing

from sbbbattlesim.player import Player
from sbbbattlesim.stats import StatBase


class StatType(StatBase):
    display_name = 'Cinderella Quest Progress'
    display_format = '{}'
    unit_id = 'SBB_CHARACTER_CINDER-ELLA'

    quest = True

    @staticmethod
    def calculate(player: Player) -> int:
        return sum(1 for char in player.completed_quests if char.id == 'SBB_CHARACTER_CINDER-ELLA')

    @staticmethod
    def merge(stats: typing.List[typing.Union[str, int, float]]):
        return (sum(stats)/len(stats))