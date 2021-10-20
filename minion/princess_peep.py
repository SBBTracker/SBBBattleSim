from events import LastBreathEvent
from minion import Minion
from minion import registry as minion_registry

class MinionType(Minion):
    name = 'Princess Peep'

    class PrincessPeepDeath(LastBreathEvent):
        def __call__(self, **kwargs):
            self.minion.owner.summon(self.minion.position, *[minion_registry['Sheep'](1, 1) for _ in range(3)])

    death = [
        PrincessPeepDeath,
    ]
