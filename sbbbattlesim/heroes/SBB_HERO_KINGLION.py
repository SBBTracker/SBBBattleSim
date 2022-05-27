from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.heroes import Hero
from sbbbattlesim.utils import Tribe


class HeroType(Hero):
    display_name = 'Mihri, King Lion'
    aura = True

    def __init__(self, mihri_buff=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mihri_buff = int(mihri_buff)
        self.aura = Aura(reason=ActionReason.MIHRI_BUFF, source=self,
                         _lambda=lambda char: Tribe.ROYAL in char.tribes or Tribe.ROYAL in char.tribes,
                         attack=1 * self.mihri_buff, health=2 * self.mihri_buff, )
