from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import StatChangeCause


class HeroType(Hero):
    display_name = '''The Fates'''
    aura = True

    def buff(self, target_character, *args, **kwargs):
        if target_character.golden:
            target_character.change_stats(attack=5, health=5, reason=StatChangeCause.FATES_BUFF, source=self, temp=True, *args, **kwargs)
