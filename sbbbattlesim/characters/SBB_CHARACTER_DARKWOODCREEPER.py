from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe


class DarkwoodCreeperOnDamage(OnDamagedAndSurvived):
    def handle(self, stack, *args, **kwargs):
        Buff(
            reason=ActionReason.DARKWOOD_CREEPER_BUFF,
            source=self.source,
            targets=[self.manager],
            attack=2 if self.source.golden else 1,
            stack=stack
        ).resolve()


class CharacterType(Character):
    display_name = 'Darkwood Creeper'
    aura = True

    _attack = 0
    _health = 3
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(reason=ActionReason.AURA_BUFF, source=self, event=DarkwoodCreeperOnDamage, priority=10)
