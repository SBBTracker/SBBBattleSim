import logging

from sbbbattlesim.events import OnLastBreath
from sbbbattlesim.heros import Hero

logger = logging.getLogger(__name__)


class MeurteDoubleLastBreath(OnLastBreath):
    last_breath = False

    def handle(self, source, stack, *args, **kwargs):
        if self.meurte.triggered:
            return

        last_breaths = [evt for evt in stack if getattr(evt, 'last_breath', False)]
        if last_breaths:
            self.meurte.triggered = True
            with stack.open(*args, **kwargs) as executor:
                executor.execute(last_breaths[-1])


class HeroType(Hero):
    display_name = 'Muerte'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False

    def buff(self, target_character, *args, **kwargs):
        if self.triggered:
            return
        target_character.register(MeurteDoubleLastBreath, meurte=self, priority=999)
