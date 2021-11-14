from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnSlay
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Bad Moon'

    def buff(self, target_character):
        class BadMoonSlayBuff(OnSlay):
            bad_moon = self

            def handle(self, source, *args, **kwargs):
                self.manager.change_stats(attack=1, health=2, reason=StatChangeCause.BAD_MOON, source=self.bad_moon)

        target_character.register(BadMoonSlayBuff, temp=True)
