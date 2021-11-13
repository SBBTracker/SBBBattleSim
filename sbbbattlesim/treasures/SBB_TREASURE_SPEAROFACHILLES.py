from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Spear of Achilles'

    def buff(self, target_character):
        class SpearOfAchillesAttack(OnPreAttack):
            character = self

            def handle(self, *args, **kwargs):
                self.character.change_stats(health=7, attack=7, reason=StatChangeCause.SPEAR_OF_ACHILLES, SOURCE=self,
                                            temp=True)

        self.register(SpearOfAchillesAttack, temp=True)
