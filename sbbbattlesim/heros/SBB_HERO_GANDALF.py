from sbbbattlesim.events import OnSupport
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import StatChangeCause


class PupSupportBuff(OnSupport):
    def handle(self, buffed, support, *args, **kwargs):
        buffed.change_stats(attack=2, health=1, reason=StatChangeCause.PUP_BUFF, source=self.pup)


class HeroType(Hero):
    display_name = 'Pup the Magic Dragon'
    aura = True

    def buff(self, target_character, *args, **kwargs):
        target_character.register(PupSupportBuff, temp=True, pup=self)
