import json
import os.path
import re

if __name__ == '__main__':

    card_info_base = json.load(open(os.path.join(os.path.dirname(__file__), 'sbbbattlesim', 'card_info.json')))

    card_info = {}
    for id, card in card_info_base.items():
        card['golden'] = True if re.search('GOLDEN_', id, re.I) else False
        card['Subtypes'] = [st for st in card['Subtypes'] if st]
        card['Keywords'] = [kw for kw in card['Keywords'] if kw]
        card_info[id] = card

    json.dump(card_info, open(os.path.join(os.path.dirname(__file__), 'sbbbattlesim', 'card_info.json'), 'w+'), indent=4)