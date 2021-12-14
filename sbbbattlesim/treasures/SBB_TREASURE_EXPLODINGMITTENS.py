from sbbbattlesim.action import Damage, EventAura
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class ExplodingMittensOnDeath(OnDeath):
    last_breath = False

    def handle(self, *args, **kwargs):
        for _ in range(bool(self.mitten.mimic) + 1):
            Damage(damage=1, reason=StatChangeCause.EXPLODING_MITTENS_DAMAGE, source=self.mitten,
                   targets=self.manager.player.opponent.valid_characters()).resolve()


class TreasureType(Treasure):
    display_name = 'Exploding Mittens'
    aura = True

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = EventAura(event=ExplodingMittensOnDeath, source=self, mitten=self)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
