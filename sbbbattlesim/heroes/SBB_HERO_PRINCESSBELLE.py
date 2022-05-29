from sbbbattlesim.action import Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.heroes import Hero
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
        self.aura = Aura(reason=ActionReason.BEAUTY_TRIBE_SHIFT, _action=beauty_tribe_shift, source=self, priority=-100)
