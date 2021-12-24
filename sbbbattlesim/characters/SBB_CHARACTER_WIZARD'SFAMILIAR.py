from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSpellCast
from sbbbattlesim.utils import Tribe


class WizardFamiliarOnSpell(OnSpellCast):
    def handle(self, caster, spell, target, stack, *args, **kwargs):
        stat_gain = (2 if self.source.golden else 1)
        if not self.source.dead:
            Buff(reason=ActionReason.WIZARDS_FAMILIAR, source=self.source, targets=[self.source],
                 attack=stat_gain, health=stat_gain, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Wizard Familiar'

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.ANIMAL, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(WizardFamiliarOnSpell, source=self)
