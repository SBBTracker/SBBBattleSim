from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


class HeroType(Hero):
    display_name = 'Evella'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animal_deaths = 0

    def buff(self, target_character):

        if Tribe.ANIMAL in target_character.tribes:
            class EvellaAura(OnDeath):
                evella = self
                last_breath = False
                def handle(self, *args, **kwargs):
                    self.evella.animal_deaths += 1
                    self.manager.owner.resolve_board()

            target_character.register(EvellaAura, temp=True)

        if Tribe.EVIL in target_character.tribes:
            target_character.change_stats(attack=self.animal_deaths, reason=StatChangeCause.EVELLA_BUFF, source=self, temp=True)
