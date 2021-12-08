from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Deepstone Mine'
    aura = True

    _level = 3

    def buff(self, target_character, *args, **kwargs):
        if Tribe.DWARF in target_character.tribes:
            for _ in range(self.mimic + 1):
                Buff(reason=StatChangeCause.DEEPSTONE_MINE, source=self, targets=[target_character],
                     attack=2, health=2, temp=True, *args, **kwargs)
