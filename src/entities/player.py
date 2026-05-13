import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self):
        self.width = 80
        self.height = 50
        self.lives = 3
        self.x = (SCREEN_WIDTH // 2) - (self.width // 2) # Nasce centralizado horizontalmente
        self.y = SCREEN_HEIGHT - self.height - 30 # Fixo na parte inferior da tela (Eixo Y não muda)
        self.speed_x = 7 # Velocidade do movimento lateral
        self.invincible = False
        self.invincible_duration = 3000 # 3 segundos (em milissegundos)
        self.last_collision_time = 0
        self.visible = True # Controla o piscar

        try:
            car_image = pygame.image.load("assets/images/main_car.png").convert_alpha()
            self.image = pygame.transform.scale(car_image, (self.width, self.height))
        except FileNotFoundError:
            print("Imagem do carro não encontrada. Usando retângulo como substituto.")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((200, 0, 0)) # Vermelho

    def update_invincibility(self):
        """Atualiza o estado de invencibilidade e o efeito visual."""
        if self.invincible:
            current_time = pygame.time.get_ticks()
            # Verifica se os 3 segundos passaram
            if current_time - self.last_collision_time > self.invincible_duration:
                self.invincible = False
                self.visible = True
            else:
                # Efeito de piscar: alterna a visibilidade a cada 100ms
                self.visible = (current_time // 100) % 2 == 0

    def move_left(self, track_left):
        if self.x > track_left + 20: # Pequena margem para não colidir com a borda da estrada
            self.x -= self.speed_x

    def move_right(self, track_right):
        if self.x < track_right - self.width - 20: # Pequena margem para não colidir com a borda da estrada
            self.x += self.speed_x

    def draw(self, surface):
        # Apenas desenha se estiver visível (efeito de piscar)
        if self.visible:
            surface.blit(self.image, (self.x, self.y))
        return self.image.get_rect(topleft=(self.x, self.y)) # Retorna o retângulo para possíveis colisões futuras