import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont("arial", 24)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Combat System")

# Load images
background = pygame.image.load("assets/background.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load Sprites
def load_sprite_sheet(image_path, rows, cols, scale_factor=1):
    """
    Load and split a sprite sheet into individual frames, and scale them.
    """
    sprite_sheet = pygame.image.load(image_path).convert_alpha()
    sheet_width, sheet_height = sprite_sheet.get_size()
    
    # Calculate precise frame size
    frame_width = sheet_width // cols
    frame_height = sheet_height // rows

    frames = []
    for row in range(rows):
        for col in range(cols):
            # Extract the exact portion of the sprite sheet
            frame = sprite_sheet.subsurface(
                pygame.Rect(
                    col * frame_width,  # Exact x-position
                    row * frame_height,  # Exact y-position
                    frame_width, frame_height  # Exact width and height
                )
            )
            # Scale the frame if necessary
            scaled_frame = pygame.transform.scale(
                frame, (int(frame_width * scale_factor), int(frame_height * scale_factor))
            )
            frames.append(scaled_frame)
    return frames, int(frame_width * scale_factor), int(frame_height * scale_factor)

# Load knight and goblin sprite sheets
knight_frames, knight_width, knight_height = load_sprite_sheet("assets/knight.png", 12, 5, scale_factor=5)
goblin_frames, goblin_width, goblin_height = load_sprite_sheet("assets/goblin.png", 4, 11, scale_factor=5)

# Player Class
class Player:
    def __init__(self, name, role, x, y):
        self.name = name
        self.role = role
        self.hp = 100
        self.mana = 50
        self.attack = 10
        self.defense = 5
        self.x = x
        self.y = y
        self.frames = knight_frames  # Loaded knight frames
        self.current_frame = 0       # For animation
        self.state = "idle"          # States: idle, attack
        self.animation_speed = 5
        self.frame_count = 0
    
    def update(self):
        # Handle animations
        self.frame_count += 1
        if self.frame_count % self.animation_speed == 0:
            if self.state == "idle":
                # Use the first 5 frames of the idle row
                start_frame = 15
                total_frames = 5
                self.current_frame = start_frame + (self.current_frame - start_frame + 1) % total_frames
            elif self.state == "attack":
                # Use the first 5 frames of the attack row
                start_frame = 35
                total_frames = 5
                offset = (self.current_frame - start_frame + 1) % total_frames
                self.current_frame = start_frame + offset

                # Reset to idle when the attack animation finishes
                if offset == total_frames - 1:  # Last frame of the attack animation
                    self.state = "idle"
    
    def draw(self):
        current_sprite = self.frames[self.current_frame]
        screen.blit(current_sprite, (self.x, self.y))
        # HP and Mana Bars
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, 100, 10))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.hp, 10))
        pygame.draw.rect(screen, BLUE, (self.x, self.y + 70, self.mana, 10))
    
    def take_damage(self, damage):
        self.hp -= max(damage - self.defense, 0)

                    
    def draw(self):
        current_sprite = self.frames[self.current_frame]
        screen.blit(current_sprite, (self.x, self.y))
        # HP and Mana Bars
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, 100, 10))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.hp, 10))
        pygame.draw.rect(screen, BLUE, (self.x, self.y + 70, self.mana, 10))
    
    def take_damage(self, damage):
        self.hp -= max(damage - self.defense, 0)

# Enemy Class
class Enemy:
    def __init__(self, name, x, y):
        self.name = name
        self.hp = 100
        self.frames = goblin_frames  # Loaded goblin frames
        self.current_frame = 33       # Start at frame 33
        self.state = "idle"           # States: idle
        self.animation_speed = 5      # Number of updates before moving to the next frame
        self.frame_count = 0          # Counts the updates
        self.x = x
        self.y = y

    def update(self):
        # Update frame for animation (frames 33 to 40)
        self.frame_count += 1
        if self.frame_count % self.animation_speed == 0:
            total_frames = 8  # Number of frames in the range (33 to 40 inclusive)
            self.current_frame = 33 + (self.current_frame - 33 + 1) % total_frames

    def draw(self):
        # Draw the current animation frame
        current_sprite = self.frames[self.current_frame]
        screen.blit(current_sprite, (self.x, self.y))
        
        # Draw HP bar above the enemy
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, 100, 10))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.hp, 10))

    def take_damage(self, damage):
        self.hp -= damage

# Main combat function
def combat():
    player = Player("Hero", "Warrior", 130, 320)
    enemy = Enemy("Goblin", 500, 200)
    clock = pygame.time.Clock()
    running = True

    # Buttons
    attack_button = pygame.Rect(50, 500, 100, 50)
    defend_button = pygame.Rect(200, 500, 100, 50)
    ability_button = pygame.Rect(350, 500, 150, 50)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if attack_button.collidepoint(event.pos):
                    print("Player attacks!")
                    player.state = "attack"
                    enemy.take_damage(random.randint(5, 10))
                elif defend_button.collidepoint(event.pos):
                    print("Player defends!")
                    player.defense += 5
                elif ability_button.collidepoint(event.pos):
                    print("Player uses Power Strike!")
                    enemy.take_damage(random.randint(15, 25))

        # Update player and enemy animations
        player.update()
        enemy.update()

        # Check for victory/defeat
        if player.hp <= 0:
            print("You lost!")
            running = False
        if enemy.hp <= 0:
            print("You won!")
            running = False

        # Draw everything
        screen.blit(background, (0, 0))
        player.draw()
        enemy.draw()

        # Buttons
        pygame.draw.rect(screen, WHITE, attack_button)
        pygame.draw.rect(screen, WHITE, defend_button)
        pygame.draw.rect(screen, WHITE, ability_button)

        screen.blit(font.render("Attack", True, BLACK), (60, 515))
        screen.blit(font.render("Defend", True, BLACK), (210, 515))
        screen.blit(font.render("Power Strike", True, BLACK), (360, 515))

        pygame.display.flip()
        clock.tick(30)

# Run the combat
combat()
pygame.quit()
