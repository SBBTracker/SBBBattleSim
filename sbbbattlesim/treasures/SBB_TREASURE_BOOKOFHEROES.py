import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class BookOfHeroesOnAttackAndKillBuff(OnAttackAndKill):
    slay = False

    def handle(self, killed_character, stack, *args, **kwargs):
        logger.debug(f'BOOK KILLED {killed_character.tribes} MIMIC {self.book.mimic}')
        if Tribe.EVIL in killed_character.tribes:
            for _ in range(self.book.mimic + 1):
                Buff(reason=ActionReason.BOOK_OF_HEROES, source=self.book, targets=[self.manager],
                     attack=1, health=2, temp=False, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = '''Book of Heroes'''
    aura = True

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = Aura(event=BookOfHeroesOnAttackAndKillBuff, source=self, book=self,
                                   _lambda=lambda char: Tribe.GOOD in char.tribes)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
