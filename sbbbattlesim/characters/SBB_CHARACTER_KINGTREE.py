from sbbbattlesim import utils
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart


class CharacterType(Character):
    display_name = 'Ashwood Elm'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class AshwoodElmOnStart(OnStart):
            ashwood = self
            def handle(self, *args, **kwargs):
                base_attack_change = self.ashwood.health
                modifier = 2 if self.ashwood.golden else 1
                attack_change = base_attack_change*modifier

                for char in self.manager.valid_characters(_lambda=lambda char: 'treant' in char.tribes):
                    char.change_stats(attack=attack_change, temp=False, reason=f'{self.ashwood} giving {self} attack')

        self.owner.register(AshwoodElmOnStart)
