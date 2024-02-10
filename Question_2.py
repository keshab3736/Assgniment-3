import pygame
import sys
import os


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)


current_dir = os.path.dirname(__file__)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.velocity = 0
        self.jump_power = -10
        self.health = 100
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()

        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = self.jump_power

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -3

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Animal vs Human Game")
    clock = pygame.time.Clock()

    
    background = pygame.image.load(os.path.join(current_dir, "sky.png")).convert()

    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # Level 1
    for i in range(20):  # Increase the number of enemies
        enemy = Enemy(SCREEN_WIDTH + i * 100, SCREEN_HEIGHT - 100)
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Level 2
    for i in range(20):  # Increase the number of enemies
        enemy = Enemy(SCREEN_WIDTH * 2 + i * 100, SCREEN_HEIGHT - 100)
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Level 3
    for i in range(20):  # Increase the number of enemies
        enemy = Enemy(SCREEN_WIDTH * 3 + i * 100, SCREEN_HEIGHT - 100)
        all_sprites.add(enemy)
        enemies.add(enemy)

    score = 0
    font = pygame.font.Font(None, 36)

   
    running = True
    while running:
        screen.blit(background, (0, 0))  # Draw background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    projectile = Projectile(player.rect.right, player.rect.centery)
                    all_sprites.add(projectile)
                    projectiles.add(projectile)

       
        all_sprites.update()

      
        hits = pygame.sprite.spritecollide(player, enemies, True)
        if hits:
            player.health -= 10
            if player.health <= 0:
                player.lives -= 1
                if player.lives <= 0:
                    game_over(screen, "Game Over")
                    running = False
                else:
                    player.health = 100

        hits = pygame.sprite.groupcollide(enemies, projectiles, True, True)
        for enemy in hits:
            score += 10

        hits = pygame.sprite.spritecollide(player, collectibles, True)
        for collectible in hits:
            pass  

       
        all_sprites.draw(screen)

        
        draw_text(screen, "Score: " + str(score), 10, 10)
        draw_text(screen, "Health: " + str(player.health), 10, 40)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def draw_text(surface, text, x, y):
    text_surface = FONT.render(text, True, WHITE)
    surface.blit(text_surface, (x, y))


def game_over(screen, text):
    screen.fill(BLACK)
    draw_text(screen, text, SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50)
    draw_text(screen, "Press Enter to Restart", SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

if __name__ == "__main__":
   main()
