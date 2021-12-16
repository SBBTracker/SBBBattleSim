from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.events import OnResolveBoard, OnStart
from sbbbattlesim.treasures import Treasure


class EyeOfAresAura(OnResolveBoard):
    def handle(self, stack, *args, **kwargs):
        for _ in range(self.eye_of_ares.mimic + 1):
            Buff(reason=ActionReason.EYE_OF_ARES_BUFF, source=self.eye_of_ares, targets=self.manager.valid_characters(),
                 attack=5, temp=True, stack=stack).resolve()


class EyeOnStart(OnStart):
    def handle(self, *args, **kwargs):
        self.eye_of_ares.player.register(EyeOfAresAura, eye_of_ares=self.eye_of_ares)
        self.eye_of_ares.player.opponent.register(EyeOfAresAura, eye_of_ares=self.eye_of_ares)


class TreasureType(Treasure):
    display_name = 'Eye of Ares'

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.board.register(EyeOnStart, eye_of_ares=self)
