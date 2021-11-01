from sbbbattlesim.characters import Character
import logging

from sbbbattlesim.events import OnStart

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Lordy'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class LordyBuffOnStart(OnStart):
            lordy = self
            def handle(self, *args, **kwargs):
                dwarfes = self.manager.valid_characters(_lambda=lambda char: 'dwarf' in char.tribes or char.id == 'SBB_CHARACTER_PRINCESSNIGHT')
                stat_change = len(dwarfes) * (4 if self.lordy.golden else 2)
                for dwarf in dwarfes:
                    dwarf.change_stats(attack=stat_change, health=stat_change, temp=False, reason=f'{self} buff')

        self.owner.register(LordyBuffOnStart)
