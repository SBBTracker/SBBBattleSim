from sbbbattlesim.events import OnAttackAndKill, OnSpawn

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import Tribe


def _throne_tribe_add(char: Character):
    if Tribe.ROYAL in char.tribes:
        char.tribes.add(Tribe.MONSTER)

class CursedThroneOnAttackAndKill(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        stats = 2 if self.source.mimic else 1
        Buff(reason=ActionReason.AURA_BUFF, source=self.source, targets=[self.manager], attack=stats,
             health=stats,
             stack=stack).resolve()

class CursedThroneOnSpawn(OnSpawn):
    def handle(self, stack, *args, **kwargs):
        player = self
        if 'SBB_TREASURE_CLOAKOFTHEASSASSIN' in player.treasures:
            targets = player.valid_characters(_lambda=lambda char: Tribe.ROYAL in char.tribes)
            for cloak in player.treasures['SBB_TREASURE_CLOAKOFTHEASSASSIN']:
                cloak.aura.execute(*targets)

class TreasureType(Treasure):
    display_name = 'Cursed Throne'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(CursedThroneOnSpawn)
        self.aura = Aura(reason=ActionReason.CURSED_THRONE, source=self, event=CursedThroneOnAttackAndKill,
                         priority=100, _lambda=lambda char: Tribe.ROYAL in char.tribes, _action=_throne_tribe_add)
