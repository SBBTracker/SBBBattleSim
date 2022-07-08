from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import Tribe

def _changeling(char: Character):
    for tribe in Tribe:
        char.tribes.add(tribe)


class TreasureType(Treasure):
    display_name = 'Radiant Prism'
    aura = True

    _level = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(reason=ActionReason.RADIANT_PRISM, source=self, _action=_changeling, priority=9999)