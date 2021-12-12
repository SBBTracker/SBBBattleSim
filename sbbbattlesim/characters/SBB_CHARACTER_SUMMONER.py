from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill, OnSpellCast
from sbbbattlesim.utils import Tribe, StatChangeCause


class AonOnSpell(OnSpellCast):
    def handle(self, caster, spell, target, stack, *args, **kwargs):
        stat_gain = (2 if self.aon.golden else 1)
        Buff(reason=StatChangeCause.AON_BUFF, source=self.aon,
             targets=self.aon.player.valid_characters(_lambda=lambda c: Tribe.MAGE in c.tribes),
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
        self.player.register(AonOnSpell, aon=self)
        self.register(AonSlay)
