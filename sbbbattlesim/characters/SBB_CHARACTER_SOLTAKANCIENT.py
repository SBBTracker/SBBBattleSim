from sbbbattlesim import utils
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import get_behind_targets


class CharacterType(Character):
    display_name = 'Soltak Ancient'
    aura = True

    def buff(self, target_character):
        behind = utils.get_behind_targets(self.position)
        if target_character.position in behind:
            target_character.invincible = True
