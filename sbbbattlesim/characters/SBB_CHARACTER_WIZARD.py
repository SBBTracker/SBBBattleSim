from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSpellCast
from sbbbattlesim.utils import StatChangeCause, Tribe


class WizardFamiliarOnSpell(OnSpellCast):
    def handle(self, caster, spell, target, stack, *args, **kwargs):
        stat_gain = (2 if self.wizard_familiar.golden else 1)
        if not self.wizard_familiar.dead:
            Buff(reason=StatChangeCause.WIZARDS_FAMILIAR, source=self.wizard_familiar, targets=[self.wizard_familiar],
                 attack=stat_gain, health=stat_gain, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Wizard Familiar'

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.ANIMAL, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(WizardFamiliarOnSpell, wizard_familiar=self)
