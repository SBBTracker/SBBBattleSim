from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Blessing of Athena'
    _level = 4
    cost = 3

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(reason=ActionReason.BLESSING_OF_ATHENA, source=self, attack=1, health=1, temp=False,
             *args, **kwargs).execute(*self.player.valid_characters()).resolve()
