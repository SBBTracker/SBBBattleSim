import logging
import random
import sys
from functools import lru_cache, cache

sys.setrecursionlimit(500)

logger = logging.getLogger(__name__)


@lru_cache(maxsize=512)
def fight(attacker, defender, turn=0, **kwargs):
    logger.info(attacker)
    logger.info(defender)

    attacker.resolve_board()
    defender.resolve_board()

    # Get Attacker
    attack_character = attacker.attack_character
    if attack_character is not None:

        # Get valid defending
        valid_defenders = defender.front
        if getattr(attack_character, 'flying', False) and next((True for m in defender.back.values() if m is not None), False):
            valid_defenders = defender.back
        slot = random.choice(list({i for i, m in valid_defenders.items() if m is not None}))
        defend_character = defender.characters[slot]

        if defend_character is not None:
            # Run the attack
            attack(attacker=attacker, defender=defender, attack_character=attack_character,
                   defend_character=defend_character, **kwargs)

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


def attack(attack_character, defend_character, **kwargs):
    logger.info(f'{attack_character} -> {defend_character}')

    # Attack Event
    attack_character('Attack', **kwargs)

    # Defend Event
    defend_character('Defend', **kwargs)

    if 'ranged' not in attack_character.keywords:
        attack_character.health -= defend_character.attack
    defend_character.health -= attack_character.attack

    # SLAY TRIGGER
    if defend_character.dead:
        attack_character('Slay', **kwargs)

    # SURVIVED ATTACK TRIGGER
    else:
        defend_character('DamagedAndSurvived', **kwargs)

    # # DEATH TRIGGER
    # if attacker_dead:
    #     attack_character(Death, **event_kwargs)
    # if defender_dead:
    #     defend_character(Death, **event_kwargs)
    #
    # if attacker_dead:
    #     attack_character.owner.characters[attack_character.position] = None
    #     attack_character.owner.graveyard.append(attack_character)
    #
    # if defender_dead:
    #     defend_character.owner.characters[defend_character.position] = None
    #     defend_character.owner.graveyard.append(defend_character)

    resolve_damage(**kwargs)

def resolve_damage(attacker, defender, **kwargs):
    attack_action = attacker.resolve_damage()

    if attack_action is True:
        resolve_damage(attacker=defender, defender=attacker, **kwargs)
