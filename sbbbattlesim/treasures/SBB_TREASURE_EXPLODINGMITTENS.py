from sbbbattlesim.action import Damage, Aura, ActionReason
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure


class ExplodingMittensOnDeath(OnDeath):
    last_breath = False

    def handle(self, *args, **kwargs):
        for _ in range(bool(self.source.mimic) + 1):
            Damage(damage=1, reason=ActionReason.EXPLODING_MITTENS_DAMAGE, source=self.source,
                   targets=self.manager.player.opponent.valid_characters()).resolve()


class TreasureType(Treasure):
    display_name = 'Exploding Mittens'
    aura = True

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(event=ExplodingMittensOnDeath, source=self)
