import pygame 
import pygame.mixer as mixer
import math
import random
import sys

# Inicializar o pygame e Criar a janela do jogo 
pygame.init()
altura = 560
largura = 840
screen = pygame.display.set_mode((largura,altura)) # criando a tela
game_state = "start_menu"

pygame.display.set_caption("Guerra Espacial")

# Fundo
fundo = pygame.image.load('Fundo.png')
tela_inicio = pygame.image.load('Tela_inicio.png')
tela_game_over = pygame.image.load('Game_Over.png')

# Objetos Do Jogo
# Jogador
velocidadeJogador = 4

JogadorIMG = pygame.image.load('Jogador.png') # Imagem da nave Jogador
JogadorLarguraIMG = 128 # pra subtrair na hora da borda
JogadorX = largura * 0.45 # pos inicial eixo X da nave
JogadorY = altura * 0.83 # pos inicial eixo Y da nave
Jogador_MudaX = 0 # isto sera somado ao JogadorX.

def posicionar_jogador():
    JogadorIMG = pygame.image.load('Jogador.png') # Imagem da nave Jogador
    JogadorLarguraIMG = 128 # pra subtrair na hora da borda
    JogadorX = largura * 0.45 # pos inicial eixo X da nave
    JogadorY = altura * 0.83 # pos inicial eixo Y da nave
    Jogador_MudaX = 0 # isto sera somado ao JogadorX.

# Inimigo
velocidadeInimigo = 6

# lista para os atributos de cada Inimigo.
InimigoIMG = []
InimigoLarguraIMG = []
InimigoX = []
InimigoY = []
Inimigo_MudaX = []
Inimigo_MudaY = []

# quantidade de inimigos
InimigoQuant = 7
#musica boladona do trabalho (FFXIV Scream)
mixer.Channel(0).play(mixer.Sound('Scream.mp3'))
mixer.Channel(1).set_volume(0.5)
#mixer.music.load('Scream.mp3')
#mixer.music.set_volume(0.65)
#mixer.music.play()

# inserindo os dados de cada Inimigo
def criaInimigos():
    for i in range(InimigoQuant):
        InimigoIMG.append(pygame.image.load('Inimigo.gif')) # Imagem pro Inimigo 
        InimigoIMG.append(pygame.image.load('Inimigo.gif')) # Imagem pro Inimigo
        InimigoLarguraIMG.append(50) # pra subtrair na hora da borda 
        InimigoX.append(random.randint(0, largura - InimigoLarguraIMG[i])) # pos inicial eixo X randomizado 
        InimigoY.append(altura * 0.01) # posicao inicial Y comum
        Inimigo_MudaX.append(random.randint(-1, 1) * velocidadeInimigo + 1) #  Deixamos uma velocidade randomica pra esquerda e direita para o eixo x 
        Inimigo_MudaY.append(random.randint(0, 9) * 0.06)  # Randomizamos um pouco a velocidade de queda 

def deletaInimigos():
    del InimigoIMG [:]
    del InimigoLarguraIMG [:]
    del InimigoX [:]
    del InimigoY [:]
    del Inimigo_MudaX [:]
    del Inimigo_MudaY [:]


# Missil
velocidadeMissil = 7
MissilIMG = pygame.image.load('Missil.png') 
MissilX = 0
MissilY = altura * 0.90
Missil_MudaX = 0 
Missil_MudaY = velocidadeMissil 
MissilEstado = "Carregado"

# utilizando formula de distancia entre cordenadas de dois pontos
def Colisao(X1,Y1,X2,Y2):
    Distancia = math.sqrt(math.pow(X1 - X2, 2) + (math.pow(Y1 - Y2, 2)))
    if Distancia <= 50  :
        ExplosaoIMG = pygame.image.load('Explosão.png') 
        screen.blit(ExplosaoIMG, (MissilX, MissilY))
        return True
    else:
        return False

# funcoes para cada objeto aparecer na tela.
def Jogador(x,y):
    screen.blit(JogadorIMG, (x,y)) # aqui estamos desenhando a nave sobre a janela do jogo(surface)
def Inimigo(x,y,i):
    screen.blit(InimigoIMG[i], (x,y)) 
def AtirarMissil(x,y): # comeca o lancamento do Missil 
    global MissilEstado
    MissilEstado = "Descarregado"
    screen.blit(MissilIMG, (x,y))

def Menu_Inicio():
   screen.fill((0, 0, 0))
   screen.blit(tela_inicio,(0,0))
   pygame.display.update()

def Menu_Game_Over():
   screen.fill((0, 0, 0, 0.6))
   font = pygame.font.SysFont('arial', 40)
   restart_button = font.render('R - Reiniciar', True, (255, 255, 255))
   quit_button = font.render('Q - Fechar a janela', True, (255, 255, 255))
   screen.blit(tela_game_over,(0,0))
   screen.blit(restart_button, (largura/2 - restart_button.get_width()/2, altura/1.8 + restart_button.get_height()))
   screen.blit(quit_button, (largura/2 - quit_button.get_width()/2, altura/1.9 + quit_button.get_height()/2))
   pygame.display.update()

game_over = False

# O jogo em si
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == "start_menu":
       Menu_Inicio()
       keys = pygame.key.get_pressed()
       if keys[pygame.K_SPACE]:
           game_state = "game"
           game_over = False
        
    if game_state == "game_over":
        Menu_Game_Over()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
           deletaInimigos()
           game_state = "start_menu"
        if keys[pygame.K_q]:
            pygame.quit()
            quit()
        
    elif game_state == "game":
        posicionar_jogador()
        criaInimigos()
        screen.fill((255,255,255)) # mudando a cor da janela pra branco
        screen.blit(fundo,(0,0))
        for event in pygame.event.get():
            if(event.type == pygame.QUIT): # caso o evento quit() é acionado, o programa fecha. o evento quit() é clicar no X na janela.
                running = False

        # Teclado Jogador
            if(event.type == pygame.KEYDOWN): # este evento verifica se uma tecla foi presionada 
                if(event.key == pygame.K_a): # caso seja a tecla A, decrementa de JogadorX
                    Jogador_MudaX -= velocidadeJogador
                if(event.key == pygame.K_d): # caso seja a tecla D, incrementa de JogadorX
                    Jogador_MudaX += velocidadeJogador
                if(event.key == pygame.K_SPACE): # caso seja a tecla espaco, verifica se o Missil esta na tela.
                    if(MissilEstado == "Carregado"): # aqui verificamos se o Missil esta na tela.
                        MissilX = JogadorX + JogadorLarguraIMG/4 # pegamos a posicao atual do Jogador para o Missil 
                        AtirarMissil(MissilX,MissilY) # atiramos o Missil de acordo com a posicao atual do Jogador 
            if(event.type == pygame.KEYUP): # este evento verifica se uma tecla foi solta, isso foi feito pra poder segurar a tecla 
                if(event.key == pygame.K_a):
                    Jogador_MudaX = 0
                if(event.key == pygame.K_d):
                    Jogador_MudaX = 0

        # Movimentos Jogador
        JogadorX = JogadorX + Jogador_MudaX  

        # Movimentos Missil
        if (MissilY < 0): 
            MissilY = altura * 0.90
            MissilEstado = "Carregado" # no momento que o Missil atinge o final do mapa, ele reseta.   
        if (MissilEstado == "Descarregado"): # enquanto o Missil nao chega no final do mapa, ele vai andando
            AtirarMissil(MissilX,MissilY)
            MissilY -= Missil_MudaY

        for i in range(InimigoQuant):
            # Movimentos Inimigo
            InimigoX[i] = InimigoX[i] + Inimigo_MudaX[i]  
            InimigoY[i] = InimigoY[i] + Inimigo_MudaY[i] 
            # Borda da tela para Inimigo
            if(InimigoX[i] < 0):
                Inimigo_MudaX[i] = velocidadeInimigo
            if(largura - InimigoLarguraIMG[i] < InimigoX[i]): 
                Inimigo_MudaX[i] = -velocidadeInimigo
            if(JogadorY <= InimigoY[i]): # Perdeu, deixou passar o asteroid
                for i in range(InimigoQuant):
                    Inimigo_MudaX[i] = 0 # inimigos param
                    Inimigo_MudaY[i] = 0 # inimigos param        
                game_over = True
                game_state = "game_over"
            # verificar se teve colisao entre o inimigo e o Missil
            Resultado = Colisao(InimigoX[i],InimigoY[i],MissilX,MissilY)
            if (Resultado):
                mixer.Channel(1).play(mixer.Sound('explosao.mp3'))
                MissilY = altura * 0.90
                MissilEstado = "Carregado" # caso aconteceu uma colisao, resetar o Missil
                InimigoX[i] = random.randint(0, largura - InimigoLarguraIMG[i]) # pos inicial eixo X da nave
                InimigoY[i] = altura * 0.01 # pos inicial eixo Y da nave
            Inimigo(InimigoX[i],InimigoY[i], i) # chamada da funcao para movimentar inimigo

        # Borda da tela para Jogador
        if(JogadorX < 0):
            JogadorX = 0.1
        if(largura - JogadorLarguraIMG < JogadorX):
            JogadorX = largura - JogadorLarguraIMG 
        
        # Chamadas 
        Jogador(JogadorX,JogadorY) # chamada da funcao Jogador para atualizar a pocisao do Jogador em cada frame
        pygame.display.update()