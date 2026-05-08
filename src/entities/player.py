import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self):
        self.width = 60
        self.height = 40
        
        # Nasce centralizado horizontalmente
        self.x = (SCREEN_WIDTH // 2) - (self.width // 2)
        
        # Fixo na parte inferior da tela (Eixo Y não muda)
        self.y = SCREEN_HEIGHT - self.height - 30 
        
        self.speed_x = 7 # Velocidade do movimento lateral
        self.color = (200, 0, 0) # Vermelho

    def move_left(self, track_left):
        if self.x > track_left + 20: # Pequena margem para não colidir com a borda da estrada
            self.x -= self.speed_x

    def move_right(self, track_right):
        if self.x < track_right - self.width - 20: # Pequena margem para não colidir com a borda da estrada
            self.x += self.speed_x

    def draw(self, surface):
        rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)
        return rect # Retorna o retângulo para possíveis colisões futuras