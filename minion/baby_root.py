from events import BuffsEvent
from minion import Minion



class MinionType(Minion):
    name = 'Baby Root'
    support = True

    class BabyRootBuff(BuffsEvent):
        def __call__(self, **kwargs):
            buff_target = kwargs['buff_target']
            buff_target.health_bonus += 3
            # print(f'{self.minion} buffed {buff_target} with +3 health')

    buffs = [
        BabyRootBuff,
    ]

