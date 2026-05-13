import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class HUD:
    def __init__(self):
        # Inicializa as fontes do Pygame
        pygame.font.init()
        # Usa uma fonte de sistema estilo "máquina de escrever" ou pixelada para dar um ar retrô
        self.font = pygame.font.SysFont("Courier New", 24, bold=True)
        self.score = 0.0

    def update(self, track_speed):
        # A pontuação (distância) aumenta baseada na velocidade atual da pista
        # Se você bater e a pista parar, a pontuação também para de subir
        if track_speed > 0:
            self.score += track_speed * 0.1

    def draw(self, surface, player, track_speed):
        # --- Configurações do Painel ---
        panel_width = 220
        panel_height = 110
        # Posiciona no canto inferior direito, com uma margem de 20 pixels
        panel_x = SCREEN_WIDTH - panel_width - 20
        panel_y = SCREEN_HEIGHT - panel_height - 20
        
        # Desenha o fundo do painel (Cinza escuro, opaco)
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(surface, (30, 30, 30), panel_rect)
        # Desenha a borda do painel (Branca, 3 pixels de espessura)
        pygame.draw.rect(surface, (200, 200, 200), panel_rect, 3)

        # --- Renderização dos Textos ---
        # Converte a velocidade do motor (ex: 35.0) para uma escala visual de km/h (ex: 350 km/h)
        velocidade_visual = int(track_speed * 20)
        
        speed_text = self.font.render(f"Vel:  {velocidade_visual} km/h", True, (255, 255, 100)) # Amarelo
        score_text = self.font.render(f"Score: {int(self.score)} m", True, (255, 255, 255)) # Branco
        lives_text = self.font.render(f"Vidas: {player.lives}", True, (255, 100, 100)) # Vermelho

        # --- Posicionamento dos Textos dentro do Painel ---
        surface.blit(speed_text, (panel_x + 15, panel_y + 15))
        surface.blit(score_text, (panel_x + 15, panel_y + 45))
        surface.blit(lives_text, (panel_x + 15, panel_y + 75))