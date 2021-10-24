import sys

import random
from functools import lru_cache

from sbbbattlesim.events import Attack, DamagedAndSurvived, Slay, Defend, Death

sys.setrecursionlimit(100)


@lru_cache(maxsize=512)
def fight(attacker, defender, turn=0):

    print(attacker)
    print(defender)

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
        defender_character = defender.characters[slot]

        if defender_character is not None:

            # Run the attack
            attack(attacker=attacker, defender=defender, attack_character=attack_character, defend_character=defender_character)

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


def attack(attack_character, defend_character, **event_kwargs):
    print(f'{attack_character} is attacking {defend_character}')

    # Attack Event
    attack_character(Attack, **event_kwargs)

    # Defend Event
    defend_character(Defend, **event_kwargs)

    if 'ranged' not in attack_character.keywords:
        attack_character.damage += defend_character.attack
    defend_character.damage += attack_character.attack

    attacker_dead = attack_character.dead()
    defender_dead = defend_character.dead()

    # SLAY TRIGGER
    if attacker_dead:
        attack_character(Slay, **event_kwargs)

    # SURVIVED ATTACK TRIGGER
    else:
        defend_character(DamagedAndSurvived, **event_kwargs)

    # LAST BREATH TRIGGER
    if attacker_dead:
        attack_character(Death, **event_kwargs)
    if defender_dead:
        defend_character(Death, **event_kwargs)

    if attacker_dead:
        attack_character.owner.characters[attack_character.position] = None
        attack_character.owner.graveyard.append(attack_character)

    if defender_dead:
        defend_character.owner.characters[defend_character.position] = None
        defend_character.owner.graveyard.append(defend_character)
