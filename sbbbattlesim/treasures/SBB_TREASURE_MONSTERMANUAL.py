from sbbbattlesim.action import Buff
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class MonsterManualOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        for _ in range(self.manual.mimic + 1):
            Buff(reason=StatChangeCause.MONSTER_MANUAL_BUFF, source=self.manual, targets=[self.manager],
                 attack=2, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = 'Monster Manual'
    aura = True

    _level = 2

    def buff(self, target_character, *args, **kwargs):
        if Tribe.MONSTER in target_character.tribes:
            target_character.register(MonsterManualOnDeath, temp=True, manual=self)
