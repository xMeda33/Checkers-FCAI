import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, GREEN
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, GREEN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        # return (-1 * (self.red_left + 2 * self.red_kings) + 2 * self.white_kings + self.white_left) * 5
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def evaluate_board(self, board, player):
        piece_value = 1
        king_value = 2
        end_row_value = 5
        close_to_enemy_value = 0.2
        aggressive_king_value = 3
        king_distance_value = 0.1
        capture_value = 0.5

        # Initialize the score to 0
        score = 0

        # Count the number of pieces and kinged pieces for the player and opponent
        self.white_left = 0
        self.white_kings = 0
        self.red_left = 0
        self.red_kings = 0

        # Keep track of the player's kinged pieces that are in aggressive positions
        aggressive_kings = set()

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece == player:
                    self.white_left += 1
                    if row == 0 or row == 7:
                        self.white_kings += 1
                        score += king_value
                        if self.is_aggressive_king(board, row, col, player):
                            aggressive_kings.add((row, col))
                    else:
                        score += piece_value
                    if row == 0 or row == 1 or row == 6 or row == 7:
                        score += end_row_value
                    if self.is_close_to_enemy(board, row, col, player):
                        score += close_to_enemy_value
                    if (row, col) in aggressive_kings:
                        score += aggressive_king_value
                    if piece.lower() == "k":
                        distance_to_enemy = min(self.get_distance_to_enemy(board, row, col, player))
                        score += king_distance_value / (1 + distance_to_enemy)

                elif piece != ".":
                    self.red_left += 1
                    if row == 0 or row == 7:
                        self.red_kings += 1
                        score -= king_value
                    else:
                        score -= piece_value
                    if row == 0 or row == 1 or row == 6 or row == 7:
                        score -= end_row_value
                    if self.is_close_to_enemy(board, row, col, player):
                        score -= close_to_enemy_value
                    if piece.lower() == "k":
                        distance_to_enemy = min(self.get_distance_to_enemy(board, row, col, player))
                        score -= king_distance_value / (1 + distance_to_enemy)

        # Add a bonus for having more pieces or more kings than the opponent
        if self.white_left > self.red_left:
            score += self.white_left - self.red_left
        if self.white_kings > self.red_kings:
            score += king_value * (self.white_kings - self.red_kings)

        # Penalize positions that lead to a potential draw
        player_row_sum = sum([1 for row in board for piece in row if piece == player])
        enemy_row_sum = sum([1 for row in board for piece in row if piece != "." and piece != player])
        if player_row_sum == 1 and enemy_row_sum == 1:
            score -= 10

        # Add a bonus for capturing enemy pieces with kinged pieces
        for row, col in aggressive_kings:
            for dr, dc in [(1, -1), (1, 1), (-1, -1), (-1, 1)]:
                r = row + dr
                c = col + dc
                if r >= 0 and r < 8 and c >= 0 and c < 8 and board[r][c] != "." and board[r][c].lower() != player:
                    score += capture_value

        return score

    def get_distance_to_enemy(board, row, col, player):
        # Get the minimum distance from a player's piece to the closest enemy piece
        distances = []
        for dr, dc in [(1, -1), (1, 1), (-1, -1), (-1, 1)]:
            r = row + dr
            c = col + dc
            while r >= 0 and r < 8 and c >= 0 and c < 8:
                if board[r][c] != "." and board[r][c].lower() != player:
                    distances.append(abs(r - row))
                    break
                r += dr
                c += dc
        if len(distances) == 0:
            return [8]
        return distances


    def is_aggressive_king(board, row, col, player):
        # Check if a player's kinged piece is in an aggressive position
        if board[row][col].lower() != "k":
            return False
        for dr, dc in [(1, -1), (1, 1), (-1, -1), (-1, 1)]:
            r = row + dr
            c = col + dc
            if r >= 0 and r < 8 and c >= 0 and c < 8 and board[r][c] == ".":
                return True
        return False

    def is_close_to_enemy(board, row, col, player):
            # Check if a player's piece is close to the opponent's piece
            for dr, dc in [(1, -1), (1, 1), (-1, -1), (-1, 1)]:
                r = row + dr
                c = col + dc
                if r >= 0 and r < 8 and c >= 0 and c < 8 and board[r][c] != "." and board[r][c] != player:
                    return True
            return False

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
