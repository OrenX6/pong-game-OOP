import random
import sys

import pygame


class Block(pygame.sprite.Sprite):

    # a class to represent a Block object.

    def __init__(self, x_pos, y_pos, path):
        """
        Constructs all the necessary attributes for the Sprite object.

        :param x_pos (int): x position of Block object
        :param y_pos (int): y position of Block object
        :param path: image file path
        """
        super().__init__()

        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player(Block):
    # a class to represent a Player object.

    def __init__(self, x_pos, y_pos, path, speed):
        """

        :param x_pos (int): x position of Player object
        :param y_pos (int): y position of Player object
        :param path: image file path
        :param speed (int): the speed of the player.
        """
        super().__init__(x_pos, y_pos, path)  # call the init method with the required arguments
        self.speed = speed

    def screen_constrain(self):
        """
        constrain the player so that he doesn't get out of the screen
        """
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update(self, ball_group):
        """
         This method control sprite behavior.

        the update method doesn't use the ball_group argument, but we still have put it there, because
        when we call the update method, the paddle group is going to call the update method of every
        single sprite in the group. if we don't specify this parameter, it will cause an error.
        :param ball_group:
        """
        self.rect.centery += self.speed
        self.screen_constrain()


class Opponent(Block):
    # a class to represent a Opponent object.

    def __init__(self, x_pos, y_pos, path, speed):
        """

        :param x_pos (int): x position of Opponent object
        :param y_pos (int): y position of Opponent object
        :param path: image file path
        :param speed (int): the speed of the Opponent.
        """
        super().__init__(x_pos, y_pos, path)  # call the init method in Block class
        self.speed = speed

    def screen_constrain(self):
        """
        constrain the player so that he doesn't get out of the screen

        """
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def movement(self, ball_group):
        """
        the movement depends on the ball position in every single frame.
        when the ball under the opponent block, move the opponent downwards.
        when the ball above the opponent block, move the opponent upwards.

        :param ball_group:
        :return:
        """

        if self.rect.top < ball_group.sprite.rect.centery:  # access the sprite inside the group
            opponent.rect.centery += self.speed
        if opponent.rect.bottom > ball_group.sprite.rect.centery:
            opponent.rect.centery -= self.speed

    def update(self, ball_group):
        """
        This method control sprite behavior.

        :param ball_group:
        """
        self.movement(ball_group)
        self.screen_constrain()


class Ball(Block):
    # a class to represent a Ball object.

    def __init__(self, x_pos, y_pos, path, speed_x, speed_y, paddles):
        """

        :param x_pos (int): initial x position of the ball
        :param y_pos (int): initial y position of the ball
        :param path: image file path
        :param speed_x (int): horizontal speed of the ball.
        :param speed_y (int): vertical speed of the ball.
        :param paddles (Group):  Group object that contain the Sprite objects (paddles)
        """
        super().__init__(x_pos, y_pos, path)
        self.speed_x = speed_x * random.choice((1, -1))
        self.speed_y = speed_y * random.choice((1, -1))
        self.paddles = paddles  # the ball should know where the two paddles are, so he can collide with them
        self.score_time = 0  # check the time when the score was being achieved.
        self.active = True  # indicate if the ball move or not

    def movement(self):
        """
        move the ball on the screen.

        """
        self.rect.centerx += self.speed_x  # int
        self.rect.centery += self.speed_y

    def collisions(self):
        """
        Check if the ball collide with the paddles or with the screen limits.
        if it is, change the direction of the ball.
        """
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:  # vertical
            pong_sound.play()
            self.speed_y *= -1

        # ball hits the player's paddle or opponent's paddle.
        if pygame.sprite.spritecollide(self, self.paddles, False):  # return an empty list or list with paddle
            pong_sound.play()
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0]  # Sprite object
            if abs(self.rect.right - collision_paddle.rect.left) < 10 and self.speed_x > 0:  # player's paddle.
                self.speed_x *= -1
            elif abs(self.rect.left - collision_paddle.rect.right) < 10 and self.speed_x < 0:  # opponent's paddle
                self.speed_x *= -1
            elif abs(self.rect.bottom - collision_paddle.rect.top) < 10 and self.speed_y > 0:  # ball hits upwards
                self.rect.bottom = collision_paddle.rect.top
                self.speed_y *= -1
            elif abs(self.rect.top - collision_paddle.rect.bottom) < 10 and self.speed_y < 0:  # ball hits downwards
                self.rect.top = collision_paddle.rect.bottom
                self.speed_y *= -1

    def reset_ball(self):
        """
        puts the ball in the middle of the screen and set new random direction
        """
        self.rect.center = root.get_rect().center
        self.speed_x *= random.choice((1, -1))
        self.speed_y *= random.choice((1, -1))

    def update(self):
        if self.active:
            self.movement()
            self.collisions()
        else:
            self.reset_ball()


class GameManager:
    # a class to represent a GameManager object.

    """
    manage the game and the game's logic.
    make the actual game, by using Block,Player,Ball,Opponent classes all together
    """

    def __init__(self, ball_group, paddle_group):
        """

        :param ball_group: GroupSingle object that contain the ball.
        :param paddle_group: Group object that contain the paddles.
        """
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.player_score = 0  # default value
        self.opponent_score = 0  # default value
        self.score_time = None  # check the time when the score was being achieved.

    def check_score(self):
        """
        when the ball scores, we play the right sound, reset the ball and count time.
        We update the scoreboard too, by adding the scores.
        """
        ball_object = self.ball_group.sprite

        if ball_object.rect.right >= SCREEN_WIDTH or ball_object.rect.left <= 0:
            score_sound.play()
            self.score_time = pygame.time.get_ticks()  # int
            ball_object.active = False

            if ball_object.rect.left <= 0:
                self.player_score += 1
            elif ball_object.rect.right >= SCREEN_WIDTH:
                self.opponent_score += 1

            ball_object.reset_ball()

    def draw_score(self):
        """
        draw the score on the screen, in every single frame
        """
        player_text_surf = font_object.render(f"{self.player_score}", True, accent_color)
        opponent_text_surf = font_object.render(f"{self.opponent_score}", True, accent_color)

        root.blit(player_text_surf, (660, 470))
        root.blit(opponent_text_surf, (610, 470))

    def draw_counter(self):
        """
        draws the counter on the screen, when the ball is not active.
        """
        current_time = pygame.time.get_ticks()  # current time (int)
        if current_time - self.score_time < 3000:  # three seconds break

            timer = round((current_time - self.score_time) * 0.001, 0)

            if timer == 0.0:
                num = 3
            elif timer == 1.0:
                num = 2
            elif timer == 2.0:
                num = 1
            else:
                num = 0
                self.ball_group.sprite.active = True
                self.score_time = None

            timer_surf = font_object.render(f"{num}", False, accent_color)  # text Surface object
            timer_rect = timer_surf.get_rect(center=(SCREEN_WIDTH / 2 - 10, SCREEN_HEIGHT / 2 + 40))
            root.blit(timer_surf, timer_rect)

    def run_game_logic(self):
        """
        run the game
        """

        self.paddle_group.draw(root)  # blit the Sprite images
        self.ball_group.draw(root)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.check_score()

        if self.score_time:
            self.draw_counter()

        self.draw_score()


# main:

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

# General setup:
pygame.mixer.pre_init()
pygame.init()
clock = pygame.time.Clock()  # Clock object

# setting up the main window:
root = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))  # display Surface object
pygame.display.set_caption("Pong")

# Static Global variables:
middle_line = pygame.Rect(SCREEN_WIDTH / 2, 0, 4, SCREEN_HEIGHT)
bg_color = pygame.Color("#a6b6c3")
accent_color = (27, 35, 43)
font_object = pygame.font.SysFont("Ariel.ttf", 32)
pong_sound = pygame.mixer.Sound(file="pong.ogg")  # Sound object
score_sound = pygame.mixer.Sound(file="score.ogg")

# Game objects and Groups:
player = Player(SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2 - 70, "Paddle.png", 0)
opponent = Opponent(20, SCREEN_HEIGHT / 2 - 70, "Paddle.png", 25)
paddle_group = pygame.sprite.Group(player, opponent)

ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "Ball.png", 6, 6, paddle_group)
ball_sprite = pygame.sprite.GroupSingle(ball)

game_manager = GameManager(ball_sprite, paddle_group)

while True:

    # Handling user inputs:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # uninitialized the pygame module
            sys.exit()  # closes the entire program

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.speed -= 15
            if event.key == pygame.K_DOWN:
                player.speed += 15
        if event.type == pygame.KEYUP:  # paddle speed become zero again
            if event.key == pygame.K_UP:
                player.speed += 15
            if event.key == pygame.K_DOWN:
                player.speed -= 15

    # static visuals:
    root.fill(bg_color)
    pygame.draw.rect(root, accent_color, middle_line)

    # Run the game
    game_manager.run_game_logic()

    # Rendering
    pygame.display.flip()
    clock.tick(120)
