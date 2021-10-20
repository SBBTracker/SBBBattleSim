from events import SlayEvent
from minion import Minion


class MinionType(Minion):
    name = 'Vain-Pire'

    class VainPireSlay(SlayEvent):
        def __call__(self, **kwargs):
            self.minion.base_attack += 1
            self.minion.base_health += 1

    slay = [
        VainPireSlay
    ]


