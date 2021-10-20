from events import BuffsEvent
from characters import Character



class CharacterType(Character):
    name = 'Baby Root'
    support = True

    class BabyRootBuff(BuffsEvent):
        def __call__(self, **kwargs):
            buff_target = kwargs['buff_target']
            buff_target.health_bonus += 3
            # print(f'{self.characters} buffed {buff_target} with +3 health')

    buffs = [
        BabyRootBuff,
    ]

