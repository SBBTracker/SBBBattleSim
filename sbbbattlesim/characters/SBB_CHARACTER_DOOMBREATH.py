from sbbbattlesim import utils
from sbbbattlesim.characters import Character
from sbbbattlesim.action import Damage
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Doombreath'

    _attack = 10
    _health = 6
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.DRAGON}

    def generate_attack(self, target, reason, attacker=False):
        behind_targets = utils.get_behind_targets(target.position)
        targets = [target, *[char for char in self.owner.opponent.valid_characters(
            _lambda=lambda char: char.position in behind_targets)]]

        return Damage(
            damage=self.attack,
            reason=reason,
            source=self,
            targets=targets
        )
