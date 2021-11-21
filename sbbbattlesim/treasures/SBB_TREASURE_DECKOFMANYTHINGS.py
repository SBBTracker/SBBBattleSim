import random

from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'Deck of Many Things'

    spell_list = (
        '''SBB_SPELL_FALLINGSTARS''',
        '''SBB_SPELL_EARTHQUAKE''',
        '''SBB_SPELL_RIDEOFTHEVALKYRIES''',
        '''SBB_SPELL_ANGEL'SBLESSING''',
        '''SBB_SPELL_LIGHTNINGBOLT''',
        '''SBB_SPELL_FIREBALL''',
        '''SBB_SPELL_ENFEEBLEMENT''',
        '''SBB_SPELL_POISONAPPLE''',
        '''SBB_SPELL_DISINTEGRATE''',
        '''SBB_SPELL_PIGOMORPH''',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class DeckOfManyThingsOnStart(OnStart):
            deck = self

            def handle(self, *args, **kwargs):
                self.manager.cast_spell(random.choice(self.deck.spell_list))
                if self.deck.mimic:
                    self.manager.cast_spell(random.choice(self.deck.spell_list))

        self.player.register(DeckOfManyThingsOnStart)