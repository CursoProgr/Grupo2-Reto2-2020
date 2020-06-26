#Breakout
import sys #Para usar exit
import time
import pygame
from pygame import mixer


ANCHO = 720
ALTO = 640
color_fondo = (0, 0, 64)

mixer.init()
mixer.music.load("sonidos/Robot_City.mp3") #Cargamos la musica
mixer.music.play(-1) #Reproducimos la musica (esta en -1 asi se hace un loop de la musica)

pygame.init()

class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Cargamos imagen pelota
        self.image = pygame.image.load('imagenes/bola.png')
        #Le damos la forma de rectángulo a la pelota, en base a lo que ocupa la imagen
        self.rect = self.image.get_rect()
        #Le damos posición inicial a la pelota
        self.rect.centerx = ANCHO/2
        self.rect.centery = ALTO/2
        #Le damos velocidad
        self.speed = [7, 7]

    def update(self):
        #Evitar que la pelota salga por abajo
        if self.rect.bottom >= ALTO:
            self.speed[1] = -self.speed[1]
        #Evitar que la pelota salga por izquierda
        if self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        #Evitar que la pelota salga por arriba
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        #Evitar que la pelota salga por derecha
        if self.rect.right >= ANCHO:
            self.speed[0] = -self.speed[0]
        #La creamos para mover la pelota a su velocidad
        self.rect.move_ip(self.speed)

class Paleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Cargamos imagen pelota
        self.image = pygame.image.load('imagenes/paleta.png')
        #Le damos la forma de rectángulo a la paleta, en base a lo que ocupa la imagen
        self.rect = self.image.get_rect()
        #Le damos posición inicial a la paleta
        self.rect.midbottom = (ANCHO/2, ALTO -20)
        #Le damos velocidad
        self.speed = [0, 0]
    def update(self, evento):
        #Buscar si apreta la tecla izquierda
        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-20, 0]
        #Buscar si se apreta la derecha
        elif evento.key == pygame.K_RIGHT and self.rect.right < ANCHO:
            self.speed = [20, 0]
        else:
            self.speed = [0, 0]
        #La creamos para mover la paleta a su velocidad
        self.rect.move_ip(self.speed)

class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        #Cargamos imagen pelota
        self.image = pygame.image.load('imagenes/ladrillo.png')
        #Le damos la forma de rectángulo al ladrillo, en base a lo que ocupa la imagen
        self.rect = self.image.get_rect()
        #Posición inicial, dada
        self.rect.topleft = posicion

class Muro(pygame.sprite.Group):
    def __init__(self, cantidadLadrillos):
        pygame.sprite.Group.__init__(self)

        pos_x = 0
        pos_y = 20
        for i in range(cantidadLadrillos):
            ladrillo = Ladrillo((pos_x, pos_y))
            self.add(ladrillo)

            pos_x += ladrillo.rect.width
            if pos_x >= ANCHO:
                pos_x = 0
                pos_y += ladrillo.rect.height

#Creamos la función para perder y terminar el juego
def juego_terminado():
    fuente = pygame.font.SysFont('Arial', 72)
    texto = fuente.render('Perdiste!!!', True, (255, 255, 255))
    texto_rect = texto.get_rect()
    texto_rect.center = [ANCHO /2, ALTO /2]
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    #Esperar 3 segundos
    time.sleep(5)
    #Salir
    sys.exit()
def puntos():
    fuente = pygame.font.SysFont('Consolas', 20)
    texto = fuente.render(str(puntuacion).zfill(5), True, (255, 255, 255))
    texto_rect = texto.get_rect()
    texto_rect.topleft = [0, 0]
    pantalla.blit(texto, texto_rect)
def mostrar_vidas():
    fuente = pygame.font.SysFont('Consolas', 20)
    cadena = "Vidas: " + str(vidas).zfill(2)
    texto = fuente.render(cadena, True, (255, 255, 255))
    texto_rect = texto.get_rect()
    texto_rect.topright = [ANCHO, 0]
    pantalla.blit(texto, texto_rect)
def ganar():
    fuente = pygame.font.SysFont('Arial', 72)
    texto = fuente.render('Ganaste crack!', True, (255, 255, 255))
    texto_rect = texto.get_rect()
    texto_rect.center = [ANCHO /2, ALTO /2]
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    #Esperar 3 segundos
    time.sleep(5)
    #Salir
    sys.exit()
    
#Inicializamos la pantalla
pantalla = pygame.display.set_mode((ANCHO,ALTO))
#Le ponemos el título a la pantalla
pygame.display.set_caption('Breakout de los pibes')
#Creamos el reloj
reloj = pygame.time.Clock()
#Para poder dejar apretado
pygame.key.set_repeat(30)
#Creamos la pelota
pelota = Pelota()
#Creamos el jugador
jugador = Paleta()
#Creamos el muro
muro = Muro(50)
#Creamos sistema puntuacion
puntuacion = 0
vidas = 3
while True:
    #Establecemos FPS
    reloj.tick(60)
    #Revisamos todos los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit
    #Eventos del teclado
        elif evento.type == pygame.KEYDOWN:
            jugador.update(evento)
            
    #Actualizar la posición de la pelota
    pelota.update()
    #Colisión entre pelota y jugador
    if pygame.sprite.collide_rect(pelota, jugador):
        pelota.speed[1] = -pelota.speed[1]
    #Colisión entre pelota y muro
    lista = pygame.sprite.spritecollide(pelota, muro, False)
    if lista:
        ladrillo = lista[0]
        cx = pelota.rect.centerx
        sonido_pelota = mixer.Sound("sonidos/tennis.ogg")#Cargamos sonido entre colision de pelota y ladrillo
        sonido_pelota.play() #Reproducimos sonido
        if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
            pelota.speed[0] = -pelota.speed[0]
        else:
            pelota.speed[1] = -pelota.speed[1]
        muro.remove(ladrillo)
        puntuacion += 10
    #Si la pelota sale por abajo, perdés
    if pelota.rect.bottom >= ALTO:
        vidas -=1
    if puntuacion >= 500:
        ganar()
    #Rellenamos la pantalla con el fondo, para que no quede estela
    pantalla.fill(color_fondo)
    #Mostrar puntos
    puntos()
    #Mostrar vidas
    mostrar_vidas()
    #Dibujamos la pelota
    pantalla.blit(pelota.image, pelota.rect)
    #Dibujamos al jugador
    pantalla.blit(jugador.image, jugador.rect)
    #Dibujamos al muro
    muro.draw(pantalla)

        
    pygame.display.flip() #Lo usamos para redibujar la pantalla, que no se cierre 

    if vidas <= 0:
        juego_terminado()
