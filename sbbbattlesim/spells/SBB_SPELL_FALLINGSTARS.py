from sbbbattlesim.action import Damage, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Falling Stars'
    _level = 2
    cost = 0

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Damage(damage=1, reason=ActionReason.FALLING_STARS, source=self,
               targets=self.player.valid_characters() + self.player.opponent.valid_characters()).resolve()
