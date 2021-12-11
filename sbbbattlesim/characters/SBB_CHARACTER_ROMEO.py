from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath, OnSummon
from sbbbattlesim.utils import Tribe, StatChangeCause

JULIET_ID = 'SBB_CHARACTER_JULIET'


class RomeoOnSummon(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        if self.triggered:
            return
        self.triggered = True
        for char in summoned_characters:
            if char is self.juliet:
                modifier = 14 if self.romeo.golden else 7
                Buff(reason=StatChangeCause.ROMEO_BUFF, source=self.romeo, targets=[char],
                     attack=modifier, health=modifier, temp=False).resolve()


class RomeoLastBreath(OnDeath):
    last_breath = True

    def handle(self, *args, **kwargs):
        dead_juliets = [j for j in self.manager.owner.graveyard if j.id == JULIET_ID]

        if dead_juliets:
            juliet = max(dead_juliets, key=lambda juliet: (juliet.attack, juliet.health))
            juliet._damage = 0

            new_juliet = character_registry[juliet.id](
                attack=juliet._base_attack,
                health=max(juliet._base_health, 1),
                tribes=juliet.tribes,
                golden=juliet.golden,
                position=self.romeo.position,
                cost=juliet.cost,
                owner=juliet.owner,
            )
            self.juliet = new_juliet

            self.manager.owner.register(RomeoOnSummon, juliet=self.juliet, romeo=self.romeo, triggered=False)
            self.manager.owner.summon(self.manager.position, [new_juliet])


class CharacterType(Character):
    display_name = 'Romeo'
    last_breath = True

    _attack = 5
    _health = 3
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.PRINCE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(RomeoLastBreath, romeo=self)
