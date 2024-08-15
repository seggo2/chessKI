import pygame
import os

# Farben definieren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (205, 133, 63)
BEIGE = (245, 245, 220)
HIGHLIGHT = (255, 0, 0)

# Schachbrettgröße und Figurengrößen festlegen
SQUARE_SIZE = 80  # Wenn du die Größe änderst, passe sie in der main.py an

# Absoluter Pfad zum Bilderordner
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chess')

# Figurenbilder laden
piece_images = {
    'bR': pygame.image.load(os.path.join(image_path, 'chess_piece_2_black_rook.png')),
    'bN': pygame.image.load(os.path.join(image_path, 'chess_piece_2_black_knight.png')),
    'bB': pygame.image.load(os.path.join(image_path, 'chess_piece_2_black_bishop.png')),
    'bQ': pygame.image.load(os.path.join(image_path, 'chess_piece_2_black_queen.png')),
    'bK': pygame.image.load(os.path.join(image_path, 'chess_piece_2_black_king.png')),
    'bP': pygame.image.load(os.path.join(image_path, 'chess_piece_2_black_pawn.png')),
    'wR': pygame.image.load(os.path.join(image_path, 'chess_piece_2_white_rook.png')),
    'wN': pygame.image.load(os.path.join(image_path, 'chess_piece_2_white_knight.png')),
    'wB': pygame.image.load(os.path.join(image_path, 'chess_piece_2_white_bishop.png')),
    'wQ': pygame.image.load(os.path.join(image_path, 'chess_piece_2_white_queen.png')),
    'wK': pygame.image.load(os.path.join(image_path, 'chess_piece_2_white_king.png')),
    'wP': pygame.image.load(os.path.join(image_path, 'chess_piece_2_white_pawn.png'))
}

# Größenanpassung der Bilder
for key in piece_images:
    piece_images[key] = pygame.transform.scale(piece_images[key], (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(screen, selected_piece, valid_moves):
    for row in range(8):
        for col in range(8):
            color = BEIGE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if selected_piece == (row, col):
                pygame.draw.rect(screen, HIGHLIGHT, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

            if (row, col) in valid_moves:
                pygame.draw.circle(screen, HIGHLIGHT, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

def draw_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--':
                screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def create_board():
    return [
        ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
        ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
    ]
