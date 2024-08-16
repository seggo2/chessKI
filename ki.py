import math
from game_logic import generate_valid_moves, make_move, is_valid_move

piece_values = {
    'P': 1,
    'R': 5,
    'N': 3,
    'B': 3,
    'Q': 9,
    'K': 1000  # Der König ist unbezahlbar, daher ein sehr hoher Wert
}

piece_square_tables = {
    'P': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [1, 1, 2, 3, 3, 2, 1, 1],
        [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
        [0.5, 1, 1, -2, -2, 1, 1, 0.5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    # Ähnliche Tabellen für R, N, B, Q, K
}

def evaluate_board(board):
    """Bewertungsfunktion basierend auf Material und Position."""
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--':
                value = piece_values.get(piece[1], 0)
                if piece[0] == 'w':
                    score += value
                    score += piece_square_tables.get(piece[1], [[0]*8]*8)[row][col]
                else:
                    score -= value
                    score -= piece_square_tables.get(piece[1], [[0]*8]*8)[7-row][col]
    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    """Minimax-Algorithmus mit Alpha-Beta-Pruning."""
    if depth == 0:
        return evaluate_board(board), None

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for row in range(8):
            for col in range(8):
                if board[row][col] != '--' and board[row][col][0] == 'b':  # KI ist Schwarz
                    moves = generate_valid_moves((row, col), board, 'black')
                    for move in moves:
                        if is_valid_move((row, col), move, board, 'black'):
                            temp_board = [r[:] for r in board]  # Temporäres Brett kopieren
                            make_move((row, col), move, temp_board)
                            eval, _ = minimax(temp_board, depth - 1, alpha, beta, False)
                            if eval > max_eval:
                                max_eval = eval
                                best_move = ((row, col), move)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = None
        for row in range(8):
            for col in range(8):
                if board[row][col] != '--' and board[row][col][0] == 'w':  # Gegner ist Weiß
                    moves = generate_valid_moves((row, col), board, 'white')
                    for move in moves:
                        if is_valid_move((row, col), move, board, 'white'):
                            temp_board = [r[:] for r in board]  # Temporäres Brett kopieren
                            make_move((row, col), move, temp_board)
                            eval, _ = minimax(temp_board, depth - 1, alpha, beta, True)
                            if eval < min_eval:
                                min_eval = eval
                                best_move = ((row, col), move)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break
        return min_eval, best_move

def make_ai_move(board):
    """Ermittelt und führt den besten Zug für die KI aus."""
    _, move = minimax(board, 4, -math.inf, math.inf, True)
    if move:
        start_pos, end_pos = move
        make_move(start_pos, end_pos, board)
        return start_pos, end_pos
    return None
