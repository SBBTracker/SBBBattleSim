from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnSupport
from sbbbattlesim.heroes import Hero


class PupSupportBuff(OnSupport):
    def handle(self, buffed, support, *args, **kwargs):
        Buff(reason=ActionReason.PUP_BUFF, source=self.source, attack=2, health=1).execute(buffed)


class HeroType(Hero):
    display_name = 'Pup the Magic Dragon'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(reason=ActionReason.PUP_BUFF, source=self, event=PupSupportBuff, priority=56)
