from sbbbattlesim import utils
from sbbbattlesim.action import Buff
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class RingOfRevengeBuff(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        for pos in utils.get_behind_targets(self.manager.position):
            char = self.manager.owner.characters.get(pos)
            if char:
                for _ in range(self.ring_of_revenge.mimic + 1):
                    Buff(reason=StatChangeCause.RING_OF_REVENGE, source=self.ring_of_revenge, targets=[char],
                         health=1, attack=1,  temp=False, stack=stack).resolve()


class TreasureType(Treasure):
    name = 'Ring of Revenge'
    aura = True

    _level = 3

    def buff(self, target_character, *args, **kwargs):
        if target_character.position in range(1, 5):
            target_character.register(RingOfRevengeBuff, temp=True, ring_of_revenge=self)
