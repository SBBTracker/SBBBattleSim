from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import find_strongest_character, find_weakest_character, Tribe


class RobinWoodOnFightStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        strongest_enemy_char = find_strongest_character(self.source.player.opponent)
        weakest_allied_char = find_weakest_character(self.source.player)

        if strongest_enemy_char:
            Buff(reason=ActionReason.ROBIN_WOOD_DEBUFF, source=self.source, targets=[strongest_enemy_char],
                 attack=-14 if self.source.golden else -7, temp=False, stack=stack).resolve()

        if weakest_allied_char:
            Buff(reason=ActionReason.ROBIN_WOOD_BUFF, source=self.source, targets=[weakest_allied_char],
                 attack=14 if self.source.golden else 7, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Robin Wood'
    ranged = True

    _attack = 7
    _health = 10
    _level = 5
    _tribes = {Tribe.GOOD, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(RobinWoodOnFightStart, priority=50, source=self)
