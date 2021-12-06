from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Crown of Atlas'
    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):
        if Tribe.ANIMAL in target_character.tribes:

            for _ in range(self.mimic + 1):
                target_character.change_stats(health=1, attack=1, reason=StatChangeCause.CROWN_OF_ATLAS, source=self,
                                              temp=True, *args, **kwargs)

            # todo how does this interact with beauty? also check heartwood
            if Tribe.EVIL in target_character.tribes:
                target_character.tribes.remove(Tribe.EVIL)
            if Tribe.GOOD not in target_character.tribes:
                target_character.tribes.add(Tribe.GOOD)
