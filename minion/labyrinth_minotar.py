from events import BuffsEvent
from minion import Minion



class MinionType(Minion):
    name = 'Labyrinth Minotaur'

    class LabyrinthMinotaurBuff(BuffsEvent):
        def __call__(self, **kwargs):
            buff_target = kwargs['buff_target']
            if 'evil' in buff_target.tribes and buff_target != self.minion:
                buff_target.attack_bonus += 1
                # print(f'{self.minion} buffed {buff_target} with +3 attack')

    buffs = [
        LabyrinthMinotaurBuff,
    ]

