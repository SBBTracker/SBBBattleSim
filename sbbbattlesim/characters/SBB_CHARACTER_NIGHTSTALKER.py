from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Vain-Pire'
    slay = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class VainPireSlay(OnAttackAndKill):
            slay = True

            def handle(self, killed_character, *args, **kwargs):
                stat_buff = 2 if self.manager.golden else 1
                self.manager.change_stats(attack=stat_buff, health=stat_buff, temp=False, reason=StatChangeCause.SLAY,
                                          source=self.manager)

        self.register(VainPireSlay)


