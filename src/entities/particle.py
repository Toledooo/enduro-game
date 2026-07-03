import pygame
import random
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, vx=0, vy=0, size=6, color=(255, 200, 50)):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.alpha = 255
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.97
        self.vy += 0.2
        self.rect.center = (self.x, self.y)

        if self.x < -self.rect.width or self.x > SCREEN_WIDTH + self.rect.width:
            self.kill()
        elif self.y < -self.rect.height or self.y > SCREEN_HEIGHT + self.rect.height:
            self.kill()
        else:
            self.alpha -= 6
            if self.alpha <= 0:
                self.kill()
            else:
                self.image.set_alpha(self.alpha)


def spawn_spark_particles(x, y, count=15):
    particles = []
    spark_colors = [(255, 200, 50), (255, 150, 30), (255, 100, 20), (255, 255, 200)]
    for _ in range(count):
        angle = random.uniform(0, 360)
        speed = random.uniform(1.5, 5.0)
        vx = speed * pygame.math.Vector2(1, 0).rotate(angle).x
        vy = speed * pygame.math.Vector2(1, 0).rotate(angle).y
        size = random.randint(4, 8)
        color = random.choice(spark_colors)
        particles.append(Particle(x, y, vx, vy, size, color))
    return particles
