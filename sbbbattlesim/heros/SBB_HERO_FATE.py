from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.heros import Hero


class HeroType(Hero):
    display_name = '''The Fates'''
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = Aura(reason=ActionReason.FATES_BUFF, source=self, _lambda=lambda char: char.golden,
                              attack=5, health=5)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
