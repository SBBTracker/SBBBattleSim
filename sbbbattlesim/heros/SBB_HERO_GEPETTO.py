from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.events import OnSummon
from sbbbattlesim.heros import Hero


class GeppettoOnSummon(OnSummon):

    def handle(self, summoned_characters, stack, *args, **kwargs):
        level = self.geppetto.player.level
        Buff(reason=ActionReason.GEPPETTO_BUFF, source=self.geppetto, targets=summoned_characters,
             attack=level, health=level, stack=stack, temp=False).resolve()


class HeroType(Hero):
    display_name = 'Geppetto'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(GeppettoOnSummon, geppetto=self)
