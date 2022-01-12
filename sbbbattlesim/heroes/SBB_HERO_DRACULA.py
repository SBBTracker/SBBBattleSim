from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.heroes import Hero


class SadDraculaOnAttackAndKill(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        Buff(reason=ActionReason.SAD_DRACULA_SLAY, source=self.source, targets=[self.manager],
             attack=2, stack=stack).resolve()


class HeroType(Hero):
    display_name = 'Sad Dracula'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(event=SadDraculaOnAttackAndKill, source=self, _lambda=lambda char: char.position == 1)
