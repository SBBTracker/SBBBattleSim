from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.treasures import Treasure


class SpearOfAchillesAttack(OnPreAttack):
    def handle(self, stack, *args, **kwargs):
        for _ in range(1 + bool(self.spear.mimic)):
            Buff(reason=ActionReason.SPEAR_OF_ACHILLES, source=self.spear, targets=[self.manager],
                 health=7, attack=7, temp=False, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = 'Spear of Achilles'
    aura = True

    _level = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feather_used = False
        stats = 4 * (bool(self.mimic) + 1)
        self.aura_buff = Aura(event=SpearOfAchillesAttack, source=self, spear=self)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
