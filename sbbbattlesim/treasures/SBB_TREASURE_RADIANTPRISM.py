from sbbbattlesim.events import OnSetup

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import Tribe

# This is here to apply Radiant Prism at beginning of combat because the info isn't sent across the wire like Tribes
class RadiantPrismOnSetup(OnSetup):
    def handle(self, *args, **kwargs):
        for char in self.source.player.valid_characters():
            _changeling(char)

def _changeling(char: Character):
    for tribe in Tribe:
        char.tribes.add(tribe)


class TreasureType(Treasure):
    display_name = 'Radiant Prism'
    aura = True

    _level = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(RadiantPrismOnSetup, source=self, priority=9999)
        self.aura = Aura(reason=ActionReason.CROWN_OF_ATLAS, source=self, _action=_changeling)