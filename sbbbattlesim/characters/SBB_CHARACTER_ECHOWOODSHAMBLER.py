import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class EchoWoodBuff(OnBuff):
    def handle(self, stack, attack, health, reason=None, on_init=False, *args, **kwargs):
        if not on_init and not self.manager.dead and reason != ActionReason.ECHOWOOD_BUFF:
            gold_multiplier = 2 if self.source.golden else 1
            attack_change = max(0, gold_multiplier * attack)
            health_change = max(0, gold_multiplier * health)

            if attack_change > 0 or health_change > 0:
                Buff(reason=ActionReason.ECHOWOOD_BUFF, source=self.source, attack=attack_change,
                     health=health_change).execute(self.source)


class CharacterType(Character):
    display_name = 'Echowood Dryad'
    aura = True

    _attack = 1
    _health = 1
    _level = 6
    _tribes = {Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(source=self, event=EchoWoodBuff, _lambda=lambda char: char is not self, priority=9999)
