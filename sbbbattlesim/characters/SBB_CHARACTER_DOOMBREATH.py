from sbbbattlesim import utils
from sbbbattlesim.characters import Character
from sbbbattlesim.action import Damage, ActionReason
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Doombreath'

    _attack = 10
    _health = 6
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.DRAGON}

    def generate_attack(self, source, target, reason, attacking=False):
        if not attacking:
            return super().generate_attack(target=target, source=source, reason=reason, attacking=attacking)

        behind_targets = utils.get_behind_targets(target.position)
        targets = [target, *[char for char in self.player.opponent.valid_characters(
            _lambda=lambda char: char.position in behind_targets)]]

        return Damage(
            damage=self.attack,
            reason=reason,
            source=self,
            targets=targets
        )
