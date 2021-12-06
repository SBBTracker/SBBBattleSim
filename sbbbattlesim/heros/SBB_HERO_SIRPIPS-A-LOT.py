from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import StatChangeCause


class HeroType(Hero):
    display_name = '''Jack's Giant'''
    aura = True

    def buff(self, target_character, *args, **kwargs):
        if target_character.position in (1, 2, 3, 4):
            target_character.change_stats(health=2, reason=StatChangeCause.JACKS_GIANT_BUFF, source=self, *args,
                                          **kwargs)
