from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Tree of Life'
    aura = True

    _level = 5

    def buff(self, target_character, *args, **kwargs):
        class TreeOfLifeHeal(OnDeath):
            tree = self
            last_breath = False
            def handle(self, stack, *args, **kwargs):
                for char in self.manager.owner.valid_characters():
                    char.change_stats(heal=char.health, temp=False, reason=StatChangeCause.TREE_OF_LIFE, source=self.tree, stack=stack)

        target_character.register(TreeOfLifeHeal, temp=True)
