from sbbbattlesim.characters import Character
import logging

from sbbbattlesim.events import OnStart, OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class CharacterType(Character):
    display_name = 'Angry'

    _attack = 4
    _health = 10
    _level = 5
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class AngryBuff(OnDamagedAndSurvived):
            def handle(self, *args, **kwargs):
                stat_change = 4 if self.manager.golden else 2
                for dwarf in self.manager.owner.valid_characters(_lambda=lambda char: 'dwarf' in char.tribes):
                    dwarf.change_stats(attack=stat_change, health=stat_change, temp=False, reason=StatChangeCause.ANGRY_BUFF)

        self.register(AngryBuff)
