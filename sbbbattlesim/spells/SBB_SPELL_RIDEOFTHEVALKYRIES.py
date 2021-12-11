from sbbbattlesim.action import Buff
from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(NonTargetedSpell):
    display_name = 'Ride of the Valkyries'
    _level = 4

    def cast(self, player, *args, **kwargs):
        Buff(reason=StatChangeCause.RIDE_OF_THE_VALKYRIES, source=self, targets=player.valid_characters(),
             attack=3, temp=False, *args, **kwargs).resolve()
