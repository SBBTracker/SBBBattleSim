from sbbbattlesim import utils
from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import StatChangeCause, Tribe


class HeartWoodOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        stat_change = 4 if self.heartwood.golden else 2
        for pos in utils.get_support_targets(self.heartwood.position,
                                             horn='SBB_TREASURE_BANNEROFCOMMAND' in self.heartwood.player.treasures):
            char = self.heartwood.player.characters[pos]
            if char is not None:
                if Tribe.TREANT in char.tribes:
                    Buff(reason=StatChangeCause.HEARTWOOD_BUFF, source=self.heartwood, targets=[char],
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
        self.player.board.register(HeartWoodOnStart, priority=100, heartwood=self)

    def buff(self, target_character, *args, **kwargs):
        pass
