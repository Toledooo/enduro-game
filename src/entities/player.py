import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self):
        self.width = 100
        self.height = 80
        
        # Nasce centralizado horizontalmente
        self.x = (SCREEN_WIDTH // 2) - (self.width // 2)
        
        # Fixo na parte inferior da tela (Eixo Y não muda)
        self.y = SCREEN_HEIGHT - self.height - 30 
        
        self.speed_x = 7 # Velocidade do movimento lateral

        try:
            car_image = pygame.image.load("assets/images/main_car.png").convert_alpha()
            self.image = pygame.transform.scale(car_image, (self.width, self.height))
        except FileNotFoundError:
            print("Imagem do carro não encontrada. Usando retângulo como substituto.")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((200, 0, 0)) # Vermelho

    def move_left(self, track_left):
        if self.x > track_left + 20: # Pequena margem para não colidir com a borda da estrada
            self.x -= self.speed_x

    def move_right(self, track_right):
        if self.x < track_right - self.width - 20: # Pequena margem para não colidir com a borda da estrada
            self.x += self.speed_x

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        rect = self.image.get_rect(topleft=(self.x, self.y))
        return rect # Retorna o retângulo para possíveis colisões futuras