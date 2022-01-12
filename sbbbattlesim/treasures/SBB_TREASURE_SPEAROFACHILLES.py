from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.treasures import Treasure


class SpearOfAchillesAttack(OnPreAttack):
    def handle(self, stack, *args, **kwargs):
        for _ in range(1 + bool(self.source.mimic)):
            Buff(reason=ActionReason.SPEAR_OF_ACHILLES, source=self.source, targets=[self.manager],
                 health=7, attack=7, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = 'Spear of Achilles'
    aura = True

    _level = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(event=SpearOfAchillesAttack, source=self)
