from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import Spell
from sbbbattlesim.utils import Tribe


class SpellType(Spell):
    display_name = '''Witch's Brew'''
    _level = 2
    cost = 1
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        Buff(health=1, attack=1, temp=False, reason=ActionReason.WITCHS_BREW, source=self, *args, **kwargs)

    @classmethod
    def filter(cls, char):
        return Tribe.EVIL in char.tribes
