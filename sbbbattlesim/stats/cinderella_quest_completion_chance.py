import typing

from sbbbattlesim.player import Player
from sbbbattlesim.stats import StatBase


import importlib
CinderellaOnSpellCast = importlib.import_module('sbbbattlesim.characters.SBB_CHARACTER_CINDER-ELLA').CinderellaOnSpellCast


class StatType(StatBase):
    display_name = 'Cinderella Quest Progress'
    display_format = '{}'
    unit_ids = ('SBB_CHARACTER_CINDER-ELLA',)

    quest = True

    @staticmethod
    def calculate(player: Player) -> int:
        return sum(
            1 for record in player.combat_records
            if isinstance(record.event, CinderellaOnSpellCast)
        )

    @staticmethod
    def merge(stats: typing.List['StatBase']):
        return (sum(stats) / len(stats)) * 100