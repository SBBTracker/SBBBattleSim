from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPreDefend
from sbbbattlesim.utils import StatChangeCause, Tribe


class RottenAppletreeOnPreDefend(OnPreDefend):
    def handle(self, attack_position, defend_position, attack_player, stack, *args, **kwargs):
        appled_enemy = attack_player.characters[attack_position]
        if appled_enemy:
            with Buff(reason=StatChangeCause.ROTTEN_APPLE_TREE_HEALTH, source=self.manager, targets=[appled_enemy],
                      health=1 - appled_enemy.health, stack=stack, temp=False):
                pass


class CharacterType(Character):
    display_name = 'Rotten Appletree'

    _attack = 0
    _health = 18
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(RottenAppletreeOnPreDefend)
