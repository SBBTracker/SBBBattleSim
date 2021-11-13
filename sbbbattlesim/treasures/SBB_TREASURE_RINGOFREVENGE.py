from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import get_behind_targets, StatChangeCause


class TreasureType(Treasure):
    name = 'Ring of Revenge'

    # TODO implement this
    def buff(self, target_character):
        class RingOfRevengeBuff(OnDeath):
            dead_character = self

            def handle(self, *args, **kwargs):
                targets = self.dead_character.get_behind_targets()
                for char in self.manager.owner.valid_characters():
                    if char.position in targets:
                        char.changestats(health=1, attack=1, reason=StatChangeCause.RING_OF_REVENGE,
                                         source=self.dead_character)
        target_character.register(RingOfRevengeBuff, temp=True)