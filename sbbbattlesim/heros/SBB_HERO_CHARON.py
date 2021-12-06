from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import StatChangeCause


class CharonOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        # This should only proc once per combat
        if self.charon.triggered:
            return  # This has already procced
        self.charon.triggered = True

        self.manager.change_stats(attack=2, health=1, reason=StatChangeCause.CHARON_BUFF, source=self.charon,
                                  stack=stack)


class HeroType(Hero):
    display_name = 'Charon'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False

    def buff(self, target_character, *args, **kwargs):
        target_character.register(CharonOnDeath, priority=999, charon=self)
