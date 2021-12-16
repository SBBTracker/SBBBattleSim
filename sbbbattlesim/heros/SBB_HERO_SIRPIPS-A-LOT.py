from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.heros import Hero


class HeroType(Hero):
    display_name = '''Jack's Giant'''
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = Aura(reason=ActionReason.JACKS_GIANT_BUFF, source=self, health=2,
                              _lambda=lambda char: char.position in (1, 2, 3, 4), )

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
