from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Tree of Life'

    def buff(self, target_character):
        class TreeOfLifeHeal(OnDeath):
            character = self

            def handle(self, *args, **kwargs):
                self.character.change_stats(health=self.character.maxHealth, temp=True,
                                            reason=StatChangeCause.TREE_OF_LIFE,
                                            source=self)

        target_character.register(TreeOfLifeHeal, temp=True)
