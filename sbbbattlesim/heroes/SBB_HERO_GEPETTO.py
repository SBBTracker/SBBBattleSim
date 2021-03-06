from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.events import OnSummon
from sbbbattlesim.heroes import Hero


class GeppettoOnSummon(OnSummon):

    def handle(self, summoned_characters, stack, *args, **kwargs):
        level = self.source.player.level
        Buff(reason=ActionReason.GEPPETTO_BUFF, source=self.source, targets=summoned_characters,
             attack=level, health=level, stack=stack, temp=False).resolve()


class HeroType(Hero):
    display_name = 'Geppetto'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(GeppettoOnSummon, source=self)
