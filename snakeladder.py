import pygame
import random
import sys
import os

pygame.init()

# Screen and board settings
WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // 10  # 10x10 board

# Colors
WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
BLUE    = (0,   0, 255)
YELLOW  = (255, 255,   0)
GREEN   = (0, 255,   0)

# Load board image
board_image_path = "snake and ladder game.png"
try:
    board_image = pygame.image.load(board_image_path)
    board_image = pygame.transform.scale(board_image, (WIDTH, HEIGHT))
except pygame.error:
    print("Could not load board image. Check the path or file name.")
    board_image = pygame.Surface((WIDTH, HEIGHT))
    board_image.fill((200, 200, 200))

# Load dice images (dice1.png ... dice6.png)
dice_images = {}
for i in range(1, 7):
    try:
        img = pygame.image.load(f"dice{i}.png")
        dice_images[i] = pygame.transform.scale(img, (60, 60))
    except pygame.error:
        # Fallback to a blank surface if not found
        dice_images[i] = pygame.Surface((60, 60))
        dice_images[i].fill((150, 150, 150))

# Load dice roll sound
try:
    roll_sound = pygame.mixer.Sound("roll.wav")
except pygame.error:
    roll_sound = None
    print("Could not load 'roll.wav'. Check the path or file name.")

# Define Snakes & Ladders
snakes = {
    93: 73,
    95: 75,
    98: 79,
    87: 24,
    64: 60,
    62: 19,
    54: 34,
    17: 7
}
ladders = {
    1: 38,
    4: 14,
    9: 31,
    21: 42,
    28: 84,
    51: 67,
    71: 91,
    80: 100
}
transitions = {**snakes, **ladders}

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snakes and Ladders")

# Convert board position (0..100) to pixel coordinates
# We'll allow position 0 for the 'start' before moving onto the board.
def get_position_coords(position):
    # If still at '0', place token off-board (or anywhere you like)
    if position == 0:
        return (-50, -50)  # hidden off-screen

    # For 1..100, typical Snakes & Ladders layout
    pos_index = position - 1
    row = pos_index // 10
    col_in_row = pos_index % 10
    
    # Even row => left-to-right, odd row => right-to-left
    if row % 2 == 0:
        col = col_in_row
    else:
        col = 9 - col_in_row
    
    pixel_x = col * CELL_SIZE + CELL_SIZE // 2
    pixel_y = (9 - row) * CELL_SIZE + CELL_SIZE // 2
    return pixel_x, pixel_y

def roll_dice():
    if roll_sound:
        roll_sound.play()
    return random.randint(1, 6)

# Moves the player, enforcing the rule:
# - If at 0, only move if dice is 1 or 6
def get_next_position(current_position, dice_roll):
    if current_position == 0:
        # Must roll 1 or 6 to leave start
        if dice_roll not in [1, 6]:
            return current_position  # Stay at 0

    new_pos = current_position + dice_roll
    if new_pos > 100:
        # If roll goes beyond 100, don't move
        return current_position

    # Check for snake/ladder
    return transitions.get(new_pos, new_pos)

def draw_board():
    screen.blit(board_image, (0, 0))

def draw_token(position, color):
    x, y = get_position_coords(position)
    pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 4)

def main():
    clock = pygame.time.Clock()
    
    # Two players, starting at position 0 (off-board)
    player_positions = [0, 0]
    player_colors = [BLUE, YELLOW]
    player_names = ["Player 1", "Player 2"]
    
    current_player = 0
    dice_value = 1
    font = pygame.font.SysFont(None, 32)
    
    game_over = False
    winner_index = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # Roll dice if game not over
                if not game_over and event.key == pygame.K_SPACE:
                    dice_value = roll_dice()
                    
                    # Move current player
                    new_position = get_next_position(player_positions[current_player], dice_value)
                    player_positions[current_player] = new_position
                    
                    # Check for win
                    if new_position == 100:
                        game_over = True
                        winner_index = current_player
                    else:
                        # Switch player
                        current_player = (current_player + 1) % 2
                
                # If game over, press R to restart (or automatically restart)
                if game_over and event.key == pygame.K_r:
                    # Reset the game
                    player_positions = [0, 0]
                    current_player = 0
                    dice_value = 1
                    game_over = False
                    winner_index = None

        # Draw the board
        draw_board()
        
        # Draw tokens
        for i in range(len(player_positions)):
            draw_token(player_positions[i], player_colors[i])
        
        # Show dice info (image + text)
        dice_text = font.render(f"Dice: {dice_value}", True, WHITE)
        screen.blit(dice_text, (10, 10))

        # If we have a dice image, draw it
        if dice_value in dice_images:
            screen.blit(dice_images[dice_value], (10, 40))
        
        # If game over, display winner & restart info
        if game_over and winner_index is not None:
            winner_text = font.render(f"{player_names[winner_index]} WINS!", True, GREEN)
            screen.blit(winner_text, (WIDTH // 2 - 60, HEIGHT // 2))
            
            restart_text = font.render("Press R to Restart", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - 80, HEIGHT // 2 + 40))
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
