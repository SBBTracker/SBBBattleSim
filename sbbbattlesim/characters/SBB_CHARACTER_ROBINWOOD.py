from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import find_strongest_character, find_weakest_character, Tribe


class RobinWoodOnFightStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        strongest_enemy_char = find_strongest_character(self.robin_wood.player.opponent)
        weakest_allied_char = find_weakest_character(self.robin_wood.player)

        if strongest_enemy_char:
            Buff(reason=ActionReason.ROBIN_WOOD_DEBUFF, source=self.robin_wood, targets=[strongest_enemy_char],
                 attack=-30 if self.robin_wood.golden else -15, temp=False, stack=stack).resolve()

        if weakest_allied_char:
            Buff(reason=ActionReason.ROBIN_WOOD_BUFF, source=self.robin_wood, targets=[weakest_allied_char],
                 attack=30 if self.robin_wood.golden else 15, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Robin Wood'

    _attack = 7
    _health = 10
    _level = 6
    _tribes = {Tribe.GOOD, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.board.register(RobinWoodOnFightStart, priority=50, robin_wood=self)
