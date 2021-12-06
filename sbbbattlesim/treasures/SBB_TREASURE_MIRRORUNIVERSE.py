from sbbbattlesim.events import OnDeath, OnStart
from sbbbattlesim.treasures import Treasure


class MirrorMirrorOnDeath(OnDeath):
    last_breath = False

    def handle(self, *args, **kwargs):
        copies = [
            self.manager.__class__(
                owner=self.manager.owner,
                position=self.manager.position,
                attack=1,
                health=1,
                golden=False,
                tribes=self.manager.tribes,
                cost=self.manager.cost,
                # TODO does this copy the tribes of the card or of the class
            ) for _ in range(1 + bool(self.mirror.mimic))
        ]

        self.manager.owner.summon(self.manager.position, copies)


class MirrorMirrorOnStart(OnStart):
    def handle(self, *args, **kwargs):
        for char in self.mirror.player.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4)):
            char.register(MirrorMirrorOnDeath, mirror=self.mirror)


class TreasureType(Treasure):
    display_name = 'Mirror Mirror'

    _level = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.board.register(MirrorMirrorOnStart, mirror=self)
