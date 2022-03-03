from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import Tribe


class TreasureType(Treasure):
    display_name = 'Sky Castle'

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
