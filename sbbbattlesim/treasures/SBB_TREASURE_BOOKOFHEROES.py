import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class BookOfHeroesOnAttackAndKillBuff(OnAttackAndKill):
    slay = False

    def handle(self, killed_character, stack, *args, **kwargs):
        logger.debug(f'BOOK KILLED {killed_character.tribes} MIMIC {self.source.mimic}')
        if Tribe.EVIL in killed_character.tribes:
            for _ in range(self.source.mimic + 1):
                Buff(reason=ActionReason.BOOK_OF_HEROES, source=self.source, targets=[self.manager],
                     attack=1, health=2, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = '''Book of Heroes'''
    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(event=BookOfHeroesOnAttackAndKillBuff, source=self,
                         _lambda=lambda char: Tribe.GOOD in char.tribes)
