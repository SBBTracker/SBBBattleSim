from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.heroes import Hero


class HeroType(Hero):
    display_name = '''The Fates'''
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(reason=ActionReason.FATES_BUFF, source=self, _lambda=lambda char: char.golden,
                         attack=3, health=3)
