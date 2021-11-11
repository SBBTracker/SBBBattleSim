from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Crown of Atlas'

    def buff(self, target_character):
        if 'animal' in target_character.tribes:
            target_character.change_stats(health=1, attack=1, reason=StatChangeCause.CROWN_OF_ATLAS, source=self,
                                          temp=True)

            # todo implement alignment changing this is actually pseudo code
            if Tribe.EVIL in target_character.tribes:
                target_character.remove(Tribe.EVIL)
            if Tribe.GOOD not in target_character.tribes:
                target_character.append(Tribe.GOOD)
