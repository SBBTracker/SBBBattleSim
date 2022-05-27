from sbbbattlesim import fight
from tests import make_character, make_player

def test_onstart_not_proc_merlin():
    player = make_player(
        characters=[
            make_character(id='GENERIC', position=1)
        ],
        hero='SBB_HERO_MERLIN',
        spells=[
            'SBB_SPELL_EARTHQUAKE'
        ]
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    fight(player, enemy)




    generic = player.characters.get(1)

    assert generic
    assert generic.attack == 1 and generic.health == 1


def test_onstart_not_proc_familar():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_WIZARD', position=1)
        ],
        spells=[
            'SBB_SPELL_EARTHQUAKE'
        ]
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=1)],
    )
    fight(player, enemy)




    cat = player.characters.get(1)

    assert cat
    assert cat.attack == 1 and cat.health == 1