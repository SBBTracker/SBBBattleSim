import logging
import random
import sys
from functools import lru_cache, cache

from sbbbattlesim.utils import StatChangeCause

sys.setrecursionlimit(500)

logger = logging.getLogger(__name__)

def fight_initialization(attacker, defender, **kwargs):
    attacker.resolve_board()
    defender.resolve_board()

    ### TODO test who's events trigger in which order
    attacker('OnStart', **kwargs)
    defender('OnStart', **kwargs)

    return fight(attacker, defender, **kwargs)

@lru_cache(maxsize=512)
def fight(attacker, defender, turn=0, **kwargs):

    logger.debug(f'********************NEW ROUND OF COMBAT: turn={turn}')

    attacker.resolve_board()
    defender.resolve_board()

    logger.info(f'Attacker {attacker}')
    logger.info(f'Defender {defender}')

    # Get Attacker
    attack_character = attacker.attack_character
    if attack_character is not None:
        attack(attacker=attacker, defender=defender, attack_character=attack_character, **kwargs )

    # Try to figure out if there is a winner
    attacker_no_characters_left = next((False for c in attacker.characters.values() if c is not None), True)
    defender_no_characters_left = next((False for c in defender.characters.values() if c is not None), True)

    if attacker_no_characters_left and defender_no_characters_left:
        return None
    elif attacker_no_characters_left:
        return defender.id
    elif defender_no_characters_left:
        return attacker.id

    return fight(
        attacker=defender,
        defender=attacker,
        turn=turn+1
    )


def attack(attack_character, attacker, defender, **kwargs):
    # Get valid defending
    defender_positions = (1, 2, 3, 4)
    if getattr(attack_character, 'flying', False) and next((True for m in defender.back.values() if m is not None), False):
        defender_positions = (5, 6, 7)
    valid_defenders = defender.valid_characters(_lambda=lambda char: char != attack_character and char.position in defender_positions)

    if not valid_defenders:
        return

    defend_character = random.choice(valid_defenders)

    logger.info(f'{attack_character} -> {defend_character}')

    # Attack Event
    attack_character('OnAttack', attack_character=attack_character, defend_character=defend_character, **kwargs)

    # Defend Event
    defend_character('OnDefend', attack_character=attack_character, defend_character=defend_character, **kwargs)

    if 'ranged' not in attack_character.keywords:
        attack_character.change_stats(damage=defend_character.attack, reason=StatChangeCause.DAMAGE_WHILE_ATTACKING)
    defend_character.change_stats(damage=attack_character.attack, reason=StatChangeCause.DAMAGE_WHILE_DEFENDING)

    # SLAY TRIGGER
    if defend_character.dead:
        attack_character('OnAttackAndKill', **kwargs)

    resolve_damage(attacker=attacker, defender=defender, **kwargs)
    resolve_damage(attacker=defender, defender=attacker, **kwargs)


def resolve_damage(attacker, defender, **kwargs):
    logger.debug(f'Resolving Damage for {attacker.id}')
    attack_action = attacker.resolve_damage()

    if attack_action is True:
        resolve_damage(attacker=defender, defender=attacker, **kwargs)
