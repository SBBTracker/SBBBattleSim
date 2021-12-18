from sbbbattlesim.action import Buff, Aura, DynamicStat, ActionReason
from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe


class EvellaAura(OnDeath):
    last_breath = False

    def handle(self, *args, **kwargs):
        self.evella.animal_deaths += 1


class HeroType(Hero):
    display_name = 'Evella'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animal_deaths = DynamicStat(0)
        self.aura_buff = (
            Aura(event=EvellaAura, evella=self, _lambda=lambda char: Tribe.ANIMAL in char.tribes),
            Aura(reason=ActionReason.EVELLA_BUFF, source=self, attack=self.animal_deaths,
                 _lambda=lambda char: Tribe.EVIL in char.tribes)
        )

    def buff(self, target_character, *args, **kwargs):
        for aura in self.aura_buff:
            aura.execute(target_character)