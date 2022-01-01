from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe


class HeroType(Hero):
    display_name = 'Mirhi, King Lion'
    aura = True

    def __init__(self, mirhi_buff=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mirhi_buff = mirhi_buff
        self.aura = Aura(reason=ActionReason.MIRHI_BUFF, source=self,
                         _lambda=lambda char: Tribe.PRINCE in char.tribes or Tribe.PRINCESS in char.tribes,
                         attack=1 * self.mirhi_buff, health=2 * self.mirhi_buff, )
