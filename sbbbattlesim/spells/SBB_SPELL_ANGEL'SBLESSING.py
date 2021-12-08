from sbbbattlesim.action import Buff
from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(NonTargetedSpell):
    display_name = 'Blessing of Athena'
    _level = 4

    def cast(self, player, *args, **kwargs):
        Buff(reason=StatChangeCause.BLESSING_OF_ATHENA, source=self, targets=player.valid_characters(),
             attack=1, health=1, temp=False, *args, **kwargs).resolve()
