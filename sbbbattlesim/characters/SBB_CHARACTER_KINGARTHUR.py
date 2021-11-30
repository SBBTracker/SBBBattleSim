from sbbbattlesim import utils
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import Tribe, StatChangeCause


class CharacterType(Character):
    display_name = 'Prince Arthur'

    _attack = 5
    _health = 5
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.PRINCE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class PrinceArthurOnStart(OnStart):
            arthur = self

            def handle(self, stack, *args, **kwargs):
                stat_change = 4 if self.arthur.golden else 2
                royals = self.manager.valid_characters(
                    _lambda=lambda char: char.golden and (Tribe.PRINCE in char.tribes or Tribe.PRINCESS in char.tribes)
                )
                for char in royals:
                    char.change_stats(
                        attack=stat_change, health=stat_change, source=self.arthur,
                        temp=False, reason=StatChangeCause.PRINCEARTHUR_BUFF, stack=stack
                    )

        self.owner.register(PrinceArthurOnStart)
