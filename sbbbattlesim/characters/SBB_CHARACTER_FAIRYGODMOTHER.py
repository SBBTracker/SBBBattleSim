from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
import logging

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Fairy Godmother'
    aura = True

    def buff(self, target_character):
        class FairyGodmotherOnDeath(OnDeath):
            fairy_godmother = self

            def handle(self, *args, **kwargs):
                stat_change = 4 if self.fairy_godmother.golden else 2
                for char in self.manager.owner.valid_characters():
                    if 'good' in char.tribes:
                        char.change_stats(health=stat_change, temp=False,
                                          reason=f'{self.manager} died and buffed all good units')

        # Give animals minions the buff
        if 'good' in target_character.tribes:  # Distinctly Fairy Godmother works on self
            target_character.register(FairyGodmotherOnDeath, temp=True)