import logging
import random
import sys
from functools import lru_cache

from sbbbattlesim.action import ActionReason

sys.setrecursionlimit(500)

logger = logging.getLogger(__name__)

FRONT = (1, 2, 3, 4)
BACK = (5, 6, 7)


def attack(attack_position, attacker, defender, **kwargs):
    attack_character = attacker.characters.get(attack_position)
    if attack_character is None:
        return

    front_characters = defender.valid_characters(_lambda=lambda char: char.position in FRONT and char is not attack_character)
    back_characters = defender.valid_characters(_lambda=lambda char: char.position in BACK and char is not attack_character)
    # Fliers target back first everyone else targets front first
    if attacker.characters.get(attack_position).flying:
        if any(back_characters):
            valid_defenders = back_characters
        else:
            valid_defenders = front_characters
    else:
        if any(front_characters):
            valid_defenders = front_characters
        else:
            valid_defenders = back_characters

    logger.debug(f'VALID DEFENDERS ({[valid.pretty_print() for valid in valid_defenders]})')

    if not valid_defenders:
        return

    defend_character = random.choice(valid_defenders)
    defend_position = defend_character.position

    # AFTER THIS POINT BOTH ATTACK AND DEFEND POSITION IS DEFINED
    # The characters in attack and defend slots may change after this point so
    # before each event attack_character and defend character is set again
    logger.info(f'{attack_character.pretty_print()} -> {defend_character.pretty_print()}')

    # Pre Damage Event
    # These functions can change the characters in given positions like Medusa
    attacker.characters.get(attack_position)('OnPreAttack', attack_position=attack_position, defend_position=defend_position, defend_player=defender, **kwargs)
    defender.characters.get(defend_position)('OnPreDefend', attack_position=attack_position, defend_position=defend_position, attack_player=attacker, **kwargs)

    # We are pulling the latest attack_character and defend character incase they changed
    attack_character = attacker.characters.get(attack_position)
    defend_character = defender.characters.get(defend_position)

    if attack_character is None or defend_character is None:
        return

    attacker_damage = defend_character.generate_attack(target=attack_character, source=defend_character, reason=ActionReason.DAMAGE_WHILE_DEFENDING, attacking=False)
    defender_damage = attack_character.generate_attack(target=defend_character, source=attack_character, reason=ActionReason.DAMAGE_WHILE_ATTACKING, attacking=True)

    if not attack_character.ranged:
        attacker_damage.execute()
    defender_damage.execute()

    if not attack_character.ranged:
        attacker_damage.resolve()

    # SLAY TRIGGER
    for _dc in defender_damage.targets:
        if _dc.dead:
            attack_character('OnAttackAndKill', killed_character=_dc, **kwargs)

    # for copycat to work properly
    attack_character('OnPostAttack', attack_position=attack_position, defend_position=defend_position, **kwargs)

    defender_damage.resolve()

    # for cupid to work properly
    defend_character('OnPostDefend', attack_position=attack_position, defend_position=defend_position, **kwargs)
