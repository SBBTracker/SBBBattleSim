from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import Tribe


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
        stats = 1 * (self.multiplier + 1)
        self.aura = Aura(reason=ActionReason.CROWN_OF_ATLAS, source=self, health=stats, attack=stats,
                         _lambda=lambda char: Tribe.ANIMAL in char.tribes, _action=_crown_tribe_shift)
