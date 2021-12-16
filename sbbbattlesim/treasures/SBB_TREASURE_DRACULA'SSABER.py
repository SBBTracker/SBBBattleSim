from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.events import OnResolveBoard, OnStart, OnDeath
from sbbbattlesim.treasures import Treasure


class DraculasSaberOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        for _ in range(self.saber.mimic + 1):
            Buff(reason=ActionReason.DRACULAS_SABER_BUFF, source=self.saber,
                 targets=self.saber.player.valid_characters(),
                 attack=2, health=1, temp=False, stack=stack).resolve()


class DraculasSaberOnResolveBoard(OnResolveBoard):
    def handle(self, *args, **kwargs):
        for char in self.manager.valid_characters():
            char.register(DraculasSaberOnDeath, temp=True, saber=self.saber)


class DraculasSaberOnStart(OnStart):
    def handle(self, *args, **kwargs):
        self.saber.player.opponent.register(DraculasSaberOnResolveBoard, saber=self.saber)


class TreasureType(Treasure):
    display_name = '''Dracula's Saber'''

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.board.register(DraculasSaberOnStart, saber=self)
