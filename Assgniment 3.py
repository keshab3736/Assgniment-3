print ("Hello world")

import pygame 
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.speed = 5
        self.jump_height = -15
        self.gravity = 1
        self.velocity_y = 0
        self.health = 100
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # Jump mechanics
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        if self.rect.y > HEIGHT - 50:
            self.rect.y = HEIGHT - 50
            self.velocity_y = 0

    def jump(self):
        self.velocity_y = self.jump_height

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 100, HEIGHT // 2)
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7

    def update(self):
        self.rect.x += self.speed

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, collectible_type):
        super().__init__()
        self.collectible_type = collectible_type
        self.image = pygame.Surface((30, 30))
        if collectible_type == "health_boost":
            self.image.fill((0, 255, 0))
        elif collectible_type == "extra_life":
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BossEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * 2, HEIGHT // 2)
        self.speed = 2
        self.health = 200

    def update(self):
        self.rect.x -= self.speed
        if self.health <= 0:
            self.kill()

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Adventure")

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()
boss_enemy = BossEnemy()
all_sprites.add(boss_enemy)

# Create player, enemies, and add to sprite groups
player = Player()
enemy = Enemy()
all_sprites.add(player, enemy)
enemies.add(enemy)

# Level design
levels = [
    [
        (100, HEIGHT - 50),
        (200, HEIGHT - 50),
        (400, HEIGHT - 100),
        (600, HEIGHT - 50),
        (800, HEIGHT - 50),
        (1000, HEIGHT - 50),
        (1200, HEIGHT - 50),
    ],
    [
        (100, HEIGHT - 50),
        (300, HEIGHT - 100),
        (600, HEIGHT - 50),
        (800, HEIGHT - 150),
        (1000, HEIGHT - 50),
        (1200, HEIGHT - 50),
        (1500, HEIGHT - 50),
    ],
    [
        (100, HEIGHT - 50),
        (400, HEIGHT - 50),
        (700, HEIGHT - 100),
        (1000, HEIGHT - 150),
        (1200, HEIGHT - 50),
        (1400, HEIGHT - 100),
        (1600, HEIGHT - 50),
    ],
]

current_level = 0
player.rect.x = 100
player.rect.y = HEIGHT - 50

# Scoring system
score = 0

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Player shoots projectile
                projectile = Projectile(player.rect.x + 40, player.rect.y + 20)
                all_sprites.add(projectile)
                projectiles.add(projectile)

    # Update
    all_sprites.update()

    # Check collisions
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        player.health -= 10
        if player.health <= 0:
            player.lives -= 1
            if player.lives <= 0:
                running = False
            else:
                player.health = 100

    # Check collisions with collectibles
    collectible_hits = pygame.sprite.spritecollide(player, collectibles, True)
    for collectible in collectible_hits:
        if collectible.collectible_type == "health_boost":
            player.health += 20
            if player.health > 100:
                player.health = 100
        elif collectible.collectible_type == "extra_life":
            player.lives += 1

    # Check collisions with boss enemy
    boss_hits = pygame.sprite.spritecollide(player, pygame.sprite.Group(boss_enemy), False)
    for boss in boss_hits:
        player.health -= 2

    # Check if player reached the end of the level
    if player.rect.x > WIDTH - 50:
        current_level += 1
        if current_level < len(levels):
            # Reset player position for the next level
            player.rect.x = 100
            player.rect.y = HEIGHT - 50
        else:
            # Player completed all levels
            running = False

    # Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # Draw health bar
    pygame.draw.rect(screen, (0, 255, 0), (10, 10, player.health * 2, 20))
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 200, 20), 2)

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font
