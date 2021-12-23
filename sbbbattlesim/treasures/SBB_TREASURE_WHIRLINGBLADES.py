from sbbbattlesim.action import Buff, ActionReason, Aura
from sbbbattlesim.events import OnBuff, OnSpawn
from sbbbattlesim.treasures import Treasure


class SingingSwordsOnSpawn(OnSpawn):
    def handle(self, stack, raw=False, on_init=False, *args, **kwargs):
        if raw:
            return

        if self.manager.position in (1, 2, 3, 4):
            attack = self.manager.attack
            if self.source.mimic:
                attack *= 2
            Buff(reason=ActionReason.SINGINGSWORD_BUFF, source=self.source, attack=attack, *args, **kwargs).execute(
                *args, **kwargs)


class SingingSwordsOnBuff(OnBuff):
    def handle(self, stack, attack, health, reason=None, *args, **kwargs):
        if self.source.mimic:
            attack *= 2
        Buff(reason=ActionReason.SINGINGSWORD_BUFF, source=self.source, attack=attack, *args, **kwargs).execute(*args, **kwargs)


class TreasureType(Treasure):
    display_name = 'Singing Swords'
    _level = 6

    # aura = True
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.aura = Aura(reason=ActionReason.SINGINGSWORD_BUFF, event=SingingSwordsOnBuff, source=self, _lambda=lambda char: char.position in (1, 2, 3, 4))
    #     self.player.register(SingingSwordsOnSpawn, source=self)
