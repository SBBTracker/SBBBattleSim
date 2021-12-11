from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Corrupted Heartwood'
    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):
        if Tribe.ANIMAL in target_character.tribes or Tribe.TREANT in target_character.tribes:

            for _ in range(self.mimic + 1):
                Buff(reason=StatChangeCause.CORRUPTED_HEARTWOOD, source=self, targets=[target_character],
                     attack=1, temp=True, *args, **kwargs).resolve()

            if Tribe.GOOD in target_character.tribes:
                target_character.tribes.remove(Tribe.GOOD)
            if Tribe.EVIL not in target_character.tribes:
                target_character.tribes.add(Tribe.EVIL)
