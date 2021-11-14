from sbbbattlesim import utils
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import get_behind_targets, Tribe


class CharacterType(Character):
    display_name = 'Soltak Ancient'
    aura = True

    _attack = 0
    _health = 20
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.TREANT}

    def buff(self, target_character):
        behind = utils.get_behind_targets(self.position)
        if target_character.position in behind:
            target_character.invincible = True
