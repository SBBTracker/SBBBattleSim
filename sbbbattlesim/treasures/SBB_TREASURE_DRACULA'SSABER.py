from sbbbattlesim.events import OnResolveBoard, OnStart, OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = '''Dracula's Saber'''

    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class DraculasSaberOnDeath(OnDeath):
            saber = self
            last_breath = False

            def handle(self, *args, **kwargs):
                for char in self.saber.player.valid_characters():
                    char.change_stats(attack=2, health=1, reason=StatChangeCause.DRACULAS_SABER_BUFF, source=self.saber,
                                      temp=False)
                    if self.saber.mimic:
                        char.change_stats(attack=2, health=1, reason=StatChangeCause.DRACULAS_SABER_BUFF,
                                          source=self.saber, temp=False)

        class DraculasSaberOnResolveBoard(OnResolveBoard):
            def handle(self, *args, **kwargs):
                for char in self.manager.valid_characters():
                    char.register(DraculasSaberOnDeath, temp=True)

        class DraculasSaberOnStart(OnStart):
            def handle(self, *args, **kwargs):
                self.manager.opponent.register(DraculasSaberOnResolveBoard)

        self.player.register(DraculasSaberOnStart)