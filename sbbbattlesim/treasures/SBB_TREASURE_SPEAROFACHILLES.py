from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class SpearOfAchillesAttack(OnPreAttack):
    def handle(self, stack, *args, **kwargs):
        for _ in range(1 + bool(self.spear.mimic)):
            self.manager.change_stats(health=7, attack=7, reason=StatChangeCause.SPEAR_OF_ACHILLES, source=self,
                                      temp=False, stack=stack)


class TreasureType(Treasure):
    display_name = 'Spear of Achilles'
    aura = True

    _level = 6

    def buff(self, target_character, *args, **kwargs):
        target_character.register(SpearOfAchillesAttack, temp=True, spear=self)
