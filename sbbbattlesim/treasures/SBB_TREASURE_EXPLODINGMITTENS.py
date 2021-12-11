from sbbbattlesim.action import Damage
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class ExplodingMittensOnDeath(OnDeath):
    last_breath = False

    def handle(self, *args, **kwargs):
        for _ in range(bool(self.mitten.mimic) + 1):
            Damage(damage=1, reason=StatChangeCause.EXPLODING_MITTENS_DAMAGE, source=self.mitten,
                   targets=self.manager.owner.opponent.valid_characters()).resolve()


class TreasureType(Treasure):
    display_name = 'Exploding Mittens'
    aura = True

    _level = 5

    def buff(self, target_character, *args, **kwargs):
        target_character.register(ExplodingMittensOnDeath, temp=True, mitten=self)
