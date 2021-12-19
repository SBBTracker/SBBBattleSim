from sbbbattlesim.action import Buff, Aura, DynamicStat, ActionReason, Action
from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe


class EvellaAura(OnDeath):
    last_breath = False

    def handle(self, *args, **kwargs):
        targets = self.source.player.valid_characters(_lambda=lambda char: Tribe.EVIL in char.tribes)
        Buff(reason=ActionReason.EVELLA_BUFF, source=self.source, attack=1, targets=targets).resolve()


class HeroType(Hero):
    display_name = 'Evella'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(event=EvellaAura, source=self, _lambda=lambda char: Tribe.ANIMAL in char.tribes),
