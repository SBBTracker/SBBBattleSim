from sbbbattlesim.events import OnResolveBoard, OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Eye of Ares'

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class EyeOfAresAura(OnResolveBoard):
            eye_of_ares = self

            def handle(self, *args, **kwargs):
                for _ in range(self.eye_of_ares.mimic + 1):
                    for char in self.manager.valid_characters():
                        char.change_stats(attack=5, reason=StatChangeCause.EYE_OF_ARES_BUFF, source=self.eye_of_ares, temp=True)

        class EyeOnStart(OnStart):
            def handle(self, *args, **kwargs):
                self.manager.register(EyeOfAresAura)
                self.manager.opponent.register(EyeOfAresAura)

        self.player.register(EyeOnStart)