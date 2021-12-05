import logging
import random
import sys
from functools import lru_cache

from sbbbattlesim.damage import Damage
from sbbbattlesim.utils import StatChangeCause

sys.setrecursionlimit(500)

logger = logging.getLogger(__name__)


@lru_cache(maxsize=512)
def fight(attacker, defender, turn=0, limit=-1, **kwargs):
    if limit > -1 and turn >= limit:
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
    attacker_no_characters_left = not bool(attacker.valid_characters())
    defender_no_characters_left = not bool(defender.valid_characters())

    if attacker_no_characters_left and defender_no_characters_left:
        return None, None
    elif attacker_no_characters_left:
        return defender, attacker
    elif defender_no_characters_left:
        return attacker, defender
    elif not (attacker.valid_characters(_lambda=lambda char: char.attack > 0) + defender.valid_characters(_lambda=lambda char: char.attack > 0)):
        return None, None

    return fight(
        attacker=defender,
        defender=attacker,
        turn=turn+1,
        limit=limit
    )


def attack(attack_position, attacker, defender, **kwargs):
    # Fliers target back first
    # everyone else targets front first
    front = (1, 2, 3, 4)
    back = (5, 6, 7)

    attack_char = attacker.characters.get(attack_position)
    front_characters = defender.valid_characters(_lambda=lambda char: char.position in front and char is not attack_char)
    back_characters = defender.valid_characters(_lambda=lambda char: char.position in back and char is not attack_char)
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

    logger.info(f'{attacker.characters.get(attack_position).pretty_print()} -> {defender.characters.get(defend_position).pretty_print()}')

    # Pre Damage Event
    # These functions can change the characters in given positions like Medusa
    attack_character = attacker.characters.get(attack_position)
    if attack_character:
        attack_character('OnPreAttack', attack_position=attack_position, defend_position=defend_position, defend_player=defender, **kwargs)

    defend_character = defender.characters.get(defend_position)
    if defend_character:
        defender.characters.get(defend_position)('OnPreDefend', attack_position=attack_position, defend_position=defend_position, attack_player=attacker, **kwargs)

    # We are pulling the latest attack_character and defend character incase they changed
    attack_character = attacker.characters.get(attack_position)
    defend_character = defender.characters.get(defend_position)

    if not attack_character.ranged:
        attacker_damage = Damage(
            x=defend_character.attack,
            reason=StatChangeCause.DAMAGE_WHILE_ATTACKING,
            source=defend_character,
            targets=[attack_character]
        )

    defender_damage = Damage(
        x=attack_character.attack,
        reason=StatChangeCause.DAMAGE_WHILE_DEFENDING,
        source=attack_character,
        targets=[defend_character]
    )

    # SLAY TRIGGER
    if defend_character.dead:
        attack_character('OnAttackAndKill', killed_character=defend_character, **kwargs)

    if not attack_character.ranged:
        attacker_damage.resolve()
    defender_damage.resolve()

    # Post Damage Event
    attack_character('OnPostAttack', attack_position=attack_position, defend_position=defend_position, **kwargs)
    defend_character('OnPostDefend', attack_position=attack_position, defend_position=defend_position, **kwargs)
