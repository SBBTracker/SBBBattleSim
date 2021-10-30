from sbbbattlesim.events import OnDeath
from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'Evil Queen'
    aura = True

    def buff(self, target_character):
        # Instantiate queen buff
        class EvilQueenOnDeath(OnDeath):
            evil_queen = self
            def handle(self, *args, **kwargs):

                self.evil_queen.base_attack += 4 if self.evil_queen.golden else 2
                self.evil_queen.base_health += 4 if self.evil_queen.golden else 2

        # Give evil minions the buff
        if 'evil' in target_character.tribes and target_character is not self:
            target_character.register(EvilQueenOnDeath, temp=True)