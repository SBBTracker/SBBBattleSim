from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath


class TreasureType(Treasure):
    display_name = 'Mirror Mirror'

    _level = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class MirrorMirrorOnDeath(OnDeath):
            mirror = self
            last_breath = False

            def handle(self, *args, **kwargs):
                copies = [self.manager.__class__(
                    owner=self.manager.owner,
                    position=self.manager.position,
                    attack=1,
                    health=1,
                    golden=False,
                    tribes=self.manager.tribes,
                    cost=self.manager.cost,
                ) for _ in range(1 + bool(self.mirror.mimic))]

                self.manager.owner.summon(self.manager.position, *copies)

        for char in self.player.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4)):
            char.register(MirrorMirrorOnDeath)
