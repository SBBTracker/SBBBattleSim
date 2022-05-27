import collections
import enum
import logging
import typing
from dataclasses import dataclass
from enum import Enum
from typing import List
import inspect

from sbbbattlesim.events import Event
from sbbbattlesim.record import Record

logger = logging.getLogger(__name__)


class ActionState(Enum):
    CREATED = 1
    EXECUTED = 2
    RESOLVED = 3
    ROLLED_BACK = 4


class ActionReason(enum.Enum):
    TEST = -1
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
    BOSSY_BUFF = 146
    TWEEDLEDEE_BUFF = 147
    JORM_ON_SLAY_BUFF = 148
    BURNING_TREE_BUFF = 149
    WATER_WRAITH_BUFF = 150

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
    CURSED_THRONE = 245

    EVELLA_BASE_BUFF = 301
    EVELLA_ANIMAL_BUFF = 301
    MERLIN_BUFF = 302
    POTION_MASTER_BUFF = 303
    GEPPETTO_BUFF = 304
    JACKS_GIANT_BUFF = 305
    MRS_CLAUS_BUFF = 306
    FATES_BUFF = 307
    KRAMPUS_BUFF = 308
    CHARON_BUFF = 309
    SAD_DRACULA_SLAY = 310
    MIHRI_BUFF = 311
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
    FOG = 457

    COPYCAT_PROC = 501
    MEURTE_PROC = 502
    TROPHY_HUNTER_PROC = 503


class Action:
    def __init__(
            self,
            reason: ActionReason,
            source: ('Character', 'Treasure', 'Hero', 'Spell'),
            targets: (typing.List['Character'], None) = None,
            _lambda=None,
            priority: int = 0,
            multiplier: int = 1,
            attack: int = 0,
            health: int = 0,
            damage: int = 0,
            heal: int = 0,
            event: (Event, None) = None,
            _action=None,
            temp: bool = False,
            *args,
            **kwargs
    ):
        self.reason = reason
        self.source = source
        self.targets = targets or []
        self._lambda = _lambda or (lambda _: True)
        self._action = _action
        self.priority = priority
        self.multiplier = multiplier
        self.temp = temp

        self.attack = attack * self.multiplier
        self.health = health * self.multiplier
        self.damage = damage
        self.heal = heal

        self.event = event

        self.args = args
        self.kwargs = kwargs

        self.state = ActionState.CREATED
        self._char_buffer = set()
        self._killed_char_buffer = set()
        self._event_buffer = collections.defaultdict(list)

        logger.debug(f'New {self} atk={self.attack} hp={self.health} dmg={self.damage} heal={self.heal} temp={self.temp} from_event_aura={self.event is not None}')

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'{self.reason} {self.source.pretty_print()}'

    def _apply(self, char, *args, **kwargs):
        '''
        This is the core of any Action class and should not be touched unless you are making changes to ALL effects
        This should never be accessed outside an Action class or subclass
        '''
        if self.attack != 0 or self.health != 0:
            char._base_attack += self.attack
            char._base_health += self.health

            # TRIGGER ON BUFF
            char('OnBuff', reason=self.reason, source=self.source, attack=self.attack * char.attack_multiplier,
                 health=self.health, *args, **kwargs)

        if self.damage > 0:
            if char.invincible and self.reason != ActionReason.DAMAGE_WHILE_DEFENDING:
                char('OnDamagedAndSurvived', damage=0, *args, **kwargs)
                return
            char._damage += self.damage

        if self.heal > 0 or self.heal == -1:
            char._damage = 0 if self.heal == -1 else max(char._damage - self.heal, 0)

        if self.damage or self.health:
            if char.health <= 0:
                char.dead = True
                logger.debug(f'{char.pretty_print()} marked for death in execution')
            elif self.damage > 0:
                char('OnDamagedAndSurvived', damage=self.damage, *args, **kwargs)

    def _clear(self, char, *args, **kwargs):
        '''
        This is the core function to specify how to reverse an action and should not be touched unless you are making changes to ALL effects
        This should never be accessed outside an Action class or subclass
        '''
        logger.debug(f'Clearing char {char.pretty_print()}')
        if self.health != 0:
            logger.debug(f'health to clear: {self.health} ; damage {char._damage} ; health {char._base_health}')
            char._damage -= min(char._damage, self.health)
            char._base_health -= self.health
            logger.debug(f'health after clear: {self.health} ; damage {char._damage} ; health {char._base_health}')

            if char.health <= 0:
                char.dead = True
                logger.debug(f'{char.pretty_print()} marked for death B')
                self._killed_char_buffer.add(char)

        if self.attack != 0:
            char._base_attack -= self.attack

        char('OnBuff', reason=self.reason, source=self.source, attack=-1*self.attack,
             health=-1*self.health)

        logger.debug(f'finished clearing char {char.pretty_print()}')

    def _register(self, char, *args, **kwargs):
        if not self.event:
            return

        # Apply Events
        for _ in range(self.multiplier):
            registered = char.register(self.event, priority=self.priority, source=self.source, *args, **kwargs)
            self._event_buffer[char].append(registered)

    def _unregister(self, char, *args, **kwargs):
        if not self.event:
            return

        # Unregister Events
        events = self._event_buffer[char]
        for e in events:
            char.unregister(e)

    def execute(self, *characters, **kwargs):
        setup = kwargs.get('setup', False)
        logger.debug(f'{self} execute ({characters}, {kwargs})')
        for char in characters or self.targets:
            if not self._lambda(char) or char in self._char_buffer:
                continue

            args = self.args
            kwargs = self.kwargs | kwargs
            self._char_buffer.add(char)
            char._action_history.append(self)

            if self.event:
                self._register(char, *args, **kwargs)
            if not setup and any(v != 0 for v in (self.attack, self.health, self.damage, self.heal)):
                self._apply(char, *args, **kwargs)

            if callable(self._action):
                self._action(char)

        self.state = ActionState.EXECUTED
        return self

    def update(self, attack=0, health=0, targets=None, *args, **kwargs):
        logger.debug(f'{self} updating (attack={attack}, health={health}) >>> {targets} ({args}, {kwargs})')
        args = (*self.args, *args)
        kwargs = self.kwargs | kwargs

        self.attack += attack
        self.health += health

        if attack != 0 or health != 0:
            for char in self._char_buffer:
                char._base_attack += attack
                char._base_health += health
                char('OnBuff', reason=self.reason, source=self.source, attack=attack * char.attack_multiplier,
                     health=health, *args, **kwargs)

        return self

    def roll_back(self, *characters, **kwargs):
        char_iter = characters or self._char_buffer.copy()
        logger.debug(f'{self} rolling back >>> {[char.pretty_print() for char in char_iter]}')
        for char in char_iter:
            if char not in self._char_buffer:
                continue
            self._char_buffer.remove(char)
            self._killed_char_buffer.add(char)

            args = self.args
            kwargs = self.kwargs | kwargs

            if self.event:
                self._unregister(char, *args, **kwargs)
            if any(v != 0 for v in (self.attack, self.health, self.damage, self.heal)):
                self._clear(char, *args, **kwargs)

        self.handle_deaths(*characters)
        self.state = ActionState.ROLLED_BACK

    def resolve(self):
        if self.state in (ActionState.CREATED, ActionState.ROLLED_BACK):
            self.execute()
        elif self.state in (ActionState.RESOLVED,):
            logger.debug(f'{self} ALREADY RESOLVED')
            return

        logger.debug(f'RESOLVING DAMAGE FOR {self}')
        self.handle_deaths()
        self.state = ActionState.RESOLVED

    def handle_deaths(self, *characters):
        char_iter = set(characters) or self._char_buffer.copy()
        dead_character_dict = collections.defaultdict(list)
        for char in char_iter | self._killed_char_buffer:
            if char.dead and char not in char.player.graveyard:
                dead_character_dict[char.player].append(char)
        self._char_buffer = self._char_buffer - char_iter

        if dead_character_dict:
            char_ls = [self.source.player, self.source.player.opponent]
            for player in char_ls:
                if player in dead_character_dict:
                    dead_characters = dead_character_dict[player]
                    player.despawn(*sorted(dead_characters, key=lambda _char: _char.position, reverse=True), reason=self.reason)


class Damage(Action):
    def __init__(self, temp=False, *args, **kwargs):
        super().__init__(temp=False, *args, **kwargs)


class Heal(Action):
    def __init__(self, temp=False, *args, **kwargs):
        super().__init__(temp=False, *args, **kwargs)


class Buff(Action):
    def __init__(self, temp=False, *args, **kwargs):
        super().__init__(temp=temp, *args, **kwargs)


class Support(Buff):
    def __init__(self, source=None, attack: int = 0, health: int = 0, *args, **kwargs):
        kwargs = dict(reason=ActionReason.SUPPORT_BUFF, temp=True) | kwargs
        multiplier = source.player.support_itr

        if source.player.hero.id == 'SBB_HERO_GANDALF':
            attack += 2
            health += 1

        super().__init__(multiplier=multiplier, source=source, attack=attack, health=health, *args, **kwargs)


class Aura(Buff):
    def __init__(self, *args, **kwargs):
        kwargs = dict(reason=ActionReason.AURA_BUFF, temp=True) | kwargs

        super().__init__(*args, **kwargs)

