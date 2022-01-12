from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.heroes import Hero


class HeroType(Hero):
    display_name = '''Jack's Giant'''
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(reason=ActionReason.JACKS_GIANT_BUFF, source=self, health=2,
                         _lambda=lambda char: char.position in (1, 2, 3, 4), )
