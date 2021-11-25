from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff
import logging

from sbbbattlesim.utils import StatChangeCause, Tribe

logger = logging.getLogger(__name__)

#aka doubly
class CharacterType(Character):
    display_name = 'Dubly'

    _attack = 1
    _health = 1
    _level = 3
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def change_stats(self, attack=0, health=0, *args, **kwargs):
        golden_multiplier = 3 if self.golden else 2
        super().change_stats(attack=attack * golden_multiplier, health=health * golden_multiplier, *args, **kwargs)
