from sbbbattlesim.action import Aura
from sbbbattlesim.events import OnDeath, OnStart
from sbbbattlesim.treasures import Treasure


class MirrorMirrorOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, reason, *args, **kwargs):
        copies = [
            self.manager.__class__(
                player=self.manager.player,
                position=self.manager.position,
                attack=1,
                health=1,
                golden=False,
                tribes=self.manager._tribes,
                cost=self.manager.cost,
                # TODO does this copy the tribes of the card or of the class
            ) for _ in range(1 + self.source.mimic)
        ]

        self.manager.player.summon(self.manager.position, copies)


class MirrorMirrorOnStart(OnStart):
    def handle(self, *args, **kwargs):
        for char in self.source.player.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4)):
            char.register(MirrorMirrorOnDeath, source=self.source, priority=999)


class TreasureType(Treasure):
    display_name = 'Mirror Mirror'
    aura = True
    _level = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(MirrorMirrorOnStart, source=self)
