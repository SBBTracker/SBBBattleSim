from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath, OnSummon
from sbbbattlesim.utils import Tribe

JULIET_ID = 'SBB_CHARACTER_JULIET'


class RomeoOnSummon(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        for char in summoned_characters:
            if char is self.kwargs['juliet']:
                modifier = 14 if self.source.golden else 7
                Buff(reason=ActionReason.ROMEO_BUFF, source=self.source, targets=[char],
                     attack=modifier, health=modifier, temp=False).resolve()

        self.manager.unregister(self)


class RomeoLastBreath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        dead_juliets = [j for j in self.manager.player.graveyard if j.id == JULIET_ID]
        dying_juliets = [j for j in self.manager.player.characters.values() if j is not None and j.id == JULIET_ID and j.dead]

        dead_juliets.extend(dying_juliets)

        if dead_juliets:
            juliet = max(dead_juliets, key=lambda juliet: (juliet.attack, juliet.health))

            new_juliet = character_registry[juliet.id](
                attack=juliet._base_attack,
                health=max(juliet._base_health, 1),
                tribes=juliet.tribes,
                golden=juliet.golden,
                position=self.source.position,
                cost=juliet.cost,
                player=juliet.player,
            )

            self.manager.player.register(RomeoOnSummon, source=self.source, juliet=new_juliet)
            self.manager.player.summon(self.source.position, [new_juliet])


class CharacterType(Character):
    display_name = 'Romeo'
    last_breath = True

    _attack = 5
    _health = 3
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.ROYAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(RomeoLastBreath, source=self)
