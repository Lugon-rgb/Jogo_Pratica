import pygame, sys, random
from pygame.locals import *

# VARIÁVEIS
screen_width = 10 * 77
screen_height = 8 * 77
game_over = False
defeat_font = None
start_following = False
screen_treshold = screen_height / 5.5
following_intepolatioin = 0.009

# Define a taxa de atualização
clock = pygame.time.Clock()

camera_y = 0

#mapa
mapa = []
tile={} # Usando dicionário

# Jogador
player_size = 50
player_x = screen_width // 2 - player_size // 2
player_y = screen_height - player_size
player_speed = 15
jump = False
jump_count = 10
velocidade_y = 1.45

on_platform = False
score = 0


# Plataformas
platform_width = 200
platform_height = 20
platforms = []

font = None

inicio = True

def comentarios():
  pass
  # #personagem variáveis
  # dino_walk = []
  # dino_frameAnim = 1
  # dino_x = 100
  # dino_y = 300
  # direcao = "direita"
  # dino_TimeAnim = 0

  #load
   #personagem
  # for i in range(1, 11):
  #   dino_walk.append(pygame.image.load("img/Personagem/Walk("+str(i)+").png"))

  #Pontuação
  #  fonte = pygame.font.Font(, 20)

  #UPDATE
  #old_x, old_y = dino_x, dino_y

  #personagem (dino)
  # if keys[pygame.K_RIGHT]:
  #   direcao = "direita"
  #   dino_x = dino_x + (0.1 * dt)
  #   dino_TimeAnim = dino_TimeAnim + dt
  #   if dino_TimeAnim > 100:
  #     dino_frameAnim = dino_frameAnim + 1      
  #     if dino_frameAnim > 9:
  #       dino_frameAnim = 1
  #     dino_TimeAnim = 0

  # if keys[pygame.K_LEFT]:
  #   direcao = "esquerda"
  #   dino_x = dino_x - (0.1 * dt)
  #   dino_TimeAnim = dino_TimeAnim + dt
  #   if dino_TimeAnim > 100:
  #     dino_frameAnim = dino_frameAnim - 1      
  #     if dino_frameAnim < 1:
  #       dino_frameAnim = 9
  #     dino_TimeAnim = 0

  # Alterar escala da imagem
  #dino_walk[dino_frameAnim] = pygame.transform.scale(dino_walk[dino_frameAnim], (210, 210))

  #DRAW
  #personagem (dino)
  #screen.blit(dino_walk[dino_frameAnim], (dino_x, dino_y))


# Adiciona plataformas a cada 200 pixels no eixo y
for i in range(0, screen_height, 160):
  platform_x = random.randint(0, screen_width - platform_width)
  platform_y = i
  platform = [platform_x, platform_y, platform_width, platform_height]
  platforms.append(platform)

# Função para desenhar as plataformas na tela
def draw_platforms(platforms):
    for platform in platforms:
        pygame.draw.rect(screen, "white", (platform[0], platform[1] - camera_y, platform[2], platform[3]))


def draw_player(x, y):
    pygame.draw.rect(screen, 'white', [x, y - camera_y, player_size, player_size])

def draw_score(score):
    score_text = font.render("Pontuação: " + str(score), True, "white")
    screen.blit(score_text, (10, 10))

# FUNÇÕES
def load_mapa(filename): # Lê o conteúdo do arquivo para a matriz
  global mapa
  file = open(filename,"r")
  for line in file.readlines():
   mapa.append(line)
  file.close()

def load():
  global clock, tile, font, defeat_font
  
  clock = pygame.time.Clock()
  
  #mapa
  load_mapa("mapa.txt")
  tile['G'] = pygame.image.load("img/Tiles/grama.png")
  tile['A'] = pygame.image.load("img/Tiles/aguaMeio.png")

  tile['E'] = pygame.image.load("img/Tiles/flutuanteLadoEsquerdo.png")
  tile['D'] = pygame.image.load("img/Tiles/flutuanteLadoDireito.png")

  # Pontuação
  font = pygame.font.Font(None, 36)
  defeat_font = pygame.font.Font(None, 60)

def movimentacaoPersonagem():
  global velocidade_y, jump, player_x, player_y, player_size, player_speed
  keys = pygame.key.get_pressed()

  if keys[pygame.K_UP] and not jump:
    jump = True
    velocidade_y = 15  # Velocidade inicial do pulo
  if keys[pygame.K_LEFT] and player_x > 0:
      player_x -= player_speed
  elif player_x <= 0:
    player_x = (screen_width - 1) - player_size
  
  if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
      player_x += player_speed
  elif player_x + player_size >= screen_width:
    player_x = 0 + player_size

def pulo():
  global jump_count, player_y, jump, on_platform, gravity, velocidade_y
  # Pula constantemente se não estiver pulando no momento
  #if not jump:
  
  if jump_count >= -10:
      neg = 1
      if jump_count < 0:
          neg = -1
      player_y -= (jump_count ** 2) * 0.32 * neg * velocidade_y
      jump_count -= 1
    
  elif jump_count <= -10 and on_platform == True or (on_platform == False and inicio == True):
      jump = True
      jump_count = 10
  elif jump_count < -10 and inicio== False:
    jump_count = -11
    player_y += 10 ** gravity
    on_platform = False


def verificaColisao():
    global score, player_x, player_y, on_platform, inicio, camera_y, player_size
    on_platform = False  # Reset on_platform flag
    for platform in platforms:
        # Define the platform's hitbox
        platform_hitbox = pygame.Rect(platform[0], platform[1] - camera_y, platform[2], platform[3])

        # Check for collision using the colliderect() method
        if player_hitbox.colliderect(platform_hitbox):
            player_y = platform[1] + camera_y - player_size
            on_platform = True
            inicio = False
            camera_y = player_y
            if platform[1] < camera_y:
                score += 1

    if not on_platform and not inicio:
        player_y += 2

# def verificaColisao():
#     global score, player_x, player_y, on_platform, inicio, camera_y
#     # Verifica colisões
#     on_platform = False  # Reset on_platform flag
    
#     for platform in platforms:
#         if (
#             player_y < platform[1] + platform[3]
#             and player_y + player_size > platform[1]
#             and player_x + player_size > platform[0]
#             and player_x < platform[0] + platform[2]
#         ):
#             player_y = platform[1] - player_size
#             on_platform = True
#             inicio = False
#             camera_y = player_y  # Update camera_y to follow the player's position
#             # Atualiza a pontuação se a plataforma estiver acima do y da câmera
#             if platform[1] < camera_y:
#                 score += 1

#     # Se não estiver em uma plataforma, o jogador está caindo
#     if not on_platform and not inicio:
      
#         player_y += 2
        

def moviCamera():
    global camera_y, player_y, start_following

    if start_following:
        target_y = player_y - 200  # Adjust this value as needed
        camera_y += (target_y - camera_y) * 0.005  # Adjust the interpolation factor as needed


def geraPlataforma():
  global platform_x, platform_y, camera_y, platform_height, platform_width
  #Gera novas plataformas conforme a câmera sobe
  while len(platforms) < 10:
      platform_x = random.randint(0, screen_width - platform_width)
      platform_y = camera_y - random.randint(50, 200)
      platform = [platform_x, platform_y, platform_width, platform_height]
      platforms.append(platform)

def removePlataformaAntiga():
  global platforms
  # Remove plataformas antigas
  global platforms
  platforms = [platform for platform in platforms if platform[1] > camera_y - screen_height]


def update(dt):
    global game_over, start_following
    movimentacaoPersonagem()
  
    pulo()
    verificaColisao()

    if player_y < screen_height / 8:  # Adjust this threshold as needed
        start_following = True

    if start_following:
        moviCamera()
        geraPlataforma()
        removePlataformaAntiga()

    if player_y > screen_height:
        game_over = True


def draw_background(screen, background_image, camera_y):
    # Calculate the starting position of the background based on the camera
    start_x = 0
    start_y = (camera_y // 128) * 128

    # Draw multiple instances of the background to cover the entire visible screen
    for i in range(8):  # Number of rows to cover the screen
        for j in range(14):  # Number of columns
            screen.blit(background_image, (j * 128, start_y + i * 128))


def draw(screen):
  global caixa, chao, game_over, start_following
  
  screen.fill((255,255,255))
  
  #pontuacao()
  
  #mapa
  for i in range(8):
    for j in range(14):
        screen.blit(tile[mapa[i][j]], ((j * 77), (i * 77) - camera_y))

  if start_following:
        # Draw the background tiles only after scrolling starts
        draw_background(screen, tile['A'], camera_y)

  draw_player(player_x, player_y)
  draw_platforms(platforms)
  draw_score(score)
  
  if game_over == True:
        defeat_text = defeat_font.render("Você perdeu!", True, "red")
        text_rect = defeat_text.get_rect(center=(screen_width // 2, (screen_height // 2) - camera_y))
        screen.blit(defeat_text, text_rect.topleft)

        
    

# CÓDIGO PRINCIAPL
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sky Jump")

load()
running = True
while running:
  clock.tick(60)
  dt = clock.get_time()

  draw(screen)
  update(dt)
  

  for event in pygame.event.get():
    if event.type == QUIT:
      running = False
      break

  pygame.display.update()

pygame.quit()
sys.exit()
