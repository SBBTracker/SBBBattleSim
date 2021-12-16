from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure


class HelmOfTheUglyGoslingOnStartBuff(OnStart):
    priority = 50

    def handle(self, stack, *args, **kwargs):
        for _ in range(bool(self.gosling.mimic) + 1):
            weakest = sorted(self.gosling.player.valid_characters(), key=lambda char: char.attack)[0]
            Buff(reason=ActionReason.HELM_OF_THE_UGLY_GOSLING, source=self.gosling, targets=[weakest],
                 attack=15, health=15, temp=False, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = 'Helm of the Ugly Gosling'

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.board.register(HelmOfTheUglyGoslingOnStartBuff, gosling=self, priority=50)
