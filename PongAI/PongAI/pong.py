# https://pl.wikipedia.org/wiki/Pong
# Patrycja Bednarska i Maciej Dzieciuch
# Uruchomienie gry odbywa się za pomocą pong.py
# Należy zainstalować paczkę pygame oraz Python ver. 3.8

import sys
from random import choice

import pygame as pg

SCREEN_RECT = pg.Rect(0, 0, 800, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 120)

################ USTAWIENIA ################
BORDER_COLOR = WHITE
PADDLE_COLOR = PINK
BALL_COLOR = WHITE

PADDLE_SPEED = 10
BALL_SPEED = 5
############################################

BORDER_WIDTH = 10
BORDER_TOP = 50
BORDER_BOTTOM = SCREEN_RECT.bottom - 50
MAX_TOP = BORDER_TOP + BORDER_WIDTH / 2 + 1
MAX_BOT = BORDER_BOTTOM - BORDER_WIDTH / 2

screen = None


class Ball:
    """Klasa definiująca piłkę

    Atrybuty:
        init_xy (tuple): Przechowuje krotke zawierającą inicjalną pozycję piłki
        pos (Rect): Przechowuje obiekt Rect z biblioteki definijąca pozycję i wielkość piłki
        speedX (int): Przechowuje prędkość piłki po osi X
        speedY (int): Przechowuje prędkość piłki po osi Y
    """

    D = 20

    def __init__(self, x, y):
        self.init_xy = (x, y)
        self.pos = pg.Rect(x, y, self.D, self.D)
        self.speedX = BALL_SPEED * choice([-1, 1])
        self.speedY = BALL_SPEED * choice([-1, 1])

    def init(self):
        self.__init__(*self.init_xy)

    def update(self, players):
        """Metoda aktualizująca położenie piłeczki

        Parametry wejściowe:
            players (Dict): Słownik zawierający dwóch graczy czyli lewą i prawą paletkę
        """
        self.pos.x += self.speedX
        self.pos.y += self.speedY

        if self.pos.top <= MAX_TOP:
            self.speedY *= -1

        elif self.pos.bottom >= MAX_BOT:
            self.speedY *= -1

        offset = 50
        if self.pos.right < -offset:
            self.init()
            players['right'].score += 1
        elif self.pos.left > SCREEN_RECT.width + offset:
            self.init()
            players['left'].score += 1

        for paddle in (players['left'].paddle, players['right'].paddle):
            if self.pos.colliderect(paddle.pos):
                self.speedX *= -1
                self.speedY += paddle.speed / 2
                if self.speedX < 0:
                    self.pos.right = paddle.pos.left
                elif self.speedY > 0:
                    self.pos.left = paddle.pos.right

    def show(self):
        """Metoda rysująca piłeczkę na ekranie"""
        pg.draw.circle(screen, BALL_COLOR, self.pos.center, self.pos.width // 2)


class Paddle:
    """Klasa definiująca paletkę

    Atrybuty:
        pos (Rect): Przechowuje obiekt Rect z biblioteki definijąca pozycję i wielkość piłki
        pos.center (Tuple): Przechowuje krotkę dotyczącą współrzędnych paletki
        speed (int): Przechowuje prędkość paletki
    """

    WIDTH, HEIGHT = 20, 150

    def __init__(self, x, y):
        self.pos = pg.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.pos.center = (x, y)
        self.speed = 0

    def update(self, direction):
        """Metoda aktualizująca położenie paletki

        Parametry wejściowe:
            direction (int): Pole definiujące kierunek w który zmierza paletka (góra/dół)
        """
        self.speed = direction * PADDLE_SPEED
        self.pos.y += self.speed

        if self.pos.top <= MAX_TOP:
            self.pos.top = MAX_TOP
        elif self.pos.bottom >= MAX_BOT:
            self.pos.bottom = MAX_BOT

    def update_ai(self, ball_pos):
        """Metoda aktualizująca położenie paletki dla komputera

        Parametry wejściowe:
            ball_pos (int): Pole definiujące prędkość piłeczki
        """
        if ball_pos <= 295:
            self.speed = -1 * PADDLE_SPEED
        elif ball_pos > 295:
            self.speed = 1 * PADDLE_SPEED

        self.pos.y += self.speed

        if self.pos.top <= MAX_TOP:
            self.pos.top = MAX_TOP
        elif self.pos.bottom >= MAX_BOT:
            self.pos.bottom = MAX_BOT

    def show(self):
        """Metoda rysująca paletkę na ekranie"""
        pg.draw.rect(screen, PADDLE_COLOR, self.pos, 0)


class Player:
    """Klasa definiująca instancję gracza

    Atrybuty:
        score (int): Przechowuje liczbę punktów dla gracza
        paddle (Paddle): Obiekt paletki
    """

    def __init__(self, x, y):
        self.score = 0
        self.paddle = Paddle(x, y)

    def show(self):
        """Metoda wykonująca drugą metodę z obiektu paddle rysującą paletkę dla gracza"""
        self.paddle.show()


class AiPlayer(Player):
    """Klasa definiująca gracza komputerowego

    Atrybuty:
        x, y (int): Przechowuje inicjalne współrzędne dla paletki
    """

    def __init__(self, x, y):
        super().__init__(x, y)

    def update_ai(self, ball_pos):
        """Metoda wykonująca metodę aktualizacji położenia paletki

        Parametry wejściowe:
            ball_pos (int): Przechowuje aktualne położenie piłeczki
        """
        self.paddle.update_ai(ball_pos)


class HumanPlayer(Player):
    """Klasa definiująca gracza ludzkiego

    Atrybuty:
        x, y (int): Przechowuje inicjalne współrzędne dla paletki
        up_key (int): Przechowuje znak przycisku z tabeli ASCII (strzałka w górę)
        up_down (int): Przechowuje znak przycisku z tabeli ASCII (strzałka w dół)
    """

    def __init__(self, x, y, up_key, down_key):
        super().__init__(x, y)
        self.up_key = up_key
        self.down_key = down_key

    def update(self, keys):
        """Metoda wykonująca metodę aktualizacji położenia paletki

        Parametry wejściowe:
            keys (Sequence): Przechowuje odczytane przyciski naciśnięte z klawiatury
        """
        direction = 0
        if keys[self.up_key]:
            direction = -1
        elif keys[self.down_key]:
            direction = 1

        self.paddle.update(direction)


def leave():
    """Metoda opisuje proces wyjścia z gry"""
    pg.quit()
    sys.exit(0)


def drawBorder(y):
    """Metoda rysująca okno gry

    Parametry wejściowe:
        y (int): Przechowuje wartości dotyczące obramowania okna gry
    """
    pg.draw.line(screen, BORDER_COLOR, (0, y), (SCREEN_RECT.width, y), BORDER_WIDTH)


def drawScore(players):
    """Metoda rysująca wyniki

    Parametry wejściowe:
        players (Dict): Słownik zawierający dwóch graczy czyli lewą i prawą paletkę
    """
    leftScore = players['left'].score
    rightScore = players['right'].score

    font = pg.font.SysFont("Calibri", 50)
    text = font.render("{} : {} ".format(leftScore, rightScore), 1, WHITE)
    rect = text.get_rect()
    rect.centerx = SCREEN_RECT.centerx
    rect.centery = (BORDER_TOP - BORDER_WIDTH / 2) / 2
    screen.blit(text, (rect.x, rect.y))


def main():
    """Główna metoda w której użyte są wszystkie klasy i metody potrzebne do poprawnego działania gry"""
    global BORDER_TOP
    global BORDER_BOTTOM
    global screen

    pg.init()
    screen = pg.display.set_mode(SCREEN_RECT.size)
    clock = pg.time.Clock()

    ball = Ball(SCREEN_RECT.centerx, SCREEN_RECT.centery)
    left = AiPlayer(50, SCREEN_RECT.centery)
    right = HumanPlayer(SCREEN_RECT.width - 50, SCREEN_RECT.centery, pg.K_UP, pg.K_DOWN)

    players = {'left': left, 'right': right}

    while True:
        screen.fill(BLACK)

        keys = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                leave()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    players['left'].score = 0
                    players['right'].score = 0
                    ball.init()

        drawBorder(BORDER_TOP)
        drawBorder(BORDER_BOTTOM)
        drawScore(players)

        ball.update(players)
        left.update_ai(ball.pos.y)
        right.update(keys)

        ball.show()
        left.show()
        right.show()

        pg.display.flip()
        pg.display.set_caption("fps: " + str(clock.get_fps()))
        clock.tick(60)


if __name__ == '__main__':
    main()
