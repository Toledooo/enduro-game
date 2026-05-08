import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, SKY_COLOR, GRASS_COLOR, ROAD_COLOR, WHITE

class Track:
    def __init__(self):
        self.horizon_y = SCREEN_HEIGHT // 4 # Linha do horizonte na metade da tela
        self.road_width = SCREEN_WIDTH * 0.8 # Largura da estrada próxima ao jogador
        self.road_width_horizon = 100 # Largura da estrada no horizonte
        self.speed = 0
        self.lines_y = []
        self.spawn_timer = 0
        self.spawn_delay_base = 19  # Tempo base de geração (em frames)

    def update(self):
        # Se o carro tiver velocidade, as faixas se movem para baixo
        if self.speed > 0:
            # 1. Gerador de faixas no tempo
            self.spawn_timer += 1
            
            # Quanto maior a velocidade, menor o tempo de espera (delay) para gerar a próxima faixa.
            # Isso evita que fique um "buraco" gigante entre as faixas em altas velocidades.
            current_delay = max(5, self.spawn_delay_base - int(self.speed * 0.8))

            if self.spawn_timer >= current_delay:
                self.lines_y.append(self.horizon_y)  # Nova faixa nasce no horizonte
                self.spawn_timer = 0

            # 2. Movimento das faixas para baixo
            for i in range(len(self.lines_y)):
                distance_from_horizon = self.lines_y[i] - self.horizon_y
                line_speed = (self.speed * 0.5) + (distance_from_horizon * 0.05)
                self.lines_y[i] += line_speed

            # 3. Limpeza de Memória
            # Mantém na lista apenas as faixas que ainda estão dentro da tela.
            self.lines_y = [y for y in self.lines_y if y <= SCREEN_HEIGHT]
    def draw(self, surface):
        # Desenha o céu
        sky_rect = pygame.Rect(0,0, SCREEN_WIDTH, self.horizon_y)
        pygame.draw.rect(surface, SKY_COLOR, sky_rect)

        # Desenha a grama
        grass_rect = pygame.Rect(0, self.horizon_y, SCREEN_WIDTH, SCREEN_HEIGHT - self.horizon_y)
        pygame.draw.rect(surface, GRASS_COLOR, grass_rect)

        # Criação da estrada usando um polígono
        road_polygon = [
            ((SCREEN_WIDTH // 2) - (self.road_width_horizon // 2.5), self.horizon_y), # Ponto esquerdo no horizonte
            ((SCREEN_WIDTH // 2) + (self.road_width_horizon // 2.5), self.horizon_y), # Ponto direito no horizonte
            ((SCREEN_WIDTH // 2) + (self.road_width // 2.5), SCREEN_HEIGHT), # Ponto direito próximo
            ((SCREEN_WIDTH // 2) - (self.road_width // 2.5), SCREEN_HEIGHT) # Ponto esquerdo próximo
        ]

        # Desenha a estrada
        street_rect = pygame.draw.polygon(surface, ROAD_COLOR, road_polygon)

        for line in self.lines_y:
            # Não desenha se estiver exatamente no horizonte (questão estética)
            if line <= self.horizon_y + 2:
                continue
                
            # Calcula o "fator de escala" (0.0 no horizonte, 1.0 na base da tela)
            scale = (line - self.horizon_y) / (SCREEN_HEIGHT - self.horizon_y)
            
            # A largura e altura da faixa crescem conforme ela desce
            line_width = max(4, int(20 * scale))
            line_height = max(2, int(40 * scale))
            
            # Desenha a faixa no centro do X, na altura Y atual
            line_rect = pygame.Rect((SCREEN_WIDTH // 2) - (line_width // 2), int(line), line_width, line_height)
            pygame.draw.rect(surface, WHITE, line_rect)

        return street_rect # Retorna o polígono da estrada para possíveis colisões futuras