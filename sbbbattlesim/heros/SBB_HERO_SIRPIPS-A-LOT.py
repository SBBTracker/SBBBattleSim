from sbbbattlesim.action import Buff
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import StatChangeCause


class HeroType(Hero):
    display_name = '''Jack's Giant'''
    aura = True

    def buff(self, target_character, *args, **kwargs):
        if target_character.position in (1, 2, 3, 4):
            Buff(reason=StatChangeCause.JACKS_GIANT_BUFF, source=self, targets=[target_character],
                 health=2, temp=True, *args, **kwargs).resolve()
