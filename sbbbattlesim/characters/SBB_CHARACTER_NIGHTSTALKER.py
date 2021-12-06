from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import StatChangeCause, Tribe


class VainPireSlay(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        stat_buff = 2 if self.manager.golden else 1
        self.manager.change_stats(
            attack=stat_buff,
            health=stat_buff,
            temp=False,
            reason=StatChangeCause.SLAY,
            source=self.manager,
            stack=stack
        )


class CharacterType(Character):
    display_name = 'Vain-Pire'

    _attack = 4
    _health = 4
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(VainPireSlay)
