from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill


class CharacterType(Character):
    display_name = 'Jormungandr'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.LancelotSlay)

    class JormungandrOnAttackAndKill(OnAttackAndKill):
        def handle(self, killed_character, *args, **kwargs):
            modifier = 40 if self.golden else 20
            self.manager.change_stats(attack=modifier, health=modifier, temp=False, reason=f'{self} slayed an enemy and is growing')