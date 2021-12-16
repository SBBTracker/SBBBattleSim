import logging

from sbbbattlesim.action import Aura
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


class MuerteAuraBuff(Aura):
    def execute(self, character):
        character.register(MeurteDoubleLastBreath, meurte=self.source, priority=999)


class HeroType(Hero):
    display_name = 'Muerte'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False
        self.aura_buff = MuerteAuraBuff(event=MeurteDoubleLastBreath, source=self, priority=999, meurte=self,
                                        _lambda=lambda char: not self.triggered)

    def buff(self, target_character, *args, **kwargs):
        if self.triggered:
            return
        self.aura_buff.execute(target_character)
