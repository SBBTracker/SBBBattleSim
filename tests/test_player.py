from sbbbattlesim import configure_logging
from sbbbattlesim.characters import Character
from sbbbattlesim.treasures import Treasure
from tests import make_player, make_character


configure_logging()


def test_player():
    make_player()


def test_full_player():
    make_player(
        id='Hello',
        hero='world',
        characters=[make_character(position=i) for i in range(1, 8)],
        treasures=['one', 'two', 'three'],
        spells=['fireball', 'lightning_bolt']
    )


def test_player_replace_hero():
    player = make_player(hero='TEST_HERO')

    replace_id = 'SBB_HERO_SIRPIPS-A-LOT'
    player.replace_hero(replace_id)

    assert player.hero.id == replace_id


def test_player_add_character_board():
    player = make_player(hero='TEST_HERO')

    for i in range(1, 8):
        player.add_character(make_character(position=i))
        assert player.characters[i] is not None

    #TODO Should this move the character back to the hand or raise an error?
    position_five = player.characters[5]
    player.add_character(make_character(position=5))

    assert player.characters[5] is not position_five

    #TODO make a test for specific updates I.E. Riverwish placed on the board when you have Cloak of the Assassin


def test_player_remove_character_board():
    player = make_player(hero='TEST_HERO')

    for i in range(1, 8):
        player.add_character(make_character(position=i))
        assert player.characters[i] is not None

    player.remove_character(5)
    assert player.characters[5] is None

    #TODO make a test for specific updates I.E. Riverwish removed from the board when you have Cloak of the Assassin


def test_player_add_character_hand():
    player = make_player(hero='TEST_HERO')

    player.add_character_to_hand(make_character(position=4))

    assert len(player.hand) > 0
    assert isinstance(player.hand[0], Character), player.hand
    assert player.hand[0].position == 4
    assert player.characters[4] is None


def test_player_remove_character_hand():
    player = make_player(hero='TEST_HERO')

    character = player.add_character_to_hand(make_character(position=4))
    # TODO Should `Player.add_character_to_hand` return the charater object so it can be used to do player.hand.remove(character)?

    assert len(player.hand) > 0
    assert isinstance(player.hand[0], Character), player.hand
    player.hand.remove(character)


def test_player_move_character_hand_to_board():
    player = make_player(hero='TEST_HERO')

    character = player.add_character_to_hand(make_character(position=4))

    assert len(player.hand) > 0
    assert isinstance(player.hand[0], Character), player.hand
    player.hand.remove(character)

    player.add_character(character)


def test_player_move_character_board_to_hand():
    player = make_player(hero='TEST_HERO')

    character = player.add_character_to_hand(make_character(position=4))

    assert len(player.hand) > 0
    assert isinstance(player.hand[0], Character), player.hand
    player.hand.remove(character)

    player.add_character(character)


def test_player_triple_character_board():
    #TODO How should tripling logic work?
    pass


def test_player_triple_character_hand():
    #TODO How should tripling logic work?
    pass


def test_player_add_treasure():
    player = make_player(hero='TEST_HERO')

    player.add_treasure('TREASURE_ONE', 'TREASURE_TWO')

    assert len(player.treasures) == 2
    assert isinstance(player.treasures[0], Treasure)
    assert isinstance(player.treasures[1], Treasure)


def test_player_remove_treasure():
    player = make_player(hero='TEST_HERO')

    player.add_treasure('TREASURE_ONE', 'TREASURE_TWO')

    assert len(player.treasures) == 2

    player.treasures.pop(0)
