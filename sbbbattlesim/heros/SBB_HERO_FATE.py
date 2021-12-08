from sbbbattlesim.action import Buff
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import StatChangeCause


class HeroType(Hero):
    display_name = '''The Fates'''
    aura = True

    def buff(self, target_character, *args, **kwargs):
        if target_character.golden:
            Buff(reason=StatChangeCause.FATES_BUFF, source=self, targets=[target_character],
                 attack=5, health=5,  temp=True, *args, **kwargs).resolve()
