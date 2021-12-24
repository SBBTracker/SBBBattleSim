from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSummon, OnStart, OnSpawn
from sbbbattlesim.utils import Tribe


class CraftyOnSpawn(OnSpawn):
    def handle(self, stack, *args, **kwargs):
        already_buffed = next((True for action in self.source._action_history if action.reason == ActionReason.CRAFTY_BUFF), False)
        if already_buffed:
            return

        buff = 2 * len(self.source.player.treasures) * (2 if self.source.golden else 1)
        Buff(reason=ActionReason.CRAFTY_BUFF, source=self.source, attack=buff, health=buff, *args, **kwargs).execute(self.source)


class CharacterType(Character):
    display_name = 'Crafty'

    aura = True

    _attack = 2
    _health = 2
    _level = 2
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(CraftyOnSpawn)
