from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill, OnSpellCast
from sbbbattlesim.utils import Tribe


class AonOnSpell(OnSpellCast):
    def handle(self, caster, spell, target, stack, *args, **kwargs):
        stat_gain = (2 if self.source.golden else 1)
        Buff(reason=ActionReason.AON_BUFF, source=self.source,
             targets=self.source.player.valid_characters(_lambda=lambda c: Tribe.MAGE in c.tribes),
             attack=stat_gain, stack=stack).resolve()


class AonSlay(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, *args, **kwargs):
        # discounts spells
        pass


class CharacterType(Character):
    display_name = 'Aon'

    _attack = 6
    _health = 12
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(AonOnSpell, source=self)
        self.register(AonSlay)
