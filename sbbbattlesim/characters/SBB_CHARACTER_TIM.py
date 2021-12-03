from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSpellCast
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Spell Weaver'
    ranged = True

    _attack = 1
    _health = 3
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class SpellWeaverOnSpell(OnSpellCast):
            weaver = self

            def handle(self, caster, spell, target, stack, *args, **kwargs):
                stat_gain = (2 if self.weaver.golden else 1)
                if not self.weaver.dead:
                    self.weaver.change_stats(
                        attack=stat_gain,
                        reason=StatChangeCause.SPELL_WEAVER,
                        source=self.weaver,
                        stack=stack,
                    )

        self.owner.register(SpellWeaverOnSpell)
