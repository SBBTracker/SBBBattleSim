from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Sky Castle'
    aura = True

    _level = 4

    def buff(self, target_character, *args, **kwargs):
        if Tribe.PRINCE in target_character.tribes or Tribe.PRINCESS in target_character.tribes:
            for _ in range(1 + bool(self.mimic)):
                Buff(reason=StatChangeCause.SKYCASTLE, source=self, targets=[target_character],
                     health=4, attack=4, temp=True, *args, **kwargs).resolve()
