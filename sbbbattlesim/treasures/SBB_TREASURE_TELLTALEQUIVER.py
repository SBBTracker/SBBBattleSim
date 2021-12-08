from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Tell Tale Quiver'
    aura = True

    _level = 3

    def buff(self, target_character, *args, **kwargs):
        if target_character.position >= 5 and target_character.ranged:
            for _ in range(self.mimic + 1):
                Buff(reason=StatChangeCause.TELL_TALE_QUIVER, source=self, targets=[target_character],
                     health=3, attack=3, temp=True, *args, **kwargs).resolve()
