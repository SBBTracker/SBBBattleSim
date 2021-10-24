from sbbbattlesim.events import BuffsEvent, SupportEvent
from sbbbattlesim.characters import Character



class CharacterType(Character):
    name = 'Mad Mim'
    support = True

    class MadMimBuff(SupportEvent):
        def __call__(self, **kwargs):
            kwargs['buff_target'].attack_bonus += 6 if self.character.golden else 3

    support = (
        MadMimBuff,
    )


