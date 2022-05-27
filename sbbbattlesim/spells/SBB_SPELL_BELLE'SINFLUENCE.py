from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell
from sbbbattlesim.utils import Tribe


class SpellType(Spell):
    display_name = '''Beauty's Influence'''
    _level = 3
    cost = 1
    targeted = True


    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(reason=ActionReason.BEAUTYS_INFLUENCE, source=self, targets=[target],
             health=4, attack=0, temp=False, *args, **kwargs).resolve()

        target.tribes.remove(Tribe.EVIL)
        target.tribes.add(Tribe.GOOD)

    @classmethod
    def filter(cls, char):
        return Tribe.EVIL in char.tribes
