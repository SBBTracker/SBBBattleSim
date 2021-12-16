from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe


class HeroType(Hero):
    display_name = 'Mrs. Claus'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = Aura(reason=ActionReason.MRS_CLAUS_BUFF, source=self,
                              _lambda=lambda char: Tribe.GOOD in char.tribes,
                              attack=1, health=1, )

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
