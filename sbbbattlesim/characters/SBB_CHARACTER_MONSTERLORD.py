import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class OniKingOnMonsterAttack(OnPreAttack):
    def handle(self, stack, *args, **kwargs):
        stat_change = 14 if self.source.golden else 7
        Buff(source=self.source, reason=ActionReason.ONIKING_BUFF, targets=[self.manager],
             attack=stat_change, health=stat_change, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Oni Tyrant'
    aura = True

    _attack = 7
    _health = 7
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(source=self, event=OniKingOnMonsterAttack, _lambda=lambda char: Tribe.MONSTER in char.tribes)
