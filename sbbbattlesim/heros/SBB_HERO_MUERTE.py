import logging

from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero


logger = logging.getLogger(__name__)


class HeroType(Hero):
    display_name = 'Muerte'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False

    def buff(self, target_character):
        if self.triggered:
            return

        class MeurteDoubleLastBreath(OnDeath):
            meurte = self
            priority = -999
            last_breath = False

            def handle(self, stack, *args, **kwargs):
                if self.meurte.triggered:
                    return

                last_breaths = [evt for evt in stack if evt.last_breath]
                if last_breaths:
                    self.meurte.triggered = True
                    with stack.open(*args, **kwargs):
                        stack.execute(last_breaths[-1])

        target_character.register(MeurteDoubleLastBreath)
