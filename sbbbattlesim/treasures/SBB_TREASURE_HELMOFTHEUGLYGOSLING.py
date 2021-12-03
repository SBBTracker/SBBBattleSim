from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Helm of the Ugly Gosling'

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class HelmOfTheUglyGoslingBeansOnStartBuff(OnStart):
            priority=50
            gosling = self

            def handle(self, stack, *args, **kwargs):
                for _ in range(bool(self.gosling.mimic) + 1):
                    weakest = sorted(self.manager.valid_characters(), key=lambda char: char.attack)[0]
                    weakest.change_stats(attack=15, health=15, reason=StatChangeCause.HELM_OF_THE_UGLY_GOSLING, source=self.gosling, temp=False, stack=stack)

        self.player.register(HelmOfTheUglyGoslingBeansOnStartBuff)
