from sbbbattlesim.characters import Character
import logging

from sbbbattlesim.events import OnStart

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Fake Caster'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class FakeCastOnStart(OnStart):
            caster = self
            def handle(self, *args, **kwargs):
                pass

        self.owner.register(FakeCastOnStart)
