from sbbbattlesim.damage import Damage
from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(NonTargetedSpell):
    display_name = 'Falling Stars'
    _level = 2

    def cast(self, player, *args, **kwargs):
        Damage(
            1,
            reason=StatChangeCause.FALLING_STARS,
            source=self,
            targets=player.valid_characters() + player.opponent.valid_characters()
        ).resolve()
