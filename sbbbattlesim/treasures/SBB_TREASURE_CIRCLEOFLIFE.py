from sbbbattlesim.action import Aura, Heal, ActionReason
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure


class TreeOfLifeHeal(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        for _ in range(self.tree.mimic + 1):
            Heal(reason=ActionReason.TREE_OF_LIFE, source=self.tree, targets=self.manager.player.valid_characters(),
                 heal=-1, temp=False, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = 'Tree of Life'
    aura = True

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 2 * (self.mimic + 1)
        self.aura_buff = Aura(event=TreeOfLifeHeal, source=self, tree=self)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
