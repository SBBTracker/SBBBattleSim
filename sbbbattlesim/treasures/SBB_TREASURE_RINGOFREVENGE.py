from sbbbattlesim import utils
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import get_behind_targets, StatChangeCause


class TreasureType(Treasure):
    name = 'Ring of Revenge'
    aura = True

    _level = 3

    def buff(self, target_character):
        if target_character.position in range(1, 5):

            class RingOfRevengeBuff(OnDeath):
                last_breath = False
                ring_of_revenge = self

                def handle(self, *args, **kwargs):
                    for pos in utils.get_behind_targets(self.manager.position):
                        char = self.manager.owner.characters.get(pos)
                        if char:
                            for _ in range(self.ring_of_revenge.mimic + 1):
                                char.change_stats(health=1, attack=1, reason=StatChangeCause.RING_OF_REVENGE, source=self.ring_of_revenge)

            target_character.register(RingOfRevengeBuff, temp=True)
