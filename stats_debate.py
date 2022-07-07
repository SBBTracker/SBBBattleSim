import collections
import json
import math

from sbbbattlesim import simulate, configure_logging, from_state, fight
from sbbbattlesim.player import Player
from tests.test_simulate import MockLogObject

if __name__ == '__main__':
    configure_logging()

    fake_state = {
        'IDK Some Loser': [
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_THEGREATANDPOWERFUL',
                cardattack='124',
                cardhealth='132',
                is_golden=False,
                cost='6',
                slot='0',  # This is to make sure it does the proper correction
                subtypes=['mage']
            ),
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_THEGREATANDPOWERFUL',
                cardattack='112',
                cardhealth='112',
                is_golden=False,
                cost='6',
                slot='1',  # This is to make sure it does the proper correction
                subtypes=['mage']
            ),
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_WRETCHEDMUMMY',
                cardattack='39',
                cardhealth='30',
                is_golden=False,
                cost='4',
                slot='2',  # This is to make sure it does the proper correction
                subtypes=['evil', 'monster']
            ),
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_ROTTENAPPLETREE',
                cardattack='8',
                cardhealth='26',
                is_golden=False,
                cost='5',
                slot='3',  # This is to make sure it does the proper correction
                subtypes=['evil', 'treant']
            ),
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_LOBO',
                cardattack='41',
                cardhealth='41',
                is_golden=False,
                cost='5',
                slot='4',  # This is to make sure it does the proper correction
                subtypes=['evil', 'monster']
            ),
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_KINGTREE',
                cardattack='37',
                cardhealth='79',
                is_golden=True,
                cost='6',
                slot='5',  # This is to make sure it does the proper correction
                subtypes=['evil', 'treant']
            ),
            MockLogObject(
                zone='Character',
                content_id='''SBB_CHARACTER_WIZARD'SFAMILIAR''',
                cardattack='104',
                cardhealth='104',
                is_golden=True,
                cost='2',
                slot='6',  # This is to make sure it does the proper correction
                subtypes=['animal', 'mage']
            ),
            # MockLogObject(
            #     zone='Treasure',
            #     content_id='SBB_TREASURE_HELMOFTHEUGLYGOSLING',
            # ),
            # MockLogObject(
            #     zone='Treasure',
            #     content_id='SBB_TREASURE_TREASURECHEST',
            # ),
            # MockLogObject(
            #     zone='Treasure',
            #     content_id='SBB_TREASURE_IVORYOWL',
            # ),
            # MockLogObject(
            #     zone='Hero',
            #     content_id='SBB_HERO_DRACULA',
            # ),
            # MockLogObject(
            #     zone='Spell',
            #     content_id='SBB_SPELL_BEASTWITHIN',
            # ),
        ],
        'Imoartel': [
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_MEDUSA',
                cardattack='13',
                cardhealth='11',
                is_golden=False,
                cost='4',
                slot='0',  # This is to make sure it does the proper correction
                subtypes=['evil', 'monster']
            ),
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_MEDUSA',
                cardattack='15',
                cardhealth='15',
                is_golden=True,
                cost='4',
                slot='5',  # This is to make sure it does the proper correction
                subtypes=['evil', 'monster']
            ),
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_ROTTENAPPLETREE',
                cardattack='1',
                cardhealth='19',
                is_golden=False,
                cost='5',
                slot='6',  # This is to make sure it does the proper correction
                subtypes=['evil', 'treant']
            ),
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_ROTTENAPPLETREE',
                cardattack='4',
                cardhealth='53',
                is_golden=False,
                cost='5',
                slot='3',  # This is to make sure it does the proper correction
                subtypes=['evil', 'treant']
            ),
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_MEDUSA',
                cardattack='14',
                cardhealth='14',
                is_golden=True,
                cost='4',
                slot='4',  # This is to make sure it does the proper correction
                subtypes=['evil', 'monster']
            ),
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_PUMPKINKING',
                cardattack='31',
                cardhealth='31',
                is_golden=True,
                cost='6',
                slot='2',  # This is to make sure it does the proper correction
                subtypes=['evil', 'monster']
            ),
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_MONSTERLORD',
                cardattack='21',
                cardhealth='21',
                is_golden=False,
                cost='6',
                slot='1',  # This is to make sure it does the proper correction
                subtypes=['evil', 'monster']
            ),
            MockLogObject(
                zone='Treasure',
                content_id='SBB_TREASURE_SPEAROFACHILLES',
            ),
            # MockLogObject(
            #     zone='Treasure',
            #     content_id='SBB_TREASURE_SUMMONINGCIRCLE',
            # ),
            # MockLogObject(
            #     zone='Treasure',
            #     content_id='SBB_TREASURE_PHOENIXFEATHER',
            # ),
            # MockLogObject(
            #     zone='Hero',
            #     content_id='SBB_HERO_DRACULA',
            # ),
            MockLogObject(
                zone='Spell',
                content_id='SBB_SPELL_POISONAPPLE',
            ),
        ]
    }

    threads, simulations = 8, 1000
    sim_stats = simulate(fake_state, t=threads, k=simulations)

    win_rate = collections.defaultdict(int)
    win_rate_per_first_attacker_per_attack_position = {
        pid: {
            i: collections.defaultdict(int) for i in range(1, 5)
        } for pid in sim_stats.adv_stats.keys()
    }
    for result in sim_stats.results:
        win_rate[result.win_id] += 1

        first_defender_id = list(set(result.adv_stats.keys()) - set(result.first_attacker))[0]
        first_defender_position = result.adv_stats[first_defender_id]['first_defender_position']
        win_rate_per_first_attacker_per_attack_position[result.first_attacker][first_defender_position][result.win_id] += 1

    parsed_state = from_state(fake_state)
    players = [Player(id=i, **d) for i, d in parsed_state.items()]

    for player in players:
        print(player.id)
        for char in player.valid_characters():
            print(char.pretty_print())
        print('')

    for wid, wins in win_rate.items():
        print(wid, f'{round((wins/(threads * simulations)) * 100, 2)}%')

    # print(json.dumps(sim_stats.adv_stats, indent=4))
    print(json.dumps(win_rate_per_first_attacker_per_attack_position, indent=4))




    # combat_result = fight(*players)
