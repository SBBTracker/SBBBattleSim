from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
import random


class CharacterType(Character):
    display_name = 'Grim Soul'
    last_breath = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.GrimSoulLastBreath)

    class GrimSoulLastBreath(OnDeath):
        last_breath = True
        def handle(self, *args, **kwargs):
            valid_chars = self.manager.owner.valid_characters(
                _lambda = lambda char : char.event_type_is_registered('OnAttackAndKill') \
                                        and char.id != "SBB_CHARACTER_CERBERUS"
            )

            if valid_chars:
                char = random.choice(valid_chars)
                char('OnAttackAndKill', None, *args, **kwargs)