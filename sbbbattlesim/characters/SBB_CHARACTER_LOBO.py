from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Southern Siren'
    slay = True

    _attack = 10
    _health = 10
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.SouthernSirenSlay)

    class SouthernSirenSlay(OnAttackAndKill):
        slay = True
        def handle(self, killed_character, *args, **kwargs):
            modifier = 2 if self.manager.golden else 1
            chars = [
                character_registry[killed_character.id](
                    self.manager.owner, self.manager.position,
                    killed_character.attack, killed_character.max_health,
                    golden=killed_character.golden,
                    tribes=killed_character.tribes,
                    cost=killed_character.cost
                )
            ]
            chars = chars*modifier

            self.manager.owner.summon(self.manager.position, chars)
