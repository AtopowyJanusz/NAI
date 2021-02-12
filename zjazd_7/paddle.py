"""
Autorzy: Maciej Dzieciuch, Patrycja Bednarka
Uruchomienie: python3 main.py

Opis:
Gra jest prostą grą w paletkę i piłkę. Gdzie mamy paletkę na ziemi i paletka musi uderzyć w poruszającą się piłkę.
Jeśli piłka dotknie ziemi zamiast paletki, to zostaje naliczony naliczony punkt jako uchybienie.
"""
import turtle as t


class Paddle:

    def __init__(self):

        self.done = False
        self.reward = 0
        self.hit, self.miss = 0, 0

        """Ustawienie tła"""

        self.win = t.Screen()
        self.win.title('Paddle')
        self.win.bgcolor('black')
        self.win.setup(width=600, height=600)
        self.win.tracer(0)

        """Utawienie paletki"""

        self.paddle = t.Turtle()
        self.paddle.speed(0)
        self.paddle.shape('square')
        self.paddle.shapesize(stretch_wid=1, stretch_len=5)
        self.paddle.color('white')
        self.paddle.penup()
        self.paddle.goto(0, -275)

        """Ustawienie piłki"""

        self.ball = t.Turtle()
        self.ball.speed(0)
        self.ball.shape('circle')
        self.ball.color('red')
        self.ball.penup()
        self.ball.goto(0, 100)
        self.ball.dx = 3
        self.ball.dy = -3

        """Ustawienie punktacji"""

        self.score = t.Turtle()
        self.score.speed(0)
        self.score.color('white')
        self.score.penup()
        self.score.hideturtle()
        self.score.goto(0, 250)
        self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center',
                         font=('Courier', 24, 'normal'))

        """Konfiguracja klawiszy z klawiatury"""

        self.win.listen()
        self.win.onkey(self.paddle_right, 'Right')
        self.win.onkey(self.paddle_left, 'Left')

    """Ustawienia dotyczące poruszania się paletki"""

    def paddle_right(self):

        x = self.paddle.xcor()
        if x < 225:
            self.paddle.setx(x + 20)

    def paddle_left(self):

        x = self.paddle.xcor()
        if x > -225:
            self.paddle.setx(x - 20)

    def run_frame(self):

        self.win.update()

        """Ustawienia dotyczące poruszania się piłki"""

        self.ball.setx(self.ball.xcor() + self.ball.dx)
        self.ball.sety(self.ball.ycor() + self.ball.dy)

        """Ustawienia piłki i momentu kiedy dotknie ziemi lub paletki"""

        if self.ball.xcor() > 290:
            self.ball.setx(290)
            self.ball.dx *= -1

        if self.ball.xcor() < -290:
            self.ball.setx(-290)
            self.ball.dx *= -1

        if self.ball.ycor() > 290:
            self.ball.sety(290)
            self.ball.dy *= -1

        """Ustawienia dotyczące kontaktu z ziemią"""

        if self.ball.ycor() < -290:
            self.ball.goto(0, 100)
            self.miss += 1
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center',
                             font=('Courier', 24, 'normal'))
            self.reward -= 3
            self.done = True

        """Ustawienia dotyczące kontaktu z paletką"""

        if abs(self.ball.ycor() + 250) < 2 and abs(self.paddle.xcor() - self.ball.xcor()) < 55:
            self.ball.dy *= -1
            self.hit += 1
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center',
                             font=('Courier', 24, 'normal'))
            self.reward += 3

    def reset(self):

        self.paddle.goto(0, -275)
        self.ball.goto(0, 100)
        return [self.paddle.xcor() * 0.01, self.ball.xcor() * 0.01, self.ball.ycor() * 0.01, self.ball.dx, self.ball.dy]

    """
    Funkcja służąca do wysyłania konkretnych akcji jakie ma wykonać paletka czyli ruch w lewo lub prawo
    """

    def step(self, action):

        self.reward = 0
        self.done = 0

        if action == 0:
            self.paddle_left()
            self.reward -= .1

        if action == 2:
            self.paddle_right()
            self.reward -= .1

        self.run_frame()

        state = [self.paddle.xcor() * 0.01, self.ball.xcor() * 0.01, self.ball.ycor() * 0.01, self.ball.dx,
                 self.ball.dy]
        return self.reward, state, self.done
