from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Ride of the Valkyries'
    _level = 4
    cost = 2

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(reason=ActionReason.RIDE_OF_THE_VALKYRIES, source=self, targets=self.player.valid_characters(),
             attack=3, temp=False, *args, **kwargs).resolve()
