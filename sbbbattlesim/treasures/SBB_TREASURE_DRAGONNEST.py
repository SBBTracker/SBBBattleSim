from sbbbattlesim.action import Buff
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Dragon Nest'
    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):
        if Tribe.DRAGON in target_character.tribes:
            for _ in range(self.mimic + 1):
                Buff(reason=StatChangeCause.DRAGON_NEST, source=self, targets=[target_character],
                     attack=5, health=5, temp=True, *args, **kwargs).resolve()
