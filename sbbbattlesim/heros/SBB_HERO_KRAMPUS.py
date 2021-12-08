from sbbbattlesim.action import Buff
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


class HeroType(Hero):
    display_name = 'Krampus'
    aura = True

    def buff(self, target_character, *args, **kwargs):
        if Tribe.EVIL in target_character.tribes:
            Buff(reason=StatChangeCause.KRAMPUS_BUFF, source=self, targets=[target_character],
                 attack=1, health=1,  *args, **kwargs).resolve()
