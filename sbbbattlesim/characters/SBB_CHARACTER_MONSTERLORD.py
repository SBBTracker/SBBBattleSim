import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class OniKingOnMonsterAttack(OnPreAttack):
    def handle(self, stack, *args, **kwargs):
        stat_change = 20 if self.source.golden else 10
        Buff(source=self.source, reason=ActionReason.ONIKING_BUFF, targets=[self.manager],
             attack=stat_change, health=stat_change, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Oni Tyrant'
    aura = True

    _attack = 13
    _health = 13
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(source=self, event=OniKingOnMonsterAttack, _lambda=lambda char: Tribe.MONSTER in char.tribes)
