from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Dragon Nest'
    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):
        if Tribe.DRAGON in target_character.tribes:
            for _ in range(self.mimic + 1):
                target_character.change_stats(attack=5, health=5, reason=StatChangeCause.DRAGON_NEST, source=self,
                                              temp=True, *args, **kwargs)
