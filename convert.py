j = {'2639D5BBF80FAC50': {'characters': [{'id': 'SBB_CHARACTER_LOBO', 'attack': 11, 'health': 15, 'golden': False, 'cost': 5, 'position': 6, 'tribes': ['evil', 'monster']}, {'id': 'SBB_CHARACTER_LOBO', 'attack': 10, 'health': 20, 'golden': False, 'cost': 5, 'position': 5, 'tribes': ['evil', 'monster']}, {'id': 'SBB_CHARACTER_MONSTERLORD', 'attack': 7, 'health': 7, 'golden': False, 'cost': 5, 'position': 2, 'tribes': ['evil', 'monster']}, {'id': 'SBB_CHARACTER_MONSTERLORD', 'attack': 22, 'health': 22, 'golden': True, 'cost': 5, 'position': 3, 'tribes': ['evil', 'monster']}, {'id': 'SBB_CHARACTER_MONSTERBOOK', 'attack': 14, 'health': 6, 'golden': True, 'cost': 4, 'position': 7, 'tribes': ['evil', 'monster']}, {'id': 'SBB_CHARACTER_PUMPKINKING', 'attack': 10, 'health': 10, 'golden': False, 'cost': 6, 'position': 1, 'tribes': ['evil', 'monster']}, {'id': 'SBB_CHARACTER_ECHOWOODSHAMBLER', 'attack': 1, 'health': 1, 'golden': False, 'cost': 6, 'position': 4, 'tribes': ['treant']}], 'treasures': ["SBB_TREASURE_MERLIN'SHAT", 'SBB_TREASURE_SPEAROFACHILLES', 'SBB_TREASURE_TREASURECHEST'], 'hero': 'SBB_HERO_HORDEDRAGON', 'spells': ['SBB_SPELL_FOG'], 'level': 0, 'hand': []}, '436AFEFE58201698': {'characters': [{'id': 'SBB_CHARACTER_KINGTREE', 'attack': 0, 'health': 20, 'golden': False, 'cost': 6, 'position': 4, 'tribes': ['evil', 'treant']}, {'id': 'SBB_CHARACTER_BURNINGTREE', 'attack': 10, 'health': 25, 'golden': False, 'cost': 5, 'position': 2, 'tribes': ['evil', 'treant']}, {'id': 'SBB_CHARACTER_KINGTREE', 'attack': 0, 'health': 40, 'golden': True, 'cost': 6, 'position': 3, 'tribes': ['evil', 'treant']}, {'id': 'SBB_CHARACTER_BURNINGTREE', 'attack': 10, 'health': 25, 'golden': False, 'cost': 5, 'position': 1, 'tribes': ['evil', 'treant']}, {'id': 'SBB_CHARACTER_ROBINWOOD', 'attack': 14, 'health': 20, 'golden': True, 'cost': 6, 'position': 5, 'tribes': ['good', 'treant']}, {'id': 'SBB_CHARACTER_ECHOWOODSHAMBLER', 'attack': 1, 'health': 1, 'golden': False, 'cost': 6, 'position': 7, 'tribes': ['treant']}, {'id': 'SBB_CHARACTER_ECHOWOODSHAMBLER', 'attack': 1, 'health': 1, 'golden': False, 'cost': 6, 'position': 6, 'tribes': ['treant']}], 'treasures': ['SBB_TREASURE_DRAGONNEST', 'SBB_TREASURE_HEXINGWAND', 'SBB_TREASURE_WHIRLINGBLADES'], 'hero': 'SBB_HERO_BIGDEAL', 'spells': [], 'level': 0, 'hand': []}}

import sbbbattlesim

board = sbbbattlesim.Board(j)

j2 = board.to_state()




def convert(board):
    converted_board = dict()

    for player, details in board.items():
        converted_details = dict()
        converted_details['treasures'] = [
            {
                "content_id": treasure,
                "playerid": player
            }
            for treasure in details['treasures']
        ]

        converted_details['characters'] = [
            {
                'slot': str(character['position'] - 1),
                'content_id': character,
                'cardattack': character['attack'],
                'cardhealth': character['health'],
                'is_golden': character['golden'],
                'cost': character['cost'],
                'subtypes': character['tribes'],  # NOTE, does this get us the capitalization we desire?,
                'playerid': player,
            }
            for character in details['characters']
        ]

        converted_details['hero'] = {
            'hero': details['hero'],
            'playerid': player,
            'content_id': details['hero'],
        }

        converted_details['spells'] = [
             {
                 "playerid": player,
                 "content_id": spell
             }
             for spell in details['spells']
        ]

        converted_board[player] = converted_details

    return converted_board

print(convert(j2))
