from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPreDefend


class CharacterType(Character):
    display_name = 'Rotten Appletree'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.RottenAppletreeOnPreDefend)

    class RottenAppletreeOnPreDefend(OnPreDefend):
        def handle(self, attack_position, defend_position, *args, **kwargs):
            appled_enemy = self.manager.owner.opponent.characters[defend_position]
            appled_enemy.change_stats(health=1 - appled_enemy.health,
                                      reason=f'{self} applied rotten appletree effect to {appled_enemy} settings it to one health')

