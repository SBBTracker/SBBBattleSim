from sbbbattlesim.action import Buff, AuraBuff
from sbbbattlesim.characters import Character
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


def _crown_tribe_shift(char: Character):
    if Tribe.EVIL in char.tribes:
        char.tribes.remove(Tribe.EVIL)
    if Tribe.GOOD not in char.tribes:
        char.tribes.add(Tribe.GOOD)


class TreasureType(Treasure):
    display_name = 'Crown of Atlas'
    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 1 * (self.mimic + 1)
        self.aura_buff = AuraBuff(reason=StatChangeCause.CLOAK_OF_THE_ASSASSIN, source=self, health=stats, attack=stats,
                                  _lambda=lambda char: Tribe.ANIMAL in char.tribes, _action=_crown_tribe_shift)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
