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
                stat_gain = (2 if self.wizard_familiar.golden else 1)
                if not self.wizard_familiar.dead:
                    self.wizard_familiar.change_stats(
                        attack=stat_gain, health=stat_gain, reason=StatChangeCause.WIZARDS_FAMILIAR,
                        source=self.wizard_familiar
                    )

        self.owner.register(WizardFamiliarOnSpell)
