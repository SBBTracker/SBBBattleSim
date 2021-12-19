import collections
import enum
import logging
from dataclasses import dataclass
from enum import Enum
from typing import List

from sbbbattlesim.events import SSBBSEvent
from sbbbattlesim.heros import Hero
from sbbbattlesim.spells import Spell
from sbbbattlesim.treasures import Treasure

logger = logging.getLogger(__name__)


class ActionState(Enum):
    CREATED = 1
    EXECUTED = 2
    RESOLVED = 3
    ROLLED_BACK = 4


class ActionReason(enum.Enum):
    DAMAGE_WHILE_ATTACKING = 1
    DAMAGE_WHILE_DEFENDING = 2
    SUPPORT_BUFF = 3
    AURA_BUFF = 4
    PLAYER_AURA = 5
    SLAY = 6

    ANGRY_BUFF = 101
    DOUBLEY_BUFF = 102
    FRIENDLY_SPIRIT_BUFF = 103
    PUFF_PUFF_BUFF = 107
    ROBIN_WOOD_DEBUFF = 108
    ROBIN_WOOD_BUFF = 109
    ROTTEN_APPLE_TREE_HEALTH = 110
    SHOULDER_FAIRY_BUFF = 111
    WRETCHED_MUMMY_EXPLOSION = 120
    SHADOW_ASSASSIN_ON_SLAY_BUFF = 121
    WIZARDS_FAMILIAR = 122
    BROC_LEE_BUFF = 123
    WOMBATS_IN_DISGUISE_BUFF = 124
    ECHOWOOD_BUFF = 125
    DARKWOOD_CREEPER_BUFF = 126
    THE_WHITE_STAG_BUFF = 127
    GOODBOY_BUFF = 128
    EVILQUEEN_BUFF = 129
    HUNGRYHUNGRYHIPPOCAMPUS_BUFF = 130
    LORDY_BUFF = 131
    RAINBOWUNICORN_BUFF = 132
    ASHWOOD_ELM_BUFF = 133
    BEARDEDVULTURE_BUFF = 134
    HEARTWOOD_BUFF = 135
    FAIRY_GODMOTHER_BUFF = 136
    PRINCEARTHUR_BUFF = 137
    ONIKING_BUFF = 138
    BEARSTINE_BUFF = 139
    ROMEO_BUFF = 140
    SPELL_WEAVER = 141
    CRAFTY_BUFF = 142
    STORM_KING_BUFF = 143
    AON_BUFF = 144
    PRINCESS_WIGHT_BUFF = 145

    ANCIENT_SARCOPHAGUS = 201
    BAD_MOON = 202
    BOOK_OF_HEROES = 203
    DEEPSTONE_MINE = 204
    CLOAK_OF_THE_ASSASSIN = 205
    CORRUPTED_HEARTWOOD = 206
    CROWN_OF_ATLAS = 207
    DRAGON_NEST = 208
    EASTER_EGG = 209
    EYE_OF_ARES = 210
    FAIRY_QUEENS_WAND = 211
    FOUNTAIN_OF_YOUTH = 212
    MONKEYS_PAW = 213
    JACKS_JUMPING_BEANS = 214
    OTHER_HAND_OF_VEKNA = 215
    MAGIC_SWORD = 216
    COIN_OF_CHARON = 217
    POWER_ORB = 218
    NOBLE_STEED = 219
    SIX_OF_SHIELDS = 220
    RING_OF_METEORS = 221
    RING_OF_RAGE = 222
    RING_OF_REVENGE = 223
    NEEDLE_NOSE_DAGGERS = 224
    DANCING_SWORD = 225
    SHEPHERDS_SLING = 226
    SKYCASTLE = 227
    STING = 228
    STONEHELM = 229
    SWORD_OF_FIRE_AND_ICE = 230
    TELL_TALE_QUIVER = 231
    TREE_OF_LIFE = 232
    SPEAR_OF_ACHILLES = 233
    SUMMONING_PORTAL = 234
    MONSTER_MANUAL_BUFF = 235
    EYE_OF_ARES_BUFF = 236
    MOONSONG_HORN_BUFF = 237
    SUMMONING_PORTA = 238
    EXPLODING_MITTENS_DAMAGE = 239
    HELM_OF_THE_UGLY_GOSLING = 240
    DRACULAS_SABER_BUFF = 241
    IVORY_OWL_BUFF = 242
    ROUND_TABLE_BUFF = 243
    SINGINGSWORD_BUFF = 244

    EVELLA_BUFF = 301
    MERLIN_BUFF = 302
    POTION_MASTER_BUFF = 303
    GEPPETTO_BUFF = 304
    JACKS_GIANT_BUFF = 305
    MRS_CLAUS_BUFF = 306
    FATES_BUFF = 307
    KRAMPUS_BUFF = 308
    CHARON_BUFF = 309
    SAD_DRACULA_SLAY = 310
    MIRHI_BUFF = 311
    FALLEN_ANGEL_BUFF = 312
    PUP_BUFF = 313

    BLESSING_OF_ATHENA = 401
    LUNAS_GRAVE = 402
    RIDE_OF_THE_VALKYRIES = 403
    SUGAR_AND_SPICE = 404
    MAGIC_RESEARCH = 405
    WITCHS_BREW = 406
    GIGANTIFY = 407
    HUGEIFY = 408
    STONE_SKIN = 409
    WORM_ROOT = 410
    BEAUTYS_INFLUENCE = 411
    MERLINS_TEST = 412
    QUEENS_GRACE = 413
    FLOURISH = 414
    TOIL_AND_TROUBLE = 415

    SMITE = 450
    EARTHQUAKE = 451
    SHRIVEL = 452
    FALLING_STARS = 453
    FIREBALL = 454
    LIGHTNING_BOLT = 455
    POISON_APPLE = 456


@dataclass
class DynamicStat:
    s: int

    def __add__(self, other):
        self.s += other

    def __sub__(self, other):
        self.s -= other

    def __eq__(self, other):
        return self.s == other

    def __ne__(self, other):
        return self.s != other

    def __lt__(self, other):
        return self.s < other

    def __le__(self, other):
        return self.s <= other

    def __gt__(self, other):
        return self.s > other

    def __ge__(self, other):
        return self.s >= other

    def __str__(self):
        return str(self.s)


class Action:
    def __init__(
            self,
            reason: ActionReason,
            source: ('Character', Treasure, Hero, Spell),
            targets: (List['Character'], None) = None,
            _lambda=None,
            priority: int = 0,
            attack: int = 0,
            health: int = 0,
            damage: int = 0,
            heal: int = 0,
            event: (SSBBSEvent, None) = None,
            player_event: bool = False,
            _action=None,
            *args,
            **kwargs
    ):
        self.reason = reason
        self.source = source
        self.targets = targets or []
        self._lambda = _lambda or (lambda _: True)
        self._action = _action
        self.priority = priority

        self.attack = attack
        self.health = health
        self.damage = damage
        self.heal = heal

        self.event = event
        self.player_event = player_event
        self.player_registered = False

        self.args = args
        self.kwargs = kwargs

        self.state = ActionState.CREATED
        self._char_buffer = set()
        self._event_buffer = collections.defaultdict(list)

        logger.debug(f'New {self}')

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'{self.reason} {self.source.pretty_print()} >>> {[char.pretty_print() for char in self.targets]} ({self.args}, {self.kwargs})'

    def _apply(self, char, on_init=False, raw=False, *args, **kwargs):
        '''
        This is the core of any Action class and should not be touched unless you are making changes to ALL effects
        This should never be accessed outside an Action class or subclass
        '''

        args = (*self.args, *args)
        kwargs = self.kwargs | kwargs
        self._char_buffer.add(char)
        char._action_history.append(self)

        if self.event and (not self.player_registered if self.player_event else True):
            if self.player_event:
                registered = char.player.register(self.event, priority=self.priority, source=self.source, *args,
                                                  **kwargs)
                self.player_registered = True
            else:
                registered = char.register(self.event, priority=self.priority, source=self.source, *args, **kwargs)
            self._event_buffer[char].append(registered)

        if not raw:
            if self.attack != 0 or self.health != 0:
                char._base_attack += self.attack
                char._base_health += self.health

                # TRIGGER ON BUFF
                if not on_init:
                    char('OnBuff', reason=self.reason, source=self.source, attack=self.attack, health=self.health, *args,
                         **kwargs)

        if self.damage != 0:
            if char.invincible and self.reason != ActionReason.DAMAGE_WHILE_ATTACKING:
                char('OnDamagedAndSurvived', damage=0, *args, **kwargs)
                return
            char._damage += self.damage

        if self.heal != 0:
            char._damage = 0 if self.heal == -1 else max(char._damage - self.heal, 0)

        if char.health <= 0:
            char.dead = True
            logger.debug(f'{char.pretty_print()} marked for death')
        elif self.damage > 0:
            char('OnDamagedAndSurvived', damage=self.damage, *args, **kwargs)

        if callable(self._action):
            self._action(char)

    def _clear(self, char, *args, **kwargs):
        '''
        This is the core function to specify how to reverse an action and should not be touched unless you are making changes to ALL effects
        This should never be accessed outside an Action class or subclass
        '''
        logger.debug(f'Clearing char {char.pretty_print()}')
        if self.event and (self.player_registered if self.player_event else True):
            if self.player_event:
                for registered in self._event_buffer.get(char.player, []):
                    char.player.unregister(registered)
            else:
                for registered in self._event_buffer.get(char, []):
                    char.unregister(registered)

        if self.health != 0:
            logger.debug(f'health to clear: {self.health} ; damage {char._damage} ; health {char._base_health}')
            char._damage -= min(char._damage, self.health)
            char._base_health -= self.health
            logger.debug(f'health after clear: {self.health} ; damage {char._damage} ; health {char._base_health}')

        if self.attack != 0:
            char._base_attack -= self.attack

        logger.debug(f'finished clearing char {char.pretty_print()}')

    def execute(self, character=None, *args, **kwargs):
        if self.state in (ActionState.RESOLVED, ActionState.ROLLED_BACK):
            return

        if character:
            if not self._lambda(character):
                return
            self._apply(character, *args, **kwargs)
        else:
            for char in self.targets:
                self._apply(char, *args, **kwargs)

        self.state = ActionState.EXECUTED

    def update(self, attack=0, health=0, targets=None, *args, **kwargs):
        logger.debug(f'{self} updating (attack={attack}, health={health}) >>> {targets}')
        args = (*self.args, *args)
        kwargs = self.kwargs | kwargs

        self.attack += attack
        self.health += health

        for char in self._char_buffer:
            if self.attack != 0 or self.health != 0:
                char._base_attack += attack
                char._base_health += health
                char('OnBuff', reason=self.reason, source=self.source, attack=attack, health=health, *args, **kwargs)

        if targets:
            for char in targets:
                if char in self._char_buffer:
                    continue
                self._apply(char, *args, **kwargs)

    def roll_back(self):
        for char in self.targets or self._char_buffer:
            self._clear(char)

        self.state = ActionState.ROLLED_BACK

    def resolve(self):
        if self.state == ActionState.CREATED:
            self.execute()
        elif self.state in (ActionState.RESOLVED, ActionState.ROLLED_BACK):
            logger.debug(f'{self} ALREADY RESOLVED')
            return

        logger.debug(f'RESOLVING DAMAGE FOR {self}')

        characters = self._char_buffer
        self._char_buffer = set()

        dead_characters = []

        for char in characters:
            if char in char.player.graveyard:
                logger.debug(f'{char.pretty_print()} already in graveyard')
                continue

            if char.dead:
                dead_characters.append(char)
                char.player.despawn(char)

        logger.info(f'These are the dead characters: {dead_characters}')
        for char in sorted(dead_characters, key=lambda _char: _char.position, reverse=True):
            char('OnDeath')

        self.state = ActionState.RESOLVED


class Damage(Action):
    pass


class Heal(Action):
    pass


class Buff(Action):
    pass


class Support(Buff):
    def __init__(self, *args, **kwargs):
        kwargs = dict(reason=ActionReason.SUPPORT_BUFF) | kwargs
        super().__init__(*args, **kwargs)


class Aura(Buff):
    def __init__(self, *args, **kwargs):
        kwargs = dict(reason=ActionReason.AURA_BUFF) | kwargs
        super().__init__(*args, **kwargs)
