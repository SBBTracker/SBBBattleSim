from sbbbattlesim.events import OnDeath, OnSupport
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


class HeroType(Hero):
    display_name = 'Pup the Magic Dragon'
    aura = True

    def buff(self, target_character, *args, **kwargs):
        class PupSupportBuff(OnSupport):
            pup = self
            def handle(self, buffed, support, *args, **kwargs):
                buffed.change_stats(attack=2, health=1, reason=StatChangeCause.PUP_BUFF, source=self.pup)

        target_character.register(PupSupportBuff, temp=True)
