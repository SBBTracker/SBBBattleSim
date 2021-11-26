from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Tell Tale Quiver'
    aura = True

    _level = 3

    def buff(self, target_character):
        if target_character.position >= 5and target_character.ranged:
            for _ in range(self.mimic + 1):
                target_character.change_stats(health=3, attack=3, reason=StatChangeCause.TELL_TALE_QUIVER, source=self, temp=True)
