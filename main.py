import pygame
import sys
from board import draw_board, draw_pieces, create_board
from game_logic import generate_valid_moves, make_move, is_valid_move, is_in_check, is_checkmate, can_castle, en_passant_possible, promote_pawn

# Fenstergröße
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Schach GUI")

    board = create_board()
    selected_piece = None
    valid_moves = []
    turn = 'white'
    running = True
    game_over = False
    in_check = False
    last_move = None
    king_moved = {'white': False, 'black': False}
    rook_moved = {'white': {'left': False, 'right': False}, 'black': {'left': False, 'right': False}}

    while running:
        draw_board(screen, selected_piece, valid_moves)
        draw_pieces(screen, board)

        # Textanzeige für den aktuellen Spieler
        font = pygame.font.SysFont(None, 36)
        current_turn_text = f"Am Zug: {'Weiß (User)' if turn == 'white' else 'Schwarz (KI)'}"
        text = font.render(current_turn_text, True, (0, 0, 0))
        screen.blit(text, (20, 10))

        if game_over:
            font = pygame.font.SysFont(None, 55)
            text = font.render("Schachmatt!", True, (255, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                if selected_piece:
                    end_pos = (row, col)
                    start_pos = selected_piece

                    if end_pos in valid_moves and is_valid_move(selected_piece, end_pos, board, turn):
                        
                        # Prüfen auf Rochade
                        if board[start_pos[0]][start_pos[1]] == f'{turn[0]}K' and can_castle(board, start_pos, end_pos, king_moved[turn], rook_moved[turn]):
                            if end_pos[1] == 6:
                                make_move(start_pos, end_pos, board)
                                make_move((start_pos[0], 7), (start_pos[0], 5), board)  # Turmzug für die Kurzrochade
                            elif end_pos[1] == 2:
                                make_move(start_pos, end_pos, board)
                                make_move((start_pos[0], 0), (start_pos[0], 3), board)  # Turmzug für die Langrochade
                            king_moved[turn] = True
                            rook_moved[turn]['left'] = True if end_pos[1] == 2 else rook_moved[turn]['left']
                            rook_moved[turn]['right'] = True if end_pos[1] == 6 else rook_moved[turn]['right']
                        # Prüfen auf En Passant
                        elif en_passant_possible(board, start_pos, end_pos, last_move):
                            make_move(start_pos, end_pos, board)
                            board[last_move[1][0]][last_move[1][1]] = '--'  # Der Bauer, der en passant geschlagen wird
                        else:
                            make_move(start_pos, end_pos, board)
                        
                        promote_pawn(board, end_pos)

                        selected_piece = None
                        valid_moves = []

                        # Aktualisiere den letzten Zug
                        last_move = (start_pos, end_pos)
                        
                        # Überprüfen, ob der Spieler im Schach steht
                        if is_in_check(board, 'black' if turn == 'white' else 'white'):
                            in_check = True
                            if is_checkmate(board, 'black' if turn == 'white' else 'white'):
                                game_over = True
                        else:
                            in_check = False
                        
                        turn = 'black' if turn == 'white' else 'white'
                    else:
                        selected_piece = None
                        valid_moves = []
                else:
                    if board[row][col] != '--' and (board[row][col][0] == 'w' and turn == 'white'):
                        selected_piece = (row, col)
                        valid_moves = generate_valid_moves(selected_piece, board, turn)
        
        # Anzeige, wenn der Spieler im Schach steht
        if in_check:
            font = pygame.font.SysFont(None, 55)
            text = font.render(f"{'Schwarz' if turn == 'black' else 'Weiß'} ist im Schach!", True, (255, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()

if __name__ == "__main__":
    main()
