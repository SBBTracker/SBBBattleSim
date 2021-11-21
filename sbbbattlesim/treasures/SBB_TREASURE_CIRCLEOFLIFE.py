from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Tree of Life'
    aura = True

    def buff(self, target_character):
        class TreeOfLifeHeal(OnDeath):
            tree = self
            def handle(self, *args, **kwargs):
                for char in self.manager.owner.valid_characters():
                    char.change_stats(heal=self.character.health, temp=False, reason=StatChangeCause.TREE_OF_LIFE, source=self.tree)

        target_character.register(TreeOfLifeHeal, temp=True)
