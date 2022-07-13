import typing

from sbbbattlesim.action import ActionReason
from sbbbattlesim.characters.SBB_CHARACTER_POLYWOGGLE import PolyWoggleSlay
from sbbbattlesim.characters.SBB_CHARACTER_QUESTINGPRINCESS import BravePrincessSlay
from sbbbattlesim.player import Player
from sbbbattlesim.stats import StatBase


class StatType(StatBase):
    display_name = 'Average Number of Summons'
    display_format = '{}'
    unit_ids = (
        # Summon Comp Units
        'SBB_CHARACTER_PROSPERO',
        'SBB_CHARACTER_BABYBEAR',
        'SBB_CHARACTER_HUNGRYHUNGRYHIPPOCAMPUS',
        'SBB_CHARACTER_BLACKCAT',
        'SBB_CHARACTER_PRINCESSPEEP',
        'SBB_CHARACTER_WOMBATSINDISGUISE',
        'SBB_CHARACTER_TROJANDONKEY',
        
        # Scam
        'SBB_CHARACTER_PUMPKINKING',
        'SBB_CHARACTER_THREEBIGPIGS',
        'SBB_CHARACTER_LOBO',
    )

    @staticmethod
    def calculate(player: Player) -> int:
        return sum(
            1 for record in player.combat_records
            if record.reason == ActionReason.SUMMON
        )

    @staticmethod
    def merge(stats: typing.List[typing.Union[str, int, float]]):
        return (sum(stats) / len(stats))