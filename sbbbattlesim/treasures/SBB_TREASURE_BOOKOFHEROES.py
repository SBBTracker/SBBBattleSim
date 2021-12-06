import logging

from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe

logger = logging.getLogger(__name__)


class BookOfHeroesOnAttackAndKillBuff(OnAttackAndKill):
    slay = False

    def handle(self, killed_character, stack, *args, **kwargs):
        logger.debug(f'BOOK KILLED {killed_character.tribes} MIMIC {self.book.mimic}')
        if Tribe.EVIL in killed_character.tribes:
            for _ in range(self.book.mimic + 1):
                self.target_character.change_stats(attack=1, health=2, reason=StatChangeCause.BOOK_OF_HEROES,
                                                   source=self.book, temp=False, stack=stack)


class TreasureType(Treasure):
    display_name = '''Book of Heroes'''
    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):
        if Tribe.GOOD in target_character.tribes:
            target_character.register(BookOfHeroesOnAttackAndKillBuff, temp=True, target_character=target_character,
                                      book=self)
