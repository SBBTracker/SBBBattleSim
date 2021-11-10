from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


class HeroType(Hero):
    display_name = 'Mrs. Claus'
    aura = True

    def buff(self, target_character):
        if Tribe.GOOD in target_character.tribes:
            target_character.change_stats(attack=1, health=1, reason=StatChangeCause.MRS_CLAUS_BUFF, source=self)
