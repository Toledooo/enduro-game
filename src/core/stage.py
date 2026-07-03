import pygame, random
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Stage:
    def __init__(self, initial="summer"):
        self.current = initial
        self.patches = None
        self.snowflake_img = None
        self.snowflakes = None

    def setup(self):
        """Reinicializa os assets visuais da estação atual."""
        if self.current == "winter":
            self.patches = self._build_patches()
            self._build_snowflake_system()
        else:
            self.patches = None
            self.snowflake_img = None
            self.snowflakes = None

    def _build_patches(self):
        patches = []
        for _ in range(10):
            w = random.randint(30, 60)
            h = random.randint(15, 35)
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            for _ in range(random.randint(4, 8)):
                cx = random.randint(2, w - 2)
                cy = random.randint(2, h - 2)
                r = random.randint(3, max(4, w // 4))
                shade = random.randint(210, 255)
                alpha = random.randint(140, 220)
                pygame.draw.circle(surf, (shade, shade, shade, alpha), (cx, cy), r)
            patches.append(surf)
        return patches

    def _build_snowflake_system(self):
        self.snowflake_img = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.snowflake_img, (255, 255, 255, 230), (8, 8), 5)
        pygame.draw.circle(self.snowflake_img, (255, 255, 255, 180), (4, 4), 2)
        pygame.draw.circle(self.snowflake_img, (255, 255, 255, 180), (12, 4), 2)
        pygame.draw.circle(self.snowflake_img, (255, 255, 255, 180), (4, 12), 2)
        pygame.draw.circle(self.snowflake_img, (255, 255, 255, 180), (12, 12), 2)
        self.snowflakes = []
        for _ in range(40):
            self.snowflakes.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-SCREEN_HEIGHT, 0),
                'speed': random.uniform(0.8, 2.5),
                'drift': random.uniform(-0.4, 0.4),
                'size': random.uniform(0.5, 1.5),
                'rotation': random.uniform(0, 360),
                'rot_speed': random.uniform(-2, 2),
            })

    def update_snowflakes(self):
        if self.current != "winter":
            return
        for f in self.snowflakes:
            f['y'] += f['speed']
            f['x'] += f['drift']
            f['rotation'] += f['rot_speed']
            if f['y'] > SCREEN_HEIGHT + 20:
                f['y'] = random.randint(-20, -5)
                f['x'] = random.randint(0, SCREEN_WIDTH)
            if f['x'] < -20:
                f['x'] = SCREEN_WIDTH + 20
            elif f['x'] > SCREEN_WIDTH + 20:
                f['x'] = -20

    def draw_snowflakes(self, surface):
        if self.current != "winter":
            return
        for f in self.snowflakes:
            size = max(2, int(12 * f['size']))
            scaled = pygame.transform.scale(self.snowflake_img, (size, size))
            rotated = pygame.transform.rotate(scaled, f['rotation'])
            r = rotated.get_rect(center=(int(f['x']), int(f['y'])))
            surface.blit(rotated, r)

    @property
    def grass_color(self):
        return (210, 220, 230) if self.current == "winter" else (30, 100, 30)

    def handle_key(self, key):
        """Alterna a fase baseado na tecla pressionada."""
        if key == pygame.K_1:
            self.current = "summer"
            return True
        elif key == pygame.K_2:
            self.current = "winter"
            return True
        return False

    @property
    def display_name(self):
        return "Verão" if self.current == "summer" else "Inverno"

    @property
    def display_color(self):
        return (255, 255, 100) if self.current == "summer" else (200, 220, 255)
