import typing

from sbbbattlesim.characters.SBB_CHARACTER_POLYWOGGLE import PolyWoggleSlay
from sbbbattlesim.characters.SBB_CHARACTER_QUESTINGPRINCESS import BravePrincessSlay
from sbbbattlesim.player import Player
from sbbbattlesim.stats import StatBase


class StatType(StatBase):
    display_name = 'Hercules Average Damage'
    display_format = '{}'
    unit_ids = ('SBB_CHARACTER_HERCULES',)

    quest = True

    @staticmethod
    def calculate(player: Player) -> int:
        return sum(
            record.damage for record in player.combat_records
            if record.source and record.source.id == 'SBB_CHARACTER_HERCULES' and record.damage > 0
        )

    @staticmethod
    def merge(stats: typing.List['StatBase']):
        return (sum(stats) // len(stats))