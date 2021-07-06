class Player:
    def __init__(self, sprite, player_id):
        self.sprite = sprite
        self.id = player_id


class Game:
    def __init__(self, id1=None, id2=None):
        self.board = [[0] * 7 for _ in range(6)]
        self.player1 = Player(1, id1)
        self.player2 = Player(2, id2)
        self.cur_player = self.player1
        self.ongoing = True
        self.winner = None

    def play(self, column):
        row = lowest_y(column, self.board)
        if row is None:
            pass
        else:
            self.board[row][column] = self.cur_player.sprite
            if self.wins(self.cur_player):
                self.ongoing = False
                self.winner = self.cur_player
            self.next_turn()

    def next_turn(self):
        if self.cur_player == self.player1:
            self.cur_player = self.player2
        elif self.cur_player == self.player2:
            self.cur_player = self.player1

    def get_embed(self):
        str_board = "​"
        for row in self.board:
            line = "　"
            for element in row:
                line += emotify(element) + "　"
            str_board += line + "\n \n"
        str_board += "​　:one:　:two:　:three:　:four:　:five:　:six:　:seven:"
        return str_board

    def wins(self, player):

        # Checks horizontally
        for row in range(6):
            for column in range(4):
                if self.board[row][column] == player.sprite and self.board[row][column + 1] == player.sprite and \
                        self.board[row][column + 2] == player.sprite and self.board[row][column + 3] == player.sprite:
                    return True

        # Checks Vertically
        for row in range(3):
            for column in range(7):
                if self.board[row][column] == player.sprite and self.board[row + 1][column] == player.sprite and \
                        self.board[row + 2][column] == player.sprite and self.board[row + 3][column] == player.sprite:
                    return True

        # Checks diagonally SE
        for row in range(3):
            for column in range(4):
                if self.board[row][column] == player.sprite and self.board[row + 1][column + 1] == player.sprite and \
                        self.board[row + 2][column + 2] == player.sprite and \
                        self.board[row + 3][column + 3] == player.sprite:
                    return True

        # Checks diagonally NE
        for row in range(3, 6):
            for column in range(3):
                if self.board[row][column] == player.sprite and self.board[row - 1][column + 1] == player.sprite and \
                        self.board[row - 2][column + 2] == player.sprite and \
                        self.board[row - 3][column + 3] == player.sprite:
                    return True


def lowest_y(column, board: list):
    base = -1
    while base < 5 and (base == -1 or board[base + 1][column] == 0):
        base += 1
    if base == -1:
        return None
    return base


def emotify(n: int) -> str:
    if n == 0:
        return ":black_circle:"
    if n == 1:
        return ":red_circle:"
    if n == 2:
        return ":yellow_circle:"


if __name__ == "__main__":
    game = Game()
    print(game.board)
