from events import LastBreathEvent
from minion import Minion
from minion import registry as minion_registry


class MinionType(Minion):
    name = 'Black Cat'

    class BlackCatDeath(LastBreathEvent):
        def __call__(self, **kwargs):
            self.minion.owner.summon(self.minion.position, minion_registry['Cat'](1, 1))

    death = [
        BlackCatDeath,
    ]
