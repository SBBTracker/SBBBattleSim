from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSpellCast
from sbbbattlesim.utils import Tribe


class CinderelalOnSpellCast(OnSpellCast):
    def handle(self, caster, spell, target, stack, reason=None, *args, **kwargs):
        self.source.progress_quest(1)


class CharacterType(Character):
    display_name = 'Cinder-Ella'
    quest = True

    _attack = 2
    _health = 2
    _level = 2
    _tribes = {Tribe.ROYAL, Tribe.MAGE}
    _quest_counter = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cinderella_on_spell_cast_event = None
        if not self.golden:
            self.cinderella_on_spell_cast_event = self.player.register(CinderelalOnSpellCast, source=self)

    def progress_quest(self, amount):
        super().progress_quest(amount)
        self.player.unregister(self.cinderella_on_spell_cast_event)