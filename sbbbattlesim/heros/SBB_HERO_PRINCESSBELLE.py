from sbbbattlesim.action import Aura
from sbbbattlesim.characters import Character
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe


def beauty_tribe_shift(char: Character):
    if Tribe.GOOD in char.tribes:
        char.tribes.add(Tribe.EVIL)
    elif Tribe.EVIL in char.tribes:
        char.tribes.add(Tribe.GOOD)


class HeroType(Hero):
    display_name = 'Beauty'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = Aura(_action=beauty_tribe_shift)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
