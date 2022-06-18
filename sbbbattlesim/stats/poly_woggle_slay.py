from sbbbattlesim.characters.SBB_CHARACTER_POLYWOGGLE import PolyWoggleSlay
from sbbbattlesim.player import Player


class StatType:
    display_name = 'Poly Woggle Slay Chance'

    @classmethod
    def calculate(cls, player: Player) -> int:
        return sum(
            1 for record in player.combat_records
            if isinstance(record.event, PolyWoggleSlay)
        )