
KNIGHT_MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def is_valid_knight_move(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    return (dx, dy) in KNIGHT_MOVES

def create_board(n):
    return [[-1 for _ in range(n)] for _ in range(n)]