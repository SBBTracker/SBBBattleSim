from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Ring of Rage'
    aura = True

    _level = 4

    def buff(self, target_character, *args, **kwargs):
        for _ in range(self.mimic + 1):
            target_character.change_stats(attack=3, reason=StatChangeCause.RING_OF_RAGE, source=self, temp=True, *args,
                                          **kwargs)
