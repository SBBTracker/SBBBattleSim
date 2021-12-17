from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe


class BrocLeeOnDamageAndSurvived(OnDamagedAndSurvived):
    def handle(self, stack, *args, **kwargs):
        Buff(reason=ActionReason.BROC_LEE_BUFF, source=self.manager, targets=[self.manager],
             attack=20 if self.manager.golden else 10, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Broc Lee'

    _attack = 0
    _health = 15
    _level = 4
    _tribes = {Tribe.EVIL, Tribe.TREANT}

    deactivated = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(BrocLeeOnDamageAndSurvived)
