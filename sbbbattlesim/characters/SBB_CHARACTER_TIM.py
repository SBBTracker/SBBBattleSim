from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSpellCast
from sbbbattlesim.utils import Tribe


class SpellWeaverOnSpell(OnSpellCast):
    def handle(self, caster, spell, target, stack, *args, **kwargs):
        stat_gain = (2 if self.source.golden else 1)
        if not self.source.dead:
            Buff(reason=ActionReason.SPELL_WEAVER, source=self.source, targets=[self.source],
                 attack=stat_gain, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Spell Weaver'
    ranged = True

    _attack = 1
    _health = 3
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(SpellWeaverOnSpell, source=self)
