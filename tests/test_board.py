
import sbbbattlesim


def test_convert_state_to_action_json():
    indata = {'2639D5BBF80FAC50': {'characters': [{'id': 'SBB_CHARACTER_LOBO', 'attack': 11, 'health': 15, 'golden': False, 'cost': 5, 'position': 6, 'tribes': ['evil', 'monster']}, {'id': 'SBB_CHARACTER_LOBO', 'attack': 10, 'health': 20, 'golden': False, 'cost': 5, 'position': 5, 'tribes': ['evil', 'monster']}, {'id': 'SBB_CHARACTER_MONSTERLORD', 'attack': 7, 'health': 7, 'golden': False, 'cost': 5, 'position': 2, 'tribes': ['evil', 'monster']}, {'id': 'SBB_CHARACTER_MONSTERLORD', 'attack': 22, 'health': 22, 'golden': True, 'cost': 5, 'position': 3, 'tribes': ['evil', 'monster']}, {'id': 'SBB_CHARACTER_MONSTERBOOK', 'attack': 14, 'health': 6, 'golden': True, 'cost': 4, 'position': 7, 'tribes': ['evil', 'monster']}, {'id': 'SBB_CHARACTER_PUMPKINKING', 'attack': 10, 'health': 10, 'golden': False, 'cost': 6, 'position': 1, 'tribes': ['evil', 'monster']}, {'id': 'SBB_CHARACTER_ECHOWOODSHAMBLER', 'attack': 1, 'health': 1, 'golden': False, 'cost': 6, 'position': 4, 'tribes': ['treant']}], 'treasures': ["SBB_TREASURE_MERLIN'SHAT", 'SBB_TREASURE_SPEAROFACHILLES', 'SBB_TREASURE_TREASURECHEST'], 'hero': 'SBB_HERO_HORDEDRAGON', 'spells': ['SBB_SPELL_FOG'], 'level': 0, 'hand': []}, '436AFEFE58201698': {'characters': [{'id': 'SBB_CHARACTER_KINGTREE', 'attack': 0, 'health': 20, 'golden': False, 'cost': 6, 'position': 4, 'tribes': ['evil', 'treant']}, {'id': 'SBB_CHARACTER_BURNINGTREE', 'attack': 10, 'health': 25, 'golden': False, 'cost': 5, 'position': 2, 'tribes': ['evil', 'treant']}, {'id': 'SBB_CHARACTER_KINGTREE', 'attack': 0, 'health': 40, 'golden': True, 'cost': 6, 'position': 3, 'tribes': ['evil', 'treant']}, {'id': 'SBB_CHARACTER_BURNINGTREE', 'attack': 10, 'health': 25, 'golden': False, 'cost': 5, 'position': 1, 'tribes': ['evil', 'treant']}, {'id': 'SBB_CHARACTER_ROBINWOOD', 'attack': 14, 'health': 20, 'golden': True, 'cost': 6, 'position': 5, 'tribes': ['good', 'treant']}, {'id': 'SBB_CHARACTER_ECHOWOODSHAMBLER', 'attack': 1, 'health': 1, 'golden': False, 'cost': 6, 'position': 7, 'tribes': ['treant']}, {'id': 'SBB_CHARACTER_ECHOWOODSHAMBLER', 'attack': 1, 'health': 1, 'golden': False, 'cost': 6, 'position': 6, 'tribes': ['treant']}], 'treasures': ['SBB_TREASURE_DRAGONNEST', 'SBB_TREASURE_HEXINGWAND', 'SBB_TREASURE_WHIRLINGBLADES'], 'hero': 'SBB_HERO_BIGDEAL', 'spells': [], 'level': 0, 'hand': []}}

    output = sbbbattlesim.Board(indata).to_state()
    assert sort_json(output) == sort_json(indata)


def sort_json(data):
    for player in data.values():
        player["characters"] = sorted(
            player["characters"],
            key=lambda x: x["position"]
        )
        for character in player["characters"]:
            character["tribes"] = sorted(character["tribes"])
    return data


