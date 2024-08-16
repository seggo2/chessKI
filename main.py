import pygame
import sys
import time
from board import draw_board, draw_pieces, create_board
from game_logic import generate_valid_moves, make_move, is_valid_move, is_in_check, is_checkmate, can_castle, en_passant_possible, promote_pawn
from ki import make_ai_move

# Fenstergrößen
WIDTH, HEIGHT = 840, 640  # Gesamtbreite um 200 Pixel nach rechts erweitert
SQUARE_SIZE = HEIGHT // 8

# Globale Variablen
turn = 'white'
timer = 0
white_captures = []
black_captures = []
game_over = False
game_start_time = time.time()  # Startzeit des Spiels
selected_piece = None  # Initialisieren der Variable
valid_moves = []  # Initialisieren der Variable

def draw_info_window(screen):
    # Info-Bereich Hintergrund
    pygame.draw.rect(screen, (230, 230, 250), (640, 0, 200, HEIGHT))  # Helles Grau-Lila als Hintergrundfarbe

    font = pygame.font.SysFont(None, 36)

    # Textanzeige für den aktuellen Spieler
    current_turn_text = f"Am Zug: {'Weiß (User)' if turn == 'white' else 'Schwarz (KI)'}"
    turn_text = font.render(current_turn_text, True, (0, 0, 0))
    screen.blit(turn_text, (650, 20))

    # Timer anzeigen
    timer_text = font.render(f"Zeit: {timer:.1f}s", True, (0, 0, 0))
    screen.blit(timer_text, (650, 60))

    # Liste der geschlagenen Figuren
    capture_text = font.render("Geschlagen:", True, (0, 0, 0))
    screen.blit(capture_text, (650, 100))
    y_offset = 130
    for piece in white_captures:
        piece_text = font.render(piece, True, (0, 0, 0))
        screen.blit(piece_text, (650, y_offset))
        y_offset += 30

    for piece in black_captures:
        piece_text = font.render(piece, True, (0, 0, 0))
        screen.blit(piece_text, (720, y_offset))
        y_offset += 30

def display_winner(screen, winner, total_time):
    """Zeigt den Gewinner und die Gesamtspielzeit an."""
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont(None, 55)
    winner_text = f"{winner} hat gewonnen!"
    time_text = f"Gesamtspielzeit: {total_time:.1f}s"

    winner_render = font.render(winner_text, True, (0, 0, 0))
    time_render = font.render(time_text, True, (0, 0, 0))

    screen.blit(winner_render, (WIDTH // 2 - winner_render.get_width() // 2, HEIGHT // 2 - winner_render.get_height() // 2 - 30))
    screen.blit(time_render, (WIDTH // 2 - time_render.get_width() // 2, HEIGHT // 2 - time_render.get_height() // 2 + 30))

    pygame.display.flip()
    pygame.time.wait(3000)

def reset_game():
    """Setzt das Spiel zurück, um eine neue Runde zu starten."""
    global board, selected_piece, valid_moves, turn, timer, white_captures, black_captures, game_over, game_start_time
    board = create_board()
    selected_piece = None
    valid_moves = []
    turn = 'white'
    timer = 0
    white_captures = []
    black_captures = []
    game_over = False
    game_start_time = time.time()

def main():
    global turn, timer, white_captures, black_captures, game_over, selected_piece, valid_moves

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Schach GUI")

    reset_game()  # Spiel initialisieren

    clock = pygame.time.Clock()

    while True:  # Endlosschleife, um das Spiel bei Bedarf neu zu starten
        while not game_over:
            screen.fill((255, 255, 255))  # Füllt den Hintergrund mit Weiß
            draw_board(screen, selected_piece, valid_moves)
            draw_pieces(screen, board)
            draw_info_window(screen)  # Zeichnet den Info-Bereich rechts neben dem Schachbrett

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and turn == 'white':
                    pos = pygame.mouse.get_pos()
                    if pos[0] < 640:  # Sicherstellen, dass der Klick im Schachbrettbereich liegt
                        col = pos[0] // SQUARE_SIZE
                        row = pos[1] // SQUARE_SIZE
                        if selected_piece:
                            end_pos = (row, col)
                            start_pos = selected_piece

                            if end_pos in valid_moves and is_valid_move(selected_piece, end_pos, board, turn):
                                captured_piece = board[end_pos[0]][end_pos[1]]
                                if captured_piece != '--':
                                    black_captures.append(captured_piece)

                                make_move(start_pos, end_pos, board)
                                promote_pawn(board, end_pos)

                                selected_piece = None
                                valid_moves = []

                                last_move = (start_pos, end_pos)
                                
                                if is_in_check(board, 'black'):
                                    in_check = True
                                    if is_checkmate(board, 'black'):
                                        game_over = True
                                        winner = "Weiß"
                                else:
                                    in_check = False
                                
                                turn = 'black'
                                timer = 0  # Timer zurücksetzen nach jedem Zug
                            else:
                                selected_piece = None
                                valid_moves = []
                        else:
                            if board[row][col] != '--' and (board[row][col][0] == 'w' and turn == 'white'):
                                selected_piece = (row, col)
                                valid_moves = generate_valid_moves(selected_piece, board, turn)
            
            # KI-Zug für Schwarz
            if turn == 'black' and not game_over:
                move = make_ai_move(board)
                if move:
                    start_pos, end_pos = move
                    if is_in_check(board, 'white'):
                        in_check = True
                        if is_checkmate(board, 'white'):
                            game_over = True
                            winner = "Schwarz"
                    else:
                        in_check = False
                    
                    turn = 'white'
                    timer = 0  # Timer zurücksetzen nach dem KI-Zug

            pygame.display.flip()

            # Timer erhöhen
            timer += clock.tick(30) / 1000.0  # Erhöhung in Sekunden

        if game_over:
            total_time = time.time() - game_start_time
            display_winner(screen, winner, total_time)

            # Option für Neustart
            font = pygame.font.SysFont(None, 36)
            restart_text = font.render("Drücke 'R' für ein neues Spiel", True, (0, 0, 0))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
            pygame.display.flip()

            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            reset_game()
                            waiting_for_restart = False  # Beendet die Wartezeit und startet das Spiel neu
                            break

if __name__ == "__main__":
    main()
