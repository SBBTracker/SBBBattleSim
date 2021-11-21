from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Ring of Rage'
    aura = True

    def buff(self, target_character):
        target_character.change_stats(attack=3, reason=StatChangeCause.RING_OF_RAGE, source=self, temp=True)
