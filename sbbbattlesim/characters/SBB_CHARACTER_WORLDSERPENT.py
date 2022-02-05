from sbbbattlesim.action import Aura, Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill, OnSlay
from sbbbattlesim.utils import Tribe


class JormungandrOnAttackAndKill(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        modifier = 40 if self.manager.golden else 20
        Buff(reason=ActionReason.SLAY, source=self.manager, targets=[self.manager],
             attack=modifier, health=modifier, temp=False, stack=stack).resolve()


class JormungandrOnSlay(OnSlay):
    def handle(self, source, stack, *args, **kwargs):
        if source.source is not self.source:
            modifier = 40 if self.source.golden else 20
            Buff(reason=ActionReason.JORM_ON_SLAY_BUFF, source=self.source, targets=[self.source],
                 attack=modifier, health=modifier, stack=stack, *args, **kwargs).resolve()


class CharacterType(Character):
    display_name = 'Jormungandr'
    aura = True

    _attack = 20
    _health = 20
    _level = 6
    _tribes = {Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(JormungandrOnAttackAndKill)
        self.aura = Aura(source=self, event=JormungandrOnSlay)
