def is_valid_pawn_move(start_pos, end_pos, board, is_white):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    
    direction = -1 if is_white else 1
    start_row_target = 6 if is_white else 1

    # Ein Feld nach vorne
    if end_row == start_row + direction and end_col == start_col and board[end_row][end_col] == '--':
        return True
    
    # Zwei Felder nach vorne von der Startposition
    if start_row == start_row_target and end_row == start_row + 2 * direction and end_col == start_col and board[end_row][end_col] == '--':
        return True
    
    # Diagonal schlagen
    if end_row == start_row + direction and abs(end_col - start_col) == 1 and board[end_row][end_col] != '--':
        return True
    
    return False

def is_valid_rook_move(start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if start_row != end_row and start_col != end_col:
        return False

    # Horizontaler oder vertikaler Weg
    if start_row == end_row:
        step = 1 if end_col > start_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] != '--':
                return False
    elif start_col == end_col:
        step = 1 if end_row > start_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] != '--':
                return False
    
    return True

def is_valid_knight_move(start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    row_diff = abs(start_row - end_row)
    col_diff = abs(start_col - end_col)
    return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

def is_valid_bishop_move(start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if abs(start_row - end_row) != abs(start_col - end_col):
        return False

    step_row = 1 if end_row > start_row else -1
    step_col = 1 if end_col > start_col else -1

    for i in range(1, abs(end_row - start_row)):
        if board[start_row + i * step_row][start_col + i * step_col] != '--':
            return False
    
    return True

def is_valid_queen_move(start_pos, end_pos, board):
    return is_valid_rook_move(start_pos, end_pos, board) or is_valid_bishop_move(start_pos, end_pos, board)

def is_valid_king_move(start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    return max(abs(start_row - end_row), abs(start_col - end_col)) == 1

def is_valid_move(start_pos, end_pos, board, turn):
    piece = board[start_pos[0]][start_pos[1]]
    target_piece = board[end_pos[0]][end_pos[1]]
    
    # Überprüfen, ob das Zielfeld eine eigene Figur enthält
    if target_piece != '--' and target_piece[0] == piece[0]:
        return False

    if piece == '--' or (piece[0] == 'w' and turn != 'white') or (piece[0] == 'b' and turn != 'black'):
        return False

    if piece[1] == 'P':
        return is_valid_pawn_move(start_pos, end_pos, board, piece[0] == 'w')
    if piece[1] == 'R':
        return is_valid_rook_move(start_pos, end_pos, board)
    if piece[1] == 'N':
        return is_valid_knight_move(start_pos, end_pos)
    if piece[1] == 'B':
        return is_valid_bishop_move(start_pos, end_pos, board)
    if piece[1] == 'Q':
        return is_valid_queen_move(start_pos, end_pos, board)
    if piece[1] == 'K':
        return is_valid_king_move(start_pos, end_pos)
    
    return False


def generate_valid_moves(start_pos, board, turn):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(start_pos, (row, col), board, turn):
                valid_moves.append((row, col))
    return valid_moves

def make_move(start_pos, end_pos, board):
    piece = board[start_pos[0]][start_pos[1]]
    board[end_pos[0]][end_pos[1]] = piece
    board[start_pos[0]][start_pos[1]] = '--'

def is_in_check(board, turn):
    # Finde die Position des Königs
    king_pos = None
    for row in range(8):
        for col in range(8):
            if board[row][col] == (turn[0] + 'K'):
                king_pos = (row, col)
                break
        if king_pos:
            break

    # Prüfe, ob irgendeine gegnerische Figur den König bedroht
    opponent_turn = 'black' if turn == 'white' else 'white'
    for row in range(8):
        for col in range(8):
            if board[row][col].startswith(opponent_turn[0]):
                if is_valid_move((row, col), king_pos, board, opponent_turn):
                    return True
    return False

def is_checkmate(board, turn):
    if not is_in_check(board, turn):
        return False

    # Prüfe alle möglichen Züge des Spielers
    for row in range(8):
        for col in range(8):
            if board[row][col].startswith(turn[0]):
                valid_moves = generate_valid_moves((row, col), board, turn)
                for move in valid_moves:
                    temp_board = [row[:] for row in board]
                    make_move((row, col), move, temp_board)
                    if not is_in_check(temp_board, turn):
                        return False
    return True

def can_castle(board, start_pos, end_pos, king_moved, rook_moved):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if king_moved or (start_row, start_col) != (end_row, end_col):
        return False

    # Kurzrochade
    if end_col == 6 and not rook_moved['right']:
        if all(board[start_row][col] == '--' for col in range(5, 7)):
            return True
    
    # Langrochade
    if end_col == 2 and not rook_moved['left']:
        if all(board[start_row][col] == '--' for col in range(1, 4)):
            return True
    
    return False

def en_passant_possible(board, start_pos, end_pos, last_move):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    
    if board[start_row][start_col][1] != 'P':
        return False
    
    if abs(start_col - end_col) == 1 and board[end_row][end_col] == '--':
        if last_move and last_move[1][0] == start_row and board[last_move[1][0]][last_move[1][1]][1] == 'P':
            if abs(last_move[1][0] - last_move[0][0]) == 2 and last_move[1][1] == end_col:
                return True
    
    return False

def promote_pawn(board, pos):
    row, col = pos
    if board[row][col][1] == 'P':
        if row == 0 or row == 7:
            board[row][col] = board[row][col][0] + 'Q'
