from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import Tribe


def _heartwood_tribe_shift(char: Character):
    if Tribe.GOOD in char.tribes:
        char.tribes.remove(Tribe.GOOD)
    if Tribe.EVIL not in char.tribes:
        char.tribes.add(Tribe.EVIL)


class TreasureType(Treasure):
    display_name = 'Corrupted Heartwood'
    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 1 * (self.multiplier + 1)
        self.aura = Aura(reason=ActionReason.CORRUPTED_HEARTWOOD, source=self, attack=stats,
                         _lambda=lambda char: Tribe.ANIMAL in char.tribes or Tribe.TREANT in char.tribes,
                         _action=_heartwood_tribe_shift)
