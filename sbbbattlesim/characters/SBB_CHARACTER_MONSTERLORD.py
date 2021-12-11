import logging

from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import Tribe, StatChangeCause

logger = logging.getLogger(__name__)


class OniKingOnMonsterAttack(OnPreAttack):
    def handle(self, stack, *args, **kwargs):
        stat_change = 20 if self.oni_king.golden else 10
        with Buff(source=self.oni_king, reason=StatChangeCause.ONIKING_BUFF, targets=[self.manager],
                  attack=stat_change, health=stat_change, temp=False, stack=stack):
            pass

class CharacterType(Character):
    display_name = 'Oni King'
    aura = True

    _attack = 13
    _health = 13
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def buff(self, target_character, *args, **kwargs):
        if Tribe.MONSTER in target_character.tribes:
            target_character.register(OniKingOnMonsterAttack, oni_king=self)
