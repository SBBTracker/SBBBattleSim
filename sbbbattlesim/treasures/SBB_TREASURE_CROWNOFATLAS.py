from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Crown of Atlas'
    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):
        if Tribe.ANIMAL in target_character.tribes:

            for _ in range(self.mimic + 1):
                Buff(reason=StatChangeCause.CROWN_OF_ATLAS, source=self, targets=[target_character],
                     health=1, attack=1, temp=True, *args, **kwargs).resolve()

            if Tribe.EVIL in target_character.tribes:
                target_character.tribes.remove(Tribe.EVIL)
            if Tribe.GOOD not in target_character.tribes:
                target_character.tribes.add(Tribe.GOOD)
