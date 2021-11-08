from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill


class CharacterType(Character):
    display_name = 'Vain-Pire'
    slay = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.VainPireSlay)

    class VainPireSlay(OnAttackAndKill):
        slay = True
        def handle(self, killed_character, *args, **kwargs):
            stat_buff = 2 if self.character.golden else 1
            self.manager.change_stats(attack=stat_buff, health=stat_buff, temp=False, reason=f'{self} slay trigger')
