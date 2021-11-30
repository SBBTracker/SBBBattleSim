import enum
import logging
import random
from sbbbattlesim.spells import registry as spell_registry

logger = logging.getLogger(__name__)


LOKI_SPELLS = (
    '''SBB_SPELL_TESTYOURMIGHT''',  # Magic Research
    '''SBB_SPELL_SUGARANDSPICE''',  # Sugar and Spice
    '''SBB_SPELL_WITCHS'SBREW''',  # Witch's Brew
    '''SBB_SPELL_DRINKMEPOTION''',  # Luna's Grace
    '''SBB_SPELL_SAPMAGIC''',  # Flourish
    '''SBB_SPELL_MONSTERMASH''',  # Worm Root
    '''SBB_SPELL_BELLE'SINFLUENCE''',  # Beauty's Influence
    '''SBB_SPELL_FLAMINGAURA''',  # Burning Palm
    '''SBB_SPELL_STONESKIN''',  # Stoneskin
    '''SBB_SPELL_MERLIN'SHAT''',  # Merlin's Test
    '''SBB_SPELL_ROYALPOWER''',  # Queen's Grace
    '''SBB_SPELL_GIGANTIFY''',  # Gigantify
    '''SBB_SPELL_HUGEIFY''',  # Hugeify
    '''SBB_SPELL_KNIGHTHOOD''',  # Knighthood
    '''SBB_SPELL_TESTYOURMIGHT''',  # Evil Twin
)
#combat spells could be used and shared between deck, book of merlin and monster book
COMBAT_SPELLS = (
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

START_OF_FIGHT_SPELLS = (
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
    '''SBB_SPELL_BEASTWITHIN''',
    '''SBB_SPELL_MENAGRIE'''

)

class Tribe(enum.Enum):
    ANIMAL = 'animal'
    DRAGON = 'dragon'
    DWARF = 'dwarf'
    EGG = 'egg'
    FAIRY = 'fairy'
    MAGE = 'mage'
    MONSTER = 'monster'
    PRINCE = 'prince'
    PRINCESS = 'princess'
    PUFF_PUFF = 'puff'
    QUEEN = 'queen'
    TREANT = 'treant'

    GOOD = 'good'
    EVIL = 'evil'


class Keyword(enum.Enum):
    SUPPORT = 'support'
    FLYING = 'flying'
    SLAY = 'slay'
    LAST_BREATH = 'last breath'
    RANGED = 'ranged'
    QUEST = 'quest'


class StatChangeCause(enum.Enum):
    DAMAGE_WHILE_ATTACKING = 1
    DAMAGE_WHILE_DEFENDING = 2
    SUPPORT_BUFF = 3
    AURA_BUFF = 4
    SLAY = 5

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

    SMITE = 450
    EARTHQUAKE = 451
    SHRIVEL = 452
    FALLING_STARS = 453
    FIREBALL = 454
    LIGHTNING_BOLT = 455
    POISON_APPLE = 456


def get_support_targets(position, horn=False):
    if horn:
        return [1, 2, 3, 4]
    return {
        5: (1, 2),
        6: (2, 3),
        7: (3, 4)
    }.get(position, ())


def get_behind_targets(position):
    return {
        1: (5, ),
        2: (5, 6),
        3: (6, 7),
        4: (7, )
    }.get(position, ())


def get_spawn_positions(position):
    spawn_order = {
        1: (1, 2, 3, 4, 5, 6, 7),
        2: (2, 3, 4, 1, 5, 6, 7),
        3: (3, 4, 2, 1, 5, 6, 7),
        4: (4, 3, 2, 1, 5, 6, 7),
        5: (5, 6, 7, 2, 1, 3, 4),
        6: (6, 7, 5, 3, 2, 1, 4),
        7: (7, 6, 5, 4, 3, 1, 2)
    }

    return spawn_order.get(position, ())


def random_combat_spell(level):
    valid_spells = [*spell_registry.filter(_lambda=lambda spell_cls: spell_cls._level <= level and spell_cls.id in COMBAT_SPELLS)]
    if valid_spells:
        return random.choice(valid_spells)


#TODO are these the same across different effects (robin wood, helm of the gosling, juliets in graveyards)
# or do they behaave differently. Set up resources with tied attack and different cost, and tied attack&cost but different
# position and do so for both weaker and stronger style effects
def find_stat_extreme_character(player, strongest=True):
    # If there are no valid characters,  return nothing
    valid_characters = player.valid_characters()
    if not valid_characters:
        return None

    func = max if strongest else min
    sub_char = func(valid_characters, key=lambda char: (char.attack, char.cost))
    sub_chars = list(filter(lambda char: char.attack == sub_char.attack and char.cost == sub_char.cost, valid_characters))
    return random.choice(sub_chars)


def find_strongest_character(player):
    return find_stat_extreme_character(player, strongest=True)


def find_weakest_character(player):
    return find_stat_extreme_character(player, strongest=False)


# DO NOT DO THIS
# TODO Summon random character with conditions
# DO NOT DO THIS
