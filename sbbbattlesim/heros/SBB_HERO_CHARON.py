from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero


class CharonOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        if self.manager._level < 2:
            return

        # This should only proc once per combat
        if self.source.triggered:
            return  # This has already procced
        self.source.triggered = True

        Buff(reason=ActionReason.CHARON_BUFF, source=self.source, targets=[self.manager],
             attack=2, health=1, stack=stack).execute()


class HeroType(Hero):
    display_name = 'Charon'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False
        self.aura = Aura(event=CharonOnDeath, priority=999, source=self)
