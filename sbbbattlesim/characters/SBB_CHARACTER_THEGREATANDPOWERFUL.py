from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSpellCast
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    # PUFF PUFF VARIABLE
    # Store the global Puff Puff buff
    # THIS IS WRONG
    # TODO This is broken
    display_name = 'Storm King'

    _attack = 2
    _health = 2
    _level = 6
    _tribes = {Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        current_buff = self.owner._spells_cast
        new_buff = min(self.attack, self.health) - (4 if self.golden else 2)
        self.owner._spells_cast = min(current_buff, new_buff) if current_buff != 0 else new_buff

        class StormKingOnSpellCast(OnSpellCast):
            storm_king = self

            def handle(self, stack, *args, **kwargs):
                stat_buff = 4 if self.storm_king.golden else 2
                self.storm_king.change_stats(
                    attack=stat_buff,
                    health=stat_buff,
                    reason=StatChangeCause.STORM_KING_BUFF,
                    source=self.storm_king,
                    *args, **kwargs
                )

        self.owner.register(StormKingOnSpellCast)

    @classmethod
    def new(cls, *args, **kwargs):
        self = super().new(*args, **kwargs)

        self.owner.resolve_board()

        stat_buff = self.owner._spells_cast * (4 if self.golden else 2)

        self.change_stats(
            attack=stat_buff,
            health=stat_buff,
            reason=StatChangeCause.STORM_KING_BUFF,
            source=self,
        )

        return self