from sbbbattlesim.events import OnResolveBoard, OnStart, OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Exploding Mittens'
    aura = True

    def buff(self, target_character):
        class ExplodingMittensOnDeath(OnDeath):
            mitten = self
            last_breath = False

            def handle(self, *args, **kwargs):
                for _ in range(bool(self.mitten.mimic) + 1):
                    for char in self.manager.owner.opponent.valid_characters():
                        char.change_stats(damage=1, reason=StatChangeCause.EXPLODING_MITTENS_DAMAGE, source=self.mitten)

        target_character.register(ExplodingMittensOnDeath, temp=True)