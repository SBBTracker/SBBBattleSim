from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Corrupted Heartwood'

    def buff(self, target_character):
        if 'animal' in target_character.tribes or 'treant' in target_character.tribes:
            target_character.change_stats(attack=1, reason=StatChangeCause.CORRUPTED_HEARTWOOD, source=self, temp=True)

            if Tribe.GOOD in target_character.tribes:
                target_character.remove(Tribe.GOOD)
            if Tribe.EVIL not in target_character.tribes:
                target_character.append(Tribe.EVIL)
