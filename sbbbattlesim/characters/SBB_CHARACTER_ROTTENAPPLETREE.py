from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPreDefend
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Rotten Appletree'

    _attack = 0
    _health = 18
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.RottenAppletreeOnPreDefend)

    class RottenAppletreeOnPreDefend(OnPreDefend):
        def handle(self, attack_position, defend_position, *args, **kwargs):
            appled_enemy = self.manager.owner.opponent.characters[defend_position]
            appled_enemy.change_stats(
                health=1 - appled_enemy.health,
                reason=StatChangeCause.ROTTEN_APPLE_TREE_HEALTH,
                source=self.manager
            )

