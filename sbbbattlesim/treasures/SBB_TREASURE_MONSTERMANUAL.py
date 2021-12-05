from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Monster Manual'
    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):

        class MonsterManualOnDeath(OnDeath):
            manual = self
            last_breath = False
            def handle(self, stack, *args, **kwargs):
                for _ in range(self.manual.mimic + 1):
                    self.manager.change_stats(attack=2, reason=StatChangeCause.MONSTER_MANUAL_BUFF, source=self.manual, stack=stack)

        target_character.register(MonsterManualOnDeath, temp=True)
