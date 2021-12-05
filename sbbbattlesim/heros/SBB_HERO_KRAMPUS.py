from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


class HeroType(Hero):
    display_name = 'Krampus'
    aura = True

    def buff(self, target_character, *args, **kwargs):
        if Tribe.EVIL in target_character.tribes:
            target_character.change_stats(attack=1, health=1, reason=StatChangeCause.KRAMPUS_BUFF, source=self, *args, **kwargs)
