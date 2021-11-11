from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = '''Book of Heroes'''

    def buff(self, target_character):
        if 'good' in target_character.tribes:
            class BookOfHeroesOnAttackAndKillBuff(OnAttackAndKill):
                good_character = target_character

                def handle(self, killed_character, *args, **kwargs):
                    if 'evil' in killed_character.tribes:
                        self.good_character.change_stats(attack=1, health=1, reason=203, source=self,
                                                         temp=False)
                    return "none", [], {}

            target_character.register(BookOfHeroesOnAttackAndKillBuff)
