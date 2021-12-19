from sbbbattlesim.action import Buff, Aura, DynamicStat, ActionReason, Action
from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe


class EvellaAura(OnDeath):
    last_breath = False

    def handle(self, *args, **kwargs):
        self.source.aura[1].update(attack=1)


class HeroType(Hero):
    display_name = 'Evella'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = (
            Aura(event=EvellaAura, source=self, _lambda=lambda char: Tribe.ANIMAL in char.tribes),
            Aura(reason=ActionReason.EVELLA_BUFF, source=self, _lambda=lambda char: Tribe.EVIL in char.tribes)
        )
