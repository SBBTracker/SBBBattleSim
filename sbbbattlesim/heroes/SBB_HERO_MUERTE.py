import logging

from sbbbattlesim.action import Aura, ActionReason
from sbbbattlesim.events import OnLastBreath
from sbbbattlesim.heroes import Hero

logger = logging.getLogger(__name__)


class MeurteDoubleLastBreath(OnLastBreath):
    def handle(self, source, stack, *args, **kwargs):
        if self.source.triggered:
            return

        last_breaths = [e for e in self.manager.get('OnDeath') if e.last_breath]
        if last_breaths:
            self.source.triggered = True
            with stack.open(*args, **kwargs) as executor:
                kwargs = kwargs | dict(reason=ActionReason.MEURTE_PROC)
                executor.execute(last_breaths[-1], *args, **kwargs)


class HeroType(Hero):
    display_name = 'Muerte'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False
        self.aura = Aura(event=MeurteDoubleLastBreath, source=self, priority=999, _lambda=lambda char: char.last_breath)
