from sbbbattlesim import utils
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Ashwood Elm'

    _attack = 0
    _health = 20
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class AshwoodElmOnStart(OnStart):
            ashwood = self
            def handle(self, stack, *args, **kwargs):
                base_attack_change = self.ashwood.health
                modifier = 2 if self.ashwood.golden else 1
                attack_change = base_attack_change*modifier

                for char in self.manager.valid_characters(_lambda=lambda char: Tribe.TREANT in char.tribes):
                    char.change_stats(attack=attack_change, temp=False, reason=StatChangeCause.ASHWOOD_ELM_BUFF,
                                      source=self.ashwood, stack=stack)

        self.owner.register(AshwoodElmOnStart)
