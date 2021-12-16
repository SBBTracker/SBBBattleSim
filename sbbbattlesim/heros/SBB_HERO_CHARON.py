from sbbbattlesim.action import Aura, Aura, ActionReason
from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero


class CharonOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        if self.manager._level < 2:
            return

        # This should only proc once per combat
        if self.charon.triggered:
            return  # This has already procced
        self.charon.triggered = True

        Buff(reason=ActionReason.CHARON_BUFF, source=self.charon, targets=[self.manager],
             attack=2, health=1, stack=stack).execute()



class HeroType(Hero):
    display_name = 'Charon'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False
        self.aura_buff = Aura(event=CharonOnDeath, priority=999, charon=self)

    def buff(self, target_character, *args, **kwargs):
        target_character.register(CharonOnDeath, priority=999, charon=self)
