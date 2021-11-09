from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSlay
from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Baba Yaga'
    support = True

    def buff(self, target_character):

        class BabaYagaOnSlayBuff(OnSlay):
            baba_yaga = self
            def handle(self, *args, **kwargs):
                source = kwargs['source']
                for _ in range(2 if self.baba_yaga.golden else 1):
                    source(*args, **kwargs)

        target_character.register(BabaYagaOnSlayBuff, temp=True)
