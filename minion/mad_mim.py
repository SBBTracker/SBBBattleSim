from events import BuffsEvent
from minion import Minion



class MinionType(Minion):
    name = 'Mad Mim'
    support = True

    class MadMimBuff(BuffsEvent):
        def __call__(self, **kwargs):
            buff_target = kwargs['buff_target']
            buff_target.attack_bonus += 3
            # print(f'{self.minion} buffed {buff_target} with +3 attack')

    buffs = [
        MadMimBuff,
    ]


