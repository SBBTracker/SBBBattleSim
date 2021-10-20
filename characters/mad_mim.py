from events import BuffsEvent
from characters import Character



class CharacterType(Character):
    name = 'Mad Mim'
    support = True

    class MadMimBuff(BuffsEvent):
        def __call__(self, **kwargs):
            buff_target = kwargs['buff_target']
            buff_target.attack_bonus += 3
            # print(f'{self.characters} buffed {buff_target} with +3 attack')

    buffs = [
        MadMimBuff,
    ]


