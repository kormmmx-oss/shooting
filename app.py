import pygame
import random

# 게임 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Air Shooter")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# 시계 설정 (FPS)
clock = pygame.time.Clock()
FPS = 60

# 폰트 설정
font = pygame.font.SysFont("arial", 30)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT-60, 40, 40)
        self.speed = 7

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + 15, y, 10, 20)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, YELLOW, self.rect)

class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH-40), -40, 40, 40)
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

def main():
    player = Player()
    bullets = []
    enemies = []
    score = 0
    running = True

    while running:
        screen.fill(BLACK)
        
        # 1. 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.rect.x, player.rect.y))

        # 2. 객체 움직임 및 업데이트
        player.move()
        
        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        # 적 생성 (확률적)
        if random.randint(1, 30) == 1:
            enemies.append(Enemy())

        for enemy in enemies[:]:
            enemy.update()
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies.remove(enemy)
                score += 1 # 놓친 적도 점수 처리하거나 패널티 부여 가능

        # 3. 충돌 감지
        for enemy in enemies[:]:
            # 총알과 적 충돌
            for bullet in bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 10
                    break
            
            # 플레이어와 적 충돌
            if enemy.rect.colliderect(player.rect):
                print(f"Game Over! Final Score: {score}")
                running = False

        # 4. 그리기
        player.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()

        # 점수 표시
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
