from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill, OnSpellCast
from sbbbattlesim.utils import Tribe, StatChangeCause


class CharacterType(Character):
    display_name = 'Aon'

    _attack = 6
    _health = 12
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class AonOnSpell(OnSpellCast):
            aon = self

            def handle(self, caster, spell, target, stack, *args, **kwargs):
                stat_gain = (2 if self.aon.golden else 1)
                Buff(reason=StatChangeCause.AON_BUFF, source=self.aon,
                     targets=self.aon.owner.valid_characters(_lambda=lambda c: Tribe.MAGE in c.tribes),
                     attack=stat_gain, stack=stack).resolve()

        self.owner.register(AonOnSpell)
        self.register(self.AonSlay)

    class AonSlay(OnAttackAndKill):
        slay = True
        def handle(self, killed_character, *args, **kwargs):
            # discounts spells
            pass



