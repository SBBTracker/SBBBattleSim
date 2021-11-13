import logging
import random
import sys
from functools import lru_cache, cache

from sbbbattlesim.utils import StatChangeCause, Keyword, resolve_damage

sys.setrecursionlimit(500)

logger = logging.getLogger(__name__)

def fight_initialization(attacker, defender, limit=None, **kwargs):
    attacker.resolve_board()
    defender.resolve_board()

    ### TODO test who's events trigger in which order
    attacker('OnStart', **kwargs)
    defender('OnStart', **kwargs)

    return fight(attacker, defender, limit=limit, **kwargs)

@lru_cache(maxsize=512)
def fight(attacker, defender, turn=0, limit=None, **kwargs):

    if limit is not None:
        if turn > limit:
            return None, None

    logger.debug(f'********************NEW ROUND OF COMBAT: turn={turn}')

    attacker.resolve_board()
    defender.resolve_board()

    logger.info(f'Attacker {attacker}')
    logger.info(f'Defender {defender}')

    # Get Attacker
    attack_position = attacker.attack_slot
    if attack_position is not None:
        attack(attacker=attacker, defender=defender, attack_position=attack_position, **kwargs)
    else:
        logger.debug(f'NO ATTACKER')

    # Try to figure out if there is a winner
    attacker_no_characters_left = next((False for c in attacker.characters.values() if c is not None), True)
    defender_no_characters_left = next((False for c in defender.characters.values() if c is not None), True)

    if attacker_no_characters_left and defender_no_characters_left:
        return None, None
    elif attacker_no_characters_left:
        return defender, attacker
    elif defender_no_characters_left:
        return attacker, defender

    return fight(
        attacker=defender,
        defender=attacker,
        turn=turn+1
    )


def attack(attack_position, attacker, defender, **kwargs):
    attack_character = attacker.characters.get(attack_position)

    # Fliers target back first
    # everyone else targets front first
    front = (1, 2, 3, 4)
    back = (5, 6, 7)
    front_characters = defender.valid_characters(_lambda=lambda char: char.position in front)
    back_characters = defender.valid_characters(_lambda=lambda char: char.position in back)
    if Keyword.FLYING in attacker.characters.get(attack_position).keywords:
        if any(back_characters):
            valid_defenders = back_characters
        else:
            valid_defenders = front_characters
    else:
        if any(front_characters):
            valid_defenders = front_characters
        else:
            valid_defenders = back_characters

    logger.debug(f'VALID DEFENDERS ({valid_defenders})')

    if not valid_defenders:
        return

    defend_character = random.choice(valid_defenders)
    defend_position = defend_character.position

    # AFTER THIS POINT BOTH ATTACK AND DEFEND POSITION IS DEFINED
    # The characters in attack and defend slots may change after this point so
    # before each event attack_character and defend character is set again

    logger.info(f'{attacker.characters.get(attack_position)} -> {defender.characters.get(defend_position)}')

    # Pre Damage Event
    # These functions can change the characters in given positions like Medusa
    attack_character = attacker.characters.get(attack_position)
    if attack_character:
        attack_character('OnPreAttack', attack_position=attack_position, defend_position=defend_position, **kwargs)

    defend_character = defender.characters.get(defend_position)
    if defend_character:
        defender.characters.get(defend_position)('OnPreDefend', attack_position=attack_position, defend_position=defend_position, **kwargs)

    # We are pulling the latest attack_character and defend character incase they changed
    attack_character = attacker.characters.get(attack_position)
    defend_character = defender.characters.get(defend_position)

    if 'ranged' not in attack_character.keywords:
        attack_character.change_stats(damage=defend_character.attack, reason=StatChangeCause.DAMAGE_WHILE_ATTACKING, source=defend_character)
    defend_character.change_stats(damage=attack_character.attack, reason=StatChangeCause.DAMAGE_WHILE_DEFENDING, source=attack_character)

    # SLAY TRIGGER
    if defend_character.dead:
        attack_character('OnAttackAndKill', defend_character, **kwargs)

    # Post Damage Event
    attack_character('OnPostAttack', attack_position=attack_position, defend_position=defend_position, **kwargs)
    defend_character('OnPostDefend', attack_position=attack_position, defend_position=defend_position, **kwargs)

    resolve_damage(attacker=attacker, defender=defender, **kwargs)
    resolve_damage(attacker=defender, defender=attacker, **kwargs)
