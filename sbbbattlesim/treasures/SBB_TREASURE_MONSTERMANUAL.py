from sbbbattlesim.events import OnStart, OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Monster Manual'
    aura = True

    def buff(self, target_character):

        class MonsterManualOnDeath(OnDeath):
            manual = self
            last_breath = False
            def handle(self, *args, **kwargs):
                for _ in range(self.manual.mimic + 1):
                    self.manager.change_stats(attack=2, reason=StatChangeCause.MONSTER_MANUAL_BUFF, source=self.manual)

        target_character.register(MonsterManualOnDeath, temp=True)
