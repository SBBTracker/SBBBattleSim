import logging

from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe, StatChangeCause

logger = logging.getLogger(__name__)


class AngryBuff(OnDamagedAndSurvived):
    def handle(self, stack, *args, **kwargs):
        stat_change = 4 if self.manager.golden else 2
        Buff(reason=StatChangeCause.ANGRY_BUFF, source=self.manager,
             targets=self.manager.player.valid_characters(_lambda=lambda char: Tribe.DWARF in char.tribes),
             attack=stat_change, health=stat_change, temp=False, stack=stack,
             ).resolve()


class CharacterType(Character):
    display_name = 'Angry'

    _attack = 5
    _health = 15
    _level = 5
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(AngryBuff)
