class Board:
    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.turn = 0

    def get_attack_defense(self):
        if self.turn == 0:
            return self.player_one, self.player_two
        elif self.turn == 1:
            return self.player_two, self.player_one
        else:
            raise Exception('Board turn is not one or two')

    def winner(self):

        player_one_no_characters = next((False for c in self.player_one.characters.values() if c is not None), True)
        player_two_no_characters = next((False for c in self.player_one.characters.values() if m is not None), True)

        if player_one_no_characters and player_two_no_characters:
            return 3
        elif player_one_no_characters:
            return 2
        elif player_two_no_characters:
            return 1

    def __repr__(self):
        a, d = self.get_attack_defense()
        return f'\tAttacker ({a.player_number}): {a}\n\tDefender ({d.player_number}): {d}'




