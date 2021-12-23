from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Blessing of Athena'
    _level = 4

    def cast(self, target=None, *args):
        Buff(reason=ActionReason.BLESSING_OF_ATHENA, source=self, targets=player.valid_characters(),
             attack=1, health=1, temp=False, *args, **kwargs).resolve()
