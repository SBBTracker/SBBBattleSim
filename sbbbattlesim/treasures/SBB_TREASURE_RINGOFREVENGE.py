from sbbbattlesim import utils
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import get_behind_targets, StatChangeCause


class TreasureType(Treasure):
    name = 'Ring of Revenge'
    aura = True

    def buff(self, target_character):

        class RingOfRevengeBuff(OnDeath):
            last_breath = False
            def handle(self, *args, **kwargs):
                for pos in utils.get_behind_targets(self.manager.position):
                    char = self.manager.owner.characters.get(pos)
                    if char:
                       char.change_stats(health=1, attack=1, reason=StatChangeCause.RING_OF_REVENGE, source=self.manager)

        target_character.register(RingOfRevengeBuff, temp=True)
