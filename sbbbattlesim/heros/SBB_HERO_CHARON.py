from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import StatChangeCause

class HeroType(Hero):
    display_name = 'Charon'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False

    def buff(self, target_character, *args, **kwargs):

        class CharonOnDeath(OnDeath):
            priority = 999
            last_breath = False
            charon = self

            def handle(self, stack, *args, **kwargs):
                # This should only proc once per combat
                if self.charon.triggered:
                    return  # This has already procced
                self.charon.triggered = True

                self.manager.change_stats(attack=2, health=1, reason=StatChangeCause.CHARON_BUFF, source=self.charon, stack=stack)

        target_character.register(CharonOnDeath)

