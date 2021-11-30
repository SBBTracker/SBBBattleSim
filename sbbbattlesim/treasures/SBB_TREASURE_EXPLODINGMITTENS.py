from sbbbattlesim.damage import Damage
from sbbbattlesim.events import OnResolveBoard, OnStart, OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Exploding Mittens'
    aura = True

    _level = 5

    def buff(self, target_character, *args, **kwargs):
        class ExplodingMittensOnDeath(OnDeath):
            mitten = self
            last_breath = False

            def handle(self, *args, **kwargs):
                for _ in range(bool(self.mitten.mimic) + 1):
                    Damage(1, reason=StatChangeCause.EXPLODING_MITTENS_DAMAGE, source=self.mitten,
                           targets=self.manager.owner.opponent.valid_characters()).resolve()

        target_character.register(ExplodingMittensOnDeath, temp=True)