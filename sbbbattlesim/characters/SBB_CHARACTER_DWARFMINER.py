from sbbbattlesim.characters import Character
import logging

from sbbbattlesim.events import OnStart, OnDamagedAndSurvived

logger = logging.getLogger(__name__)


class CharacterType(Character):
    display_name = 'Angry'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class AngryBuff(OnDamagedAndSurvived):
            def handle(self, *args, **kwargs):
                dwarfes = self.manager.owner.valid_characters(_lambda=lambda char: 'dwarf' in char.tribes)
                stat_change = 4 if self.manager.golden else 2
                for dwarf in dwarfes:
                    dwarf.change_stats(attack=stat_change, health=stat_change, temp=False, reason=f'{self} buff')

        self.register(AngryBuff)
