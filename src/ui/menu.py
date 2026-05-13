import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Menu:
    def __init__(self):
        pygame.font.init()
        
        # Tenta carregar uma fonte retrô customizada (se você baixar e colocar na pasta)
        try:
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 60)
            self.game_over_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 50)
        except FileNotFoundError:
            # Fallback: Se não achar o arquivo, usa a Impact (nativa, grossa e pesada)
            self.title_font = pygame.font.SysFont("Impact", 80)
            self.game_over_font = pygame.font.SysFont("Impact", 70)

        # Fonte menor para as instruções
        self.text_font = pygame.font.SysFont("Courier New", 24, bold=True)

    def draw_main_menu(self, surface):
        surface.fill((10, 10, 20)) # Fundo escuro
        
        # Título do jogo
        title_text = self.title_font.render("ENDURO", True, (255, 255, 100))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        surface.blit(title_text, title_rect)

        # Instrução de Start (com efeitinho de piscar)
        current_time = pygame.time.get_ticks()
        if (current_time // 500) % 2 == 0: # Pisca a cada 500ms
            start_text = self.text_font.render("Pressione ENTER para Jogar", True, (255, 255, 255))
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            surface.blit(start_text, start_rect)

    def draw_game_over(self, surface, final_score):
        # Efeito Fade: Cria uma película escura semi-transparente por cima do jogo pausado
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180) # Nível de transparência (0 a 255)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # Texto GAME OVER
        go_text = self.game_over_font.render("GAME OVER", True, (255, 50, 50))
        go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        surface.blit(go_text, go_rect)

        # Pontuação Final
        score_text = self.text_font.render(f"Distância Final: {int(final_score)} m", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(score_text, score_rect)

        # Instrução de Restart
        current_time = pygame.time.get_ticks()
        if (current_time // 500) % 2 == 0:
            restart_text = self.text_font.render("Pressione ENTER para Tentar Novamente", True, (200, 200, 200))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            surface.blit(restart_text, restart_rect)