import pathlib
import random
import pygame
import sys
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.core.scoreboard import Scoreboard
from src.entities.track import Track
from src.entities.player import Player
from src.entities.npc import NPC
from src.ui.hud import HUD
from src.ui.menu import Menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Enduro Game")
    clock = pygame.time.Clock()
    pygame.mixer.init() # Inicia o sistema de som
    
    # --- CARREGAMENTO DE ASSETS ---
    try:
        # Carrega a Música (Deixe em loop infinito)
        pygame.mixer.music.load("assets/sounds/tokyo-drift-soundtrack.wav")
        pygame.mixer.music.set_volume(0.4) # Música de fundo (mais baixa)
        # Carrega o Som de Game Over
        game_over_sound = pygame.mixer.Sound("assets/sounds/spongebob_fail.mp3")
        # Carrega o Som da Batida
        crash_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
        # Carrega as imagens de fundo (parallax)
        cloud_image = pygame.image.load("assets/images/clouds.jpg").convert_alpha()
        mountain_image = pygame.image.load("assets/images/mount.png").convert_alpha()
        # Carrega as imagens dos NPCs
        npc_images = [pygame.image.load(image_path).convert_alpha() for image_path in pathlib.Path("assets/images/").glob("npc_*.png")]
        grass_images = [pygame.image.load(grass_path).convert_alpha() for grass_path in pathlib.Path("assets/images/").glob("grassandflowers*.png")]
    except FileNotFoundError as e:
        print(f"Erro ao carregar asset: {e}")
        print("Certifique-se de que todos os arquivos necessários estão na pasta 'assets'.")
        pygame.quit()
        sys.exit()

    # --- Configurações iniciais do jogo ---
    scoreboard = Scoreboard()
    game_state = "MENU" # Estados possíveis: "MENU", "PLAYING", "GAME_OVER"
    menu = Menu()
    track = None
    player = None
    hud = None
    active_npcs = [] # Lista de inimigos ativos na tela
    npc_spawn_timer = 0
    max_speed = 7.0  # Velocidade máxima do jogo
    acceleration = 0.02 # O quão rápido ele chega na velocidade máxima

    def reset_game():
        """Zera todas as instâncias para uma nova partida limpa"""
        nonlocal track, player, hud, active_npcs, npc_spawn_timer
        track = Track(grass_images, cloud_image, mountain_image)
        track.speed = 0.0
        player = Player()
        hud = HUD()
        active_npcs = []
        npc_spawn_timer = 0
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # O ESC agora volta do ranking pro menu, ou fecha o jogo
                if event.key == pygame.K_ESCAPE:
                    if game_state == "LEADERBOARD":
                        game_state = "MENU"
                    else:
                        running = False

            # --- CONTROLE DOS MENUS VIA TECLADO ---
                if event.key == pygame.K_RETURN: # Tecla ENTER
                    if game_state == "MENU":
                        reset_game()
                        game_state = "PLAYING"
                        pygame.mixer.music.play(-1) # O -1 faz a música repetir para sempre
                    elif game_state == "GAME_OVER":
                        reset_game()
                        game_state = "MENU"
                elif event.key == pygame.K_TAB and game_state == "MENU":
                    game_state = "LEADERBOARD"

        # ==========================================
        # ESTADO 1: TELA DE MENU INICIAL
        # ==========================================
        if game_state == "MENU":
            menu.draw_main_menu(screen)

        # ==========================================
        # ESTADO 2: JOGO RODANDO
        # ==========================================
        elif game_state == "PLAYING":

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.move_left(track_left=track_rect.left)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.move_right(track_right=track_rect.right)
            
            # --- NOVO: CONTROLE DE COLISÃO E ACELERAÇÃO ---
            current_time = pygame.time.get_ticks()
            
            # Verifica se o jogador bateu há menos de 1.5s (1500ms)
            is_crashed = player.invincible and (current_time - player.last_collision_time < 1500)

            if hud.score >= 2000: # A partir de 2000 pontos, o jogo fica mais difícil (aceleração aumenta)
                max_speed = 12.0

            if is_crashed:
                track.speed = 0.0  # Pista e faixas param completamente
            else:
                # Aceleração normal retoma após 1.5s
                if track.speed < max_speed:
                    track.speed += acceleration

            # --- GERADOR DE INIMIGOS (SPAWNER) ---
            npc_spawn_timer += 1
            # Sorteia um inimigo a cada ~1 a 3 segundos (assumindo 60 FPS)
            if npc_spawn_timer > random.randint(60, 180) and track.speed > 1:
                npc_spawn_timer = 0
                # Nasce um inimigo no horizonte
                novo_npc = NPC(track.horizon_y, npc_images)
                active_npcs.append(novo_npc)

            track.update()
            player.update_invincibility() # Atualiza o estado de invencibilidade do jogador
            hud.update(track.speed)

            for npc in active_npcs:
                npc.update(track.speed, track.horizon_y)
                
            # Remove os NPCs que já passaram muito da base da tela ou passaram do horizonte (para otimizar)
            active_npcs = [npc for npc in active_npcs if track.horizon_y < npc.y <= SCREEN_HEIGHT + 400]

            track_rect = track.draw(screen)
            
            active_npcs.sort(key=lambda n: n.y) # Isso garante que o carro de trás não seja desenhado por cima do carro da frente!
            
            for npc in active_npcs:
                npc_rect = npc.draw(screen, track) # Agora passamos a track inteira para ele saber calcular a curva

                # VERIFICAÇÃO DE COLISÃO
                # Só checa se o NPC estiver na tela e o jogador NÃO for invencível
                if npc_rect and player_rect.colliderect(npc_rect) and not player.invincible:
                    player.lives -= 1
                    crash_sound.play() # Toca o som da batida
                    player.invincible = True
                    player.last_collision_time = pygame.time.get_ticks()
                    
                    # Penalidade de velocidade (estilo Enduro)
                    track.speed = 0.0 
                    
                    if player.lives <= 0:
                        game_over_sound.play() # Toca o som de game over
                        scoreboard.save_score(hud.score)
                        game_state = "GAME_OVER"
                
            player_rect = player.draw(screen)
            # Vai escurecer/tingir o cenário, os inimigos e o jogador!
            track.draw_time_overlay(screen)
            hud.draw(screen, player, track.speed)

        # ==========================================
        # ESTADO 3: GAME OVER
        # ==========================================
        elif game_state == "GAME_OVER":
            pygame.mixer.music.stop() # Para a música de fundo
            menu.draw_game_over(screen, hud.score)

        # ==========================================
        # ESTADO 4: LEADERBOARD
        # ==========================================
        elif game_state == "LEADERBOARD":
            # Passamos a lista de scores que já está na memória da classe Scoreboard
            menu.draw_leaderboard(screen, scoreboard.scores)

        pygame.display.flip() # Atualiza a tela
        clock.tick(FPS) # Controla a taxa de quadros por segundo

    # Encerra o Pygame e sai do programa
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()