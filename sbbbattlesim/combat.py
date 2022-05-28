import logging
import random
import sys
from functools import lru_cache

from sbbbattlesim.action import ActionReason
from sbbbattlesim.events import EventManager, EventStack
from sbbbattlesim.player import Player
from sbbbattlesim.stats import CombatStats, calculate_damage

sys.setrecursionlimit(500)

logger = logging.getLogger(__name__)

FRONT = (1, 2, 3, 4)
BACK = (5, 6, 7)


def fight(p1: Player, p2: Player, limit=-1):
    p1.opponent, p2.opponent = p2, p1

    attacker, defender = who_goes_first(p1, p2)
    first_attacker = attacker.id

    class FightEventManager(EventManager):
        def get(self, event):
            evts = p1._events.get(event, set()) | p2._events.get(event, set())
            evts_set = set(evts)
            processed_events = set()

            if not evts:
                return

            sorting_lambda = lambda x: (x.priority, getattr(x.manager, 'position', 0))
            evts = sorted(evts, key=sorting_lambda, reverse=True)

            priority = None

            while True:
                if not evts:
                    break

                evt = evts[0]
                evts = evts[1:]

                processed_events.add(evt)

                if priority is None:
                    priority = evt.priority
                elif evt.priority < priority:
                    priority = evt.priority
                elif evt.priority > priority:
                    continue

                yield evt

                new_evts_set = p1._events.get(event, set()) | p2._events.get(event, set())

                if evts_set != new_evts_set:
                    evts_set = set(new_evts_set) - processed_events
                    evts = sorted(evts_set, key=sorting_lambda, reverse=True)

                if not evts:
                    break

        def __call__(self, event, stack=None, *args, **kwargs):
            logger.debug(f'{self.pretty_print()} triggered event {event}')

            # If an event stack already exists use it otherwise make a new stack
            stack = stack or EventStack()

            if not p1._events.get(event, set()) | p2._events.get(event, set()):
                return stack

            with stack.open(*args, **kwargs) as executor:
                for evt in self.get(event):
                    logger.debug(f'Firing {evt} with {args} {kwargs}')
                    executor.execute(evt, *args, **kwargs)

            return stack

    fight_event_manager = FightEventManager()

    logger.debug('********************SETTING UP COMBAT')
    fight_event_manager('OnSetup')
    logger.debug('********************STARTING COMBAT')
    fight_event_manager('OnStart')

    turn = 0

    winner, loser = None, None

    while True:
        if (limit > -1 and turn >= limit) or turn >= 100:
            break

        # Try to figure out if there is a winner
        attacker_no_characters_left = not bool(attacker.valid_characters())
        defender_no_characters_left = not bool(defender.valid_characters())

        if attacker_no_characters_left and defender_no_characters_left:
            break
        elif attacker_no_characters_left:
            winner, loser = defender, attacker
            break
        elif defender_no_characters_left:
            winner, loser = attacker, defender
            break
        elif not (attacker.valid_characters(_lambda=lambda char: char.attack > 0) + defender.valid_characters(
                _lambda=lambda char: char.attack > 0)):
            break

        logger.debug(f'********************NEW ROUND OF COMBAT: turn={turn}')

        logger.info(f'Attacker {attacker.pretty_print()}')
        logger.info(f'Defender {defender.pretty_print()}')

        # Get Attacker
        attack_position = attacker.get_attack_slot()
        if attack_position is not None:
            attack(attacker=attacker, defender=defender, attack_position=attack_position)
        else:
            logger.debug(f'NO ATTACKER')

        turn += 1
        attacker, defender = defender, attacker

    p1.opponent, p2.opponent = None, None

    if winner:
        return CombatStats(
            win_id=winner.id,
            damage=calculate_damage(winner),
            first_attacker=first_attacker
        )
    else:
        return CombatStats(
            win_id=None,
            damage=0,
            first_attacker=first_attacker
        )

def who_goes_first(p1, p2):
    p1cnt = _who_goes_first(p1)
    p2cnt = _who_goes_first(p2)

    if p1cnt > p2cnt:
        attacking, defending = p1, p2
    elif p2cnt > p1cnt:
        defending, attacking = p1, p2
    else:
        attacking, defending = random.sample((p1, p2), 2)

    return attacking, defending


def _who_goes_first(player):
    HERMES_BOOTS = '''SBB_TREASURE_HERMES'BOOTS'''
    TIGER = '''SBB_HERO_THECOLLECTOR'''
    MIMIC = '''SBB_TREASURE_TREASURECHEST'''
    DRAC = '''SBB_HERO_DRACULA'''

    cnt = 0
    if player.hero.id == DRAC:
        cnt += 1

    if player.treasures.get(HERMES_BOOTS):
        cnt += 1
        if player.treasures.get(MIMIC):
            cnt += 1
        if player.hero.id == TIGER:
            cnt += 1

    return cnt


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
