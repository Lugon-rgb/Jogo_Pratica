import pygame, sys, random
from pygame.locals import *

# VARIÁVEIS
screen_width = 14 * 77
screen_height = 8 * 77

# Define a taxa de atualização
clock = pygame.time.Clock()

camera_y = 0
gravity = 0.38

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
        pygame.draw.rect(screen, "white", platform)

def draw_player(x, y):
    pygame.draw.rect(screen, 'white', [x, y, player_size, player_size])

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
  global clock, tile, font
  
  clock = pygame.time.Clock()
  
  #mapa
  load_mapa("mapa.txt")
  tile['G'] = pygame.image.load("img/Tiles/grama.png")
  tile['A'] = pygame.image.load("img/Tiles/aguaMeio.png")

  tile['E'] = pygame.image.load("img/Tiles/flutuanteLadoEsquerdo.png")
  tile['D'] = pygame.image.load("img/Tiles/flutuanteLadoDireito.png")

  # Pontuação
  font = pygame.font.Font(None, 36)

def movimentacaoPersonagem():
  global velocidade_y, jump, player_x, player_y, player_size, player_speed
  keys = pygame.key.get_pressed()

  if keys[pygame.K_UP] and not jump:
    jump = True
    velocidade_y = 15  # Velocidade inicial do pulo
  if keys[pygame.K_LEFT] and player_x > 0:
      player_x -= player_speed
  elif player_x <= 0:
    player_x = 1077 - player_size
  
  if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
      player_x += player_speed
  elif player_x + player_size >= screen_width:
    player_x = 0 + player_size

# def pulo():
#   global jump_count, player_y
#   # Pula constantemente se não estiver pulando no momento
#   #if not jump:
#   if jump_count >= -10:
#     neg = 1
#     if jump_count < 0:
#         neg = -1
#     player_y -= (jump_count ** 2) * 0.5 * neg
#     jump_count -= 1
    
#   else:
#     jump = True
#     jump_count = 10

def pulo():
  global jump_count, player_y, jump, on_platform, gravity
  # Pula constantemente se não estiver pulando no momento
  #if not jump:
  if jump_count >= -10:
    neg = 1
    if jump_count < 0:
        neg = -1
    player_y -= (jump_count ** 2) * 0.5 * neg
    jump_count -= 1
    
  else:
    jump = True
    jump_count = 10
    player_y += 2
  
  # if player_y > screen_height:  # Limit the player to stay within the screen height
  #       player_y = screen_height - 200
  #       jump = False


def verificaColisao():
    global score, player_x, player_y, on_platform, inicio, camera_y
    # Verifica colisões
    on_platform = False  # Reset on_platform flag
    
    for platform in platforms:
        if (
            player_y < platform[1] + platform[3]
            and player_y + player_size > platform[1]
            and player_x + player_size > platform[0]
            and player_x < platform[0] + platform[2]
        ):
            player_y = platform[1] - player_size
            on_platform = True
            inicio = False
            camera_y = player_y  # Update camera_y to follow the player's position
            # Atualiza a pontuação se a plataforma estiver acima do y da câmera
            if platform[1] < camera_y:
                score += 1

    # Se não estiver em uma plataforma, o jogador está caindo
    if not on_platform and not inicio:
      
        player_y += 2
        

def moviCamera():
    global camera_y, player_y

    # Move a câmera para cima conforme o jogador sobe
    if player_y < camera_y + 200:
        camera_y = player_y - 200

def geraPlataforma():
  global platform_x, platform_y, camera_y, platform_height, platform_width
  camera_y = 0
  #Gera novas plataformas conforme a câmera sobe
  while len(platforms) < 10:
      platform_x = random.randint(0, screen_width - platform_width)
      platform_y = camera_y - random.randint(50, 200)
      platform = [platform_x, platform_y, platform_width, platform_height]
      platforms.append(platform)

def removePlataformaAntiga():
  # Remove plataformas antigas
  global platforms
  platforms = [platform for platform in platforms if platform[1] > camera_y - screen_height]


def update(dt):
  movimentacaoPersonagem()
  
  pulo()
  verificaColisao()
  moviCamera()
  geraPlataforma()
  removePlataformaAntiga()

  # # Verifica se o personagem atingiu o chão
  # if player_y > screen_width - player_size:
  #     player_y = screen_height - player_size
  #     jump = False
  # if player_y > screen_height:
  #   print("Você perdeu!")
  #   running = False




def draw(screen):
  global caixa, chao
  
  screen.fill((255,255,255))
  
  #pontuacao()
  
  #mapa
  for i in range(8): 
    for j in range(14):     
        screen.blit(tile[mapa[i][j]], ((j * 77), (i * 77)))

  draw_player(player_x, player_y)
  draw_platforms(platforms)
  draw_score(score)
        
    

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


'''
-----------------------------------------------------------------------------------------------------------------------------
'''



'''
-------------------------------------------------------------------------------------------------------------------------------
'''
  
#     # Verifica se o jogador atingiu o "novo chão" (fora da tela)
#     if player_y > height:
#         print("Você perdeu!")
#         running = False

'''
---------------------------------------------------------------------------------------------------------------------------------------
'''
