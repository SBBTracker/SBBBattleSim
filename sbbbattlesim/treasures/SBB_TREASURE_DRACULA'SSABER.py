from sbbbattlesim.action import Buff, ActionReason, Aura
from sbbbattlesim.events import OnDeath, OnSetup
from sbbbattlesim.treasures import Treasure


class DraculasSaberOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, reason, *args, **kwargs):
        for _ in range(self.source.multiplier + 1):
            Buff(reason=ActionReason.DRACULAS_SABER_BUFF, source=self.source, attack=1, health=1,).execute(*self.source.player.valid_characters())


class DraculasSaberOnSetup(OnSetup):
    def handle(self, *args, **kwargs):
        self.source.player.opponent.add_aura(Aura(event=DraculasSaberOnDeath, source=self.source, priority=1000))


class TreasureType(Treasure):
    display_name = '''Dracula's Saber'''
    _level = 5

    #TODO: Rewrite this to have it listen to OnDeath in a generic manner
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(DraculasSaberOnSetup, source=self, priority=1000)
