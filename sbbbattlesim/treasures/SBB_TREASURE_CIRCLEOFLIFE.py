from sbbbattlesim.action import Buff
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreeOfLifeHeal(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        for _ in range(self.tree.mimic + 1):
            Buff(reason=StatChangeCause.TREE_OF_LIFE, source=self.tree, targets=self.manager.owner.valid_characters(),
                 heal=-1, temp=False, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = 'Tree of Life'
    aura = True

    _level = 5

    def buff(self, target_character, *args, **kwargs):
        target_character.register(TreeOfLifeHeal, temp=True, tree=self)
