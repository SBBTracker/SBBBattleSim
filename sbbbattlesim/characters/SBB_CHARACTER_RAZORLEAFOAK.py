from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe, StatChangeCause


class CharacterType(Character):
    display_name = 'Broc Lee'

    _attack = 0
    _health = 15
    _level = 4
    _tribes = {Tribe.EVIL, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class BrocLeeOnDamageAndSurvived(OnDamagedAndSurvived):
            def handle(self, stack, *args, **kwargs):
                self.manager.change_stats(
                    attack=20 if self.manager.golden else 10, temp=False,
                    reason=StatChangeCause.BROC_LEE_BUFF, source=self.manager,
                    stack=stack
                )

        self.register(BrocLeeOnDamageAndSurvived)
