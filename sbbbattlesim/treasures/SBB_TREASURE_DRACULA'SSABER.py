from sbbbattlesim.action import Buff, ActionReason, Aura
from sbbbattlesim.events import OnDeath, OnSetup
from sbbbattlesim.treasures import Treasure


class DraculasSaberOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        for _ in range(self.source.mimic + 1):
            Buff(reason=ActionReason.DRACULAS_SABER_BUFF, source=self.source,
                 targets=self.source.player.valid_characters(),
                 attack=2, health=1, stack=stack).resolve()


class DraculasSaberOnSetup(OnSetup):
    def handle(self, *args, **kwargs):
        self.source.player.opponent.auras.add(Aura(event=DraculasSaberOnDeath, source=self.source))


class TreasureType(Treasure):
    display_name = '''Dracula's Saber'''
    _level = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.board.register(DraculasSaberOnSetup, source=self, priority=1000)
