import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SKY_COLOR, GRASS_COLOR, ROAD_COLOR

class Track:
    def __init__(self):
        self.horizon_y = SCREEN_HEIGHT // 4 # Linha do horizonte na metade da tela
        self.road_width = SCREEN_WIDTH * 0.8 # Largura da estrada próxima ao jogador
        self.road_width_horizon = 100 # Largura da estrada no horizonte

    def draw(self, surface):
        # Desenha o céu
        sky_rect = pygame.Rect(0,0, SCREEN_WIDTH, self.horizon_y)
        pygame.draw.rect(surface, SKY_COLOR, sky_rect)

        # Desenha a grama
        grass_rect = pygame.Rect(0, self.horizon_y, SCREEN_WIDTH, SCREEN_HEIGHT - self.horizon_y)
        pygame.draw.rect(surface, GRASS_COLOR, grass_rect)

        # Criação da estrada usando um polígono
        road_polygon = [
            ((SCREEN_WIDTH // 2) - (self.road_width_horizon // 2), self.horizon_y), # Ponto esquerdo no horizonte
            ((SCREEN_WIDTH // 2) + (self.road_width_horizon // 2), self.horizon_y), # Ponto direito no horizonte
            ((SCREEN_WIDTH // 2) + (self.road_width // 2), SCREEN_HEIGHT), # Ponto direito próximo
            ((SCREEN_WIDTH // 2) - (self.road_width // 2), SCREEN_HEIGHT) # Ponto esquerdo próximo
        ]

        # Desenha a estrada
        pygame.draw.polygon(surface, ROAD_COLOR, road_polygon)