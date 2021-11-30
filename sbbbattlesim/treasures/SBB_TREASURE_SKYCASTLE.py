from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Sky Castle'
    aura = True

    _level = 4

    def buff(self, target_character, *args, **kwargs):
        if Tribe.PRINCE in target_character.tribes or Tribe.PRINCESS in target_character.tribes:
            for _ in range(1 + bool(self.mimic)):
                target_character.change_stats(health=4, attack=4, reason=StatChangeCause.SKYCASTLE, source=self, temp=True, *args, **kwargs)
