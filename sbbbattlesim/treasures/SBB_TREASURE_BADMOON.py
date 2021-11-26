from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnSlay
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Bad Moon'
    aura = True

    _level = 3

    def buff(self, target_character):
        class BadMoonSlayBuff(OnSlay):
            bad_moon = self

            def handle(self, source, stack, *args, **kwargs):
                for _ in range(self.bad_moon.mimic + 1):
                    self.manager.change_stats(attack=1, health=2, reason=StatChangeCause.BAD_MOON,
                                              source=self.bad_moon, temp=False)

        target_character.register(BadMoonSlayBuff, temp=True)
