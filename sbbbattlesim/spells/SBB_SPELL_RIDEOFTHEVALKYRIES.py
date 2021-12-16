from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import NonTargetedSpell


class SpellType(NonTargetedSpell):
    display_name = 'Ride of the Valkyries'
    _level = 4

    def cast(self, player, *args, **kwargs):
        Buff(reason=ActionReason.RIDE_OF_THE_VALKYRIES, source=self, targets=player.valid_characters(),
             attack=3, temp=False, *args, **kwargs).resolve()
