from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


class HeroType(Hero):
    display_name = 'Fallen Angel'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.angel_attack_buff = len(self.player.valid_characters(_lambda=lambda char: Tribe.EVIL in char.tribes)) >= 3
        self.angel_health_buff = len(self.player.valid_characters(_lambda=lambda char: Tribe.GOOD in char.tribes)) >= 3

    def buff(self, target_character):
        attack_buff = 2 if self.angel_attack_buff else 0
        health_buff = 2 if self.angel_health_buff else 0

        target_character.change_stats(attack=attack_buff, health=health_buff, reason=StatChangeCause.FALLEN_ANGEL_BUFF, source=self, temp=True)
