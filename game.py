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
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Fonts
pygame.font.init()
font = pygame.font.SysFont("arial", 24)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Combat System")

# Load images
background = pygame.image.load("assets/background.jpg").convert()
warrior_img = pygame.image.load("assets/warrior.png").convert_alpha()
enemy_img = pygame.image.load("assets/enemy.png").convert_alpha()

# Classes
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
        self.sprite = warrior_img  # Default sprite for the player
    
    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))
        # HP Bar
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, 100, 10))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.hp, 10))
        # Mana Bar
        pygame.draw.rect(screen, BLUE, (self.x, self.y + 70, self.mana, 10))
    
    def take_damage(self, damage):
        self.hp -= max(damage - self.defense, 0)
    
    def use_mana(self, amount):
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

class Enemy:
    def __init__(self, name, x, y):
        self.name = name
        self.hp = 100
        self.sprite = enemy_img
        self.x = x
        self.y = y
    
    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))
        # HP Bar
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, 100, 10))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.hp, 10))
    
    def take_damage(self, damage):
        self.hp -= damage

# Main combat function
def combat():
    player = Player("Hero", "Warrior", 100, 300)
    enemy = Enemy("Goblin", 500, 300)
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
                    # Player attacks
                    damage = random.randint(5, 10)
                    print(f"Player attacks for {damage}!")
                    enemy.take_damage(damage)
                elif defend_button.collidepoint(event.pos):
                    print("Player defends!")
                    player.defense += 5
                elif ability_button.collidepoint(event.pos):
                    if player.use_mana(15):
                        damage = random.randint(15, 25)
                        print(f"Player uses Power Strike for {damage}!")
                        enemy.take_damage(damage)
                    else:
                        print("Not enough mana!")
        
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
        
        # Draw buttons
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
