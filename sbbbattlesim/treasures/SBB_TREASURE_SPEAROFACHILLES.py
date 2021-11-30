from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Spear of Achilles'
    aura = True

    _level = 6

    def buff(self, target_character, *args, **kwargs):
        class SpearOfAchillesAttack(OnPreAttack):
            spear = self
            def handle(self, stack, *args, **kwargs):
                for _ in range(1 + bool(self.spear.mimic)):
                    self.manager.change_stats(health=7, attack=7, reason=StatChangeCause.SPEAR_OF_ACHILLES, source=self, temp=False, stack=stack)

        target_character.register(SpearOfAchillesAttack, temp=True)
