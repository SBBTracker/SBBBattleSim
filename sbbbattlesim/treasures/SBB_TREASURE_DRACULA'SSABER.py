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

            def handle(self, stack, *args, **kwargs):
                for char in self.saber.player.valid_characters():
                    for _ in range(self.saber.mimic + 1):
                        char.change_stats(attack=2, health=1, reason=StatChangeCause.DRACULAS_SABER_BUFF,
                                          source=self.saber, temp=False, stack=stack)

        class DraculasSaberOnResolveBoard(OnResolveBoard):
            def handle(self, *args, **kwargs):
                for char in self.manager.valid_characters():
                    char.register(DraculasSaberOnDeath, temp=True)

        class DraculasSaberOnStart(OnStart):
            saber = self
            def handle(self, *args, **kwargs):
                self.saber.player.opponent.register(DraculasSaberOnResolveBoard)

        self.player.board.register(DraculasSaberOnStart)