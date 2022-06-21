import typing

from sbbbattlesim.player import Player
from sbbbattlesim.stats import StatBase


class StatType(StatBase):
    display_name = 'Lancelot Quest Completion Chance'
    display_format = '{}%'

    @staticmethod
    def calculate(player: Player) -> int:
        return sum(1 for char in player.completed_quests if char.id == 'SBB_CHARACTER_LANCELOT')

    @staticmethod
    def merge(stats: typing.List['StatBase']):
        return (sum(stats)/len(stats)) * 100