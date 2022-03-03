from sbbbattlesim.action import Buff, Aura, ActionReason, Action
from sbbbattlesim.events import OnDeath
from sbbbattlesim.heroes import Hero
from sbbbattlesim.utils import Tribe


class EvellaAura(OnDeath):
    last_breath = False

    def handle(self, stack, reason, *args, **kwargs):
        self.source.aura[1].update(attack=1)


class HeroType(Hero):
    display_name = 'Evella'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = (
            Aura(event=EvellaAura, source=self, _lambda=lambda char: Tribe.ANIMAL in char.tribes),
            Aura(reason=ActionReason.EVELLA_ANIMAL_BUFF, temp=False, source=self,
                 _lambda=lambda char: Tribe.EVIL in char.tribes),
            Aura(reason=ActionReason.EVELLA_BASE_BUFF, source=self,
                 _lambda=lambda char: Tribe.EVIL in char.tribes, attack=1, )
        )
