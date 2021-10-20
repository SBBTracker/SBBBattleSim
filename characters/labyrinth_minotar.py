from events import BuffsEvent
from characters import Character



class CharacterType(Character):
    name = 'Labyrinth Minotaur'

    class LabyrinthMinotaurBuff(BuffsEvent):
        def __call__(self, **kwargs):
            buff_target = kwargs['buff_target']
            if 'evil' in buff_target.tribes and buff_target != self.character:
                buff_target.attack_bonus += 1
                # print(f'{self.characters} buffed {buff_target} with +3 attack')

    buffs = [
        LabyrinthMinotaurBuff,
    ]

