from sbbbattlesim import utils
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart


class CharacterType(Character):
    display_name = 'Prince Arthur'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class PrinceArthurOnStart(OnStart):
            arthur = self

            def handle(self, *args, **kwargs):
                stat_change = 4 if self.arthur.golden else 2
                royals = self.manager.owner.valid_characters(_lambda=lambda char: char.golden and ('prince' in char.tribes or 'princess' in char.tribes))
                for char in royals:
                    char.change_stats(attack=stat_change, health=stat_change, temp=False, reason=f'{self.arthur} Onstart Royal Buff')

        self.owner.register(PrinceArthurOnStart)
