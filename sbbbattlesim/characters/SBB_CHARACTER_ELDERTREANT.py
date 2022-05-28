from sbbbattlesim import utils
from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import Tribe


class HeartWoodOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        stat_change = 4 if self.source.golden else 2
        for pos in utils.get_support_targets(self.source.position,
                                             horn='SBB_TREASURE_BANNEROFCOMMAND' in self.source.player.treasures):
            char = self.source.player.characters[pos]
            if char is not None:
                if Tribe.TREANT in char.tribes:
                    Buff(reason=ActionReason.HEARTWOOD_BUFF, source=self.source, targets=[char],
                         attack=stat_change, health=stat_change, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Heartwood Elder'
    support = True

    _attack = 5
    _health = 7
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(HeartWoodOnStart, priority=100, source=self)
