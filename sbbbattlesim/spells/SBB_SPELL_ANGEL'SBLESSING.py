from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import NonTargetedSpell


class SpellType(NonTargetedSpell):
    display_name = 'Blessing of Athena'
    _level = 4

    def cast(self, player, *args, **kwargs):
        Buff(reason=ActionReason.BLESSING_OF_ATHENA, source=self, targets=player.valid_characters(),
             attack=1, health=1, temp=False, *args, **kwargs).resolve()
