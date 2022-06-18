from sbbbattlesim.player import Player


class StatType:
    display_name = 'Prized Pig Survival Rate'

    @classmethod
    def calculate(cls, player: Player) -> int:
        return sum(
            player.valid_characters(_lambda=lambda char: char.id == 'SBB_CHARACTER_PRIZEDPIG')
        )