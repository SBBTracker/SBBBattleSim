from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSpellCast
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Wizard Familiar'

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.ANIMAL, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class WizardFamiliarOnSpell(OnSpellCast):
            wizard_familiar = self
            def handle(self, caster, spell, target, *args, **kwargs):
                self.wizard_familiar.change_stats(
                    attack=1, health=1, reason=StatChangeCause.WIZARDS_FAMILIAR, source=self.wizard_familiar
                )

        self.register(WizardFamiliarOnSpell)
