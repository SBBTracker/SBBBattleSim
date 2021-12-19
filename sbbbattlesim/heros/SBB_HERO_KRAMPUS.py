from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe


class HeroType(Hero):
    display_name = 'Krampus'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(reason=ActionReason.KRAMPUS_BUFF, source=self, _lambda=lambda char: Tribe.EVIL in char.tribes,
                         attack=1, health=1)
