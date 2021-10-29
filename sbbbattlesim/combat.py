import logging
import random
import sys
from functools import lru_cache, cache

sys.setrecursionlimit(500)

logger = logging.getLogger(__name__)


@lru_cache(maxsize=512)
def fight(attacker, defender, turn=0, **kwargs):
    if turn == 0:
        attacker.opponent = defender
        defender.opponent = attacker

    attacker.resolve_board()
    defender.resolve_board()

    logger.info(f'Attacker {attacker}')
    logger.info(f'Defender {defender}')

    # Get Attacker
    attack_character = attacker.attack_character
    if attack_character is not None:


        # Get valid defending
        valid_defenders = defender.front
        if getattr(attack_character, 'flying', False) and next((True for m in defender.back.values() if m is not None), False):
            valid_defenders = defender.back
        valid_defenders = [m for m in valid_defenders.values() if m is not None]
        if not valid_defenders:
            valid_defenders = [m for m in defender.back.values() if m is not None]

        if valid_defenders:
            # Run the attack
            attack(
                attacker=attacker,
                defender=defender,
                attack_character=attack_character,
                defend_character=random.choice(valid_defenders),
                **kwargs
            )

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


def attack(attack_character, defend_character, attacker, defender, **kwargs):
    logger.info(f'{attack_character} -> {defend_character}')

    # Attack Event
    attack_character('OnAttack', **kwargs)

    # Defend Event
    defend_character('OnDefend', **kwargs)

    if 'ranged' not in attack_character.keywords:
        attack_character.damage += defend_character.attack
    defend_character.damage += attack_character.attack

    # SLAY TRIGGER
    if defend_character.dead:
        attack_character('OnAttackAndKill', **kwargs)

    # SURVIVED ATTACK TRIGGER
    else:
        defend_character('OnDamagedAndSurvived', **kwargs)

    resolve_damage(attacker=attacker, defender=defender, **kwargs)
    resolve_damage(attacker=defender, defender=attacker, **kwargs)


def resolve_damage(attacker, defender, **kwargs):
    attack_action = attacker.resolve_damage()

    if attack_action is True:
        resolve_damage(attacker=defender, defender=attacker, **kwargs)
