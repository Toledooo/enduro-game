# Enduro - Pygame Remake V1

Este projeto é uma releitura do clássico jogo **Enduro** (1983), originalmente desenvolvido pela Activision para o Atari 2600. O objetivo é recriar a experiência de corrida de resistência, onde o jogador deve ultrapassar um número determinado de carros para avançar para o próximo dia, enfrentando variações climáticas e de visibilidade.

## 💻 Desenvolvedores

* **Gabriel Toledo** - [GitHub](https://github.com/Toledooo)
* **Marcelo Boeira** - [GitHub](https://github.com/MarceloFBoeira)

## 🚘 O Projeto

O jogo está sendo desenvolvido em **Python** utilizando a biblioteca **Pygame**. O foco é manter a fidelidade à mecânica original enquanto aplicamos boas práticas de engenharia de software e design de sistemas.

## 🏁 Características e Funcionalidades

* **Motor Pseudo-3D:** Renderização de pista com curvas dinâmicas, escalonamento de sprites (NPCs e cenário) baseados em perspectiva e matemática de ponto de fuga.
* **Ciclo de Dia e Noite:** Sistema de passagem de tempo utilizando filtros de sobreposição (*Screen Overlay*) que tingem o cenário suavemente entre o dia, pôr do sol, noite e amanhecer.
* **Cenário em Parallax:** Fundo de tela multi-camadas (Céu e Montanhas) rolando em velocidades independentes para criar uma sensação de profundidade profunda durante as curvas.
* **Máquina de Estados (FSM):** Gerenciamento de fluxo de jogo segmentado entre Menu Inicial, Gameplay, Game Over e Leaderboard.
* **Sistema de Colisões:** Física de penalidade de velocidade e período de invencibilidade (efeito *blink*) após batidas, recriando o peso punitivo do Enduro original.
* **Leaderboard Local:** Sistema de *Highscores* com salvamento persistente (Auto-save) em formato `.json`, registrando as 5 maiores distâncias percorridas e suas respectivas datas.
* **Design de Áudio:** Trilha sonora contínua e efeitos sonoros programados (batidas e Game Over) gerenciados via `pygame.mixer`.

## 🎮 Controles

| Tecla | Ação |
| :--- | :--- |
| `Seta Esquerda` ou `A` | Virar o carro para a Esquerda |
| `Seta Direita` ou `D` | Virar o carro para a Direita |
| `ENTER` | Iniciar jogo / Confirmar (Menus) |
| `TAB` | Acessar o Leaderboard (Menu Inicial) |
| `ESC` | Voltar ao Menu / Sair do Jogo |

## 🛠️ Como Executar

**Pré-requisitos:**
* Python 3.8 ou superior instalado em sua máquina.

**Passo a passo:**
1. Clone este repositório para a sua máquina local.
2. É recomendada a criação de um ambiente virtual (venv):
   ```bash
   python -m venv venv
   source venv/bin/activate  # (No Windows: venv\Scripts\activate)
   ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4. Execute o jogo:
    ```bash
    python main.py
    ```

## 📂 Estrutura do Projeto

```text
/
├── assets/                 # Recursos visuais e sonoros
│   ├── audio/              # Efeitos sonoros (.wav, .mp3)
│   ├── fonts/              # Fontes customizadas (ex: PressStart2P.ttf)
│   └── images/             # Sprites de grama, carros, céu e montanhas
├── src/
│   ├── core/
│   │   ├── settings.py     # Constantes globais (Resolução, Cores, FPS)
│   │   └── scoreboard.py   # Lógica de leitura e gravação do JSON
│   ├── entities/
│   │   ├── track.py        # Matemática da pista, horizonte e parallax
│   │   ├── player.py       # Lógica e movimentação do jogador
│   │   └── npc.py          # Lógica e movimentação dos personagens
│   └── ui/
│       ├── hud.py          # Renderização de Pontuação, Velocidade e Vidas
│       └── menu.py         # Telas de Início, Game Over e Ranking
├── main.py                 # Ponto de entrada e Loop Principal (Máquina de Estados)
└── requirements.txt        # Dependências do Python
```
## 🎵 Créditos e Assets
Este projeto utiliza recursos visuais e sonoros criados por terceiros. Agradecemos aos seguintes criadores e plataformas:

**Áudio e Trilha Sonora:**

- Música de Fundo: [[Tokyo Drift (Fast & Furious)](https://www.youtube.com/watch?v=pS5d77DQHOI)] por [[Teriyaki Boyz](https://www.youtube.com/channel/UCRLFCARcsV7Iw_XENoNvrsg)] - Obtido em: [[Yout.com](https://www.yout.com/)]

- Efeitos Sonoros (Batida): Gerado através da ferramenta sfxr.me / Obtido em: [[sfxr.me](https://sfxr.me/)]

- Efeito Game Over: [SpongeBob Fail] - Obtido em: [[Myinstants](https://www.myinstants.com/)]

**Artes Visuais (Imagens e Sprites):**

- Carros (Player e NPCs): Criados por [[freepik](https://www.magnific.com/author/freepik)] - Obtido em: [[magnific.com]([https://itch.io/game-assets](https://www.magnific.com/free-ai-image/8-bits-cars-gaming-assets_133331049.htm#fromView=search&page=1&position=4&uuid=5ca473f0-4418-44e3-8d87-dbd738bb7b3a&query=Pixel+car+back+view?log-in=google))]

- Cenário (Montanhas e Nuvens): Criados por [Free Game Assets (GUI, Sprite, Tilesets)] - Obtido em: [[itch.io](https://free-game-assets.itch.io/)]

- Texturas (Grama): Pacote de 32 sprites por [[styloo](https://styloo.itch.io/)] - Obtido em: [[itch.io](https://styloo.itch.io/pixel-grass-and-flowers)]

**Tipografia:**

- Fonte do Título: [Press Start 2P] por [CodeMan38] - Obtido em: [[Google Fonts](https://fonts.google.com/)]
