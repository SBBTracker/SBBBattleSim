from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnSupport
from sbbbattlesim.heros import Hero


class PupSupportBuff(OnSupport):
    def handle(self, buffed, support, *args, **kwargs):
        Buff(reason=ActionReason.PUP_BUFF, source=self.pup, targets=[buffed],
             attack=2, health=1).resolve()


class HeroType(Hero):
    display_name = 'Pup the Magic Dragon'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(reason=ActionReason.FATES_BUFF, source=self, _lambda=lambda char: char.golden,
                         event=PupSupportBuff, pup=self)
