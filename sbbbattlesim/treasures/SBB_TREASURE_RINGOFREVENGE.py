from sbbbattlesim import utils
from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure


class RingOfRevengeBuff(OnDeath):
    last_breath = False

    def handle(self, stack, reason, *args, **kwargs):
        for pos in utils.get_behind_targets(self.manager.position):
            char = self.manager.player.characters.get(pos)
            if char:
                for _ in range(self.source.mimic + 1):
                    Buff(reason=ActionReason.RING_OF_REVENGE, source=self.source, targets=[char],
                         health=1, attack=1, stack=stack).resolve()


class TreasureType(Treasure):
    name = 'Ring of Revenge'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        stats = 3 * (self.mimic + 1)
        self.aura = Aura(event=RingOfRevengeBuff, source=self, _lambda=lambda char: char.position in (1, 2, 3, 4))
