from kivy.app import App
# blank canvas
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

"""
Ways to react to touch in Kivy:
--->on_touch_down()--when we touch the screen via mouse or fingers(touch screen)
--->on_touch_up()----when we lift our fingeror mouse after touching
--->on_touch_move()--when we drag finger or mouse
"""


class PongPaddle(Widget):
    score = NumericProperty(0)
    # creating method to detect ball or collision detection

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self):
        y_pos = randint(0, 360)
        # remove comment to check Y_pos
        # print(y_pos)
        self.ball.velocity = Vector(4, 0).rotate(y_pos)

    def update(self, dt):
        # writing all movement func of ball
        self.ball.move()

        # Ball Bounce function
        # bounce vertical
        if (self.ball.y < 0) or (self.ball.y > self.height-50):
            self.ball.velocity_y *= -1
        # bounce horizontal along with score up
        # left
        if (self.ball.x < 0):
            self.ball.velocity_x *= -1
            self.player2.score += 1

        # right
        if (self.ball.x > self.width-50):
            self.ball.velocity_x *= -1
            self.player1.score += 1

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    def on_touch_move(self, touch):
        # touch area for player 1 on left
        if touch.x < self.width/4:
            self.player1.center_y = touch.y
        # touch area for player2 on right
        if touch.x > self.width*(3/4):
            self.player2.center_y = touch.y


# pong ball class
class PongBall(Widget):
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    # Using numeric property as Kivy is used for multiplatform
    # and Java doesn't automatically understand the var type

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

# inheriting from App class


class PongApp(App):

    # build method inherits from itself
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
    # PongApp inherits run() method from App class
