from sbbbattlesim.action import Damage, ActionReason
from sbbbattlesim.spells import NonTargetedSpell


class SpellType(NonTargetedSpell):
    display_name = 'Falling Stars'
    _level = 2

    def cast(self, player, *args, **kwargs):
        Damage(damage=1, reason=ActionReason.FALLING_STARS, source=self,
               targets=player.valid_characters() + player.opponent.valid_characters()).resolve()
