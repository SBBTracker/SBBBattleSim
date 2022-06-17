from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe


class VainPireSlay(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        stat_buff = 2 if self.manager.golden else 1
        Buff(reason=ActionReason.VAINPIRE_SLAY, source=self.manager, targets=[self.manager],
             attack=stat_buff, health=stat_buff, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Vain-Pire'

    _attack = 4
    _health = 4
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(VainPireSlay)
