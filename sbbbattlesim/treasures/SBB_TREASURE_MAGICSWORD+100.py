from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Magic Sword +100'
    aura = True

    _level = 7

    def buff(self, target_character, *args, **kwargs):
        if 1 == target_character.position:
            for _ in range(bool(self.mimic) + 1):
                target_character.change_stats(attack=100, reason=StatChangeCause.MAGIC_SWORD, source=self, temp=True, *args, **kwargs)
