import logging

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff, OnDeath
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)

# this probably doesn't work with Riverwish Mermaid and that is not my problem
# TODO make reggie fix this
class PrincessPeaOnBuff(OnBuff):
    def handle(self, reason, stack, attack, health, *args, **kwargs):
        if reason not in [ActionReason.SUPPORT_BUFF]:
            return
        golden_multiplier = 2 if self.source.golden else 1
        Buff(reason=ActionReason.PRINCESS_PEA_SELFBUFF, source=self.source, targets=[self.source],
             attack=attack * golden_multiplier, health=health * golden_multiplier, stack=stack).resolve()

class PrincessPeaLastBreath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        chars = {action.source for action in self.manager._action_history if action.reason == ActionReason.SUPPORT_BUFF}
        if not chars:
            return

        Buff(reason=ActionReason.PRINCESS_PEA_BUFF, source=self.manager, targets=[*chars],
             attack=self.manager.attack, health=self.manager.max_health,
             stack=stack).execute()


class CharacterType(Character):
    display_name = 'Princess Pea'
    last_breath = True

    _attack = 10
    _health = 10
    _level = 6
    _tribes = {Tribe.ROYAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(PrincessPeaOnBuff, priority=9999)
        self.register(PrincessPeaLastBreath)