import arcade

SPRITE_SCALING = 1

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 10


class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class Brick(arcade.Sprite):

    def __init__(self,
                 filename: str=None,
                 brick_type: int=1,
                 hits: int=1,
                 scale: float=1,
                 image_x: float=0, image_y: float=0,
                 image_width: float=0, image_height: float=0,
                 center_x: float=0, center_y: float=0):
        super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y)
        self.brick_type = brick_type
        self.hits = hits

    """def update(self):
        if self.hits == 0:
            self.kill()
        if self.brick_type == 2 and self.hits == 1:
            self.filename = "images/brick_blue_cracked.png" """


class Ball(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):
        """ Constructor. """
        # Call the parent class (Sprite) constructor
        super().__init__(filename, sprite_scaling)

        # Instance variables that control the edges of where we bounce
        self.left_boundary = 0
        self.right_boundary = 0
        self.top_boundary = 0
        self.bottom_boundary = 0

        self.change_x = 0
        self.change_y = 0

    def update(self):

        # Move the ball
        self.center_x -= self.change_x
        self.center_y -= self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.center_x < self.left_boundary:
            self.change_x *= -1

        if self.center_x > self.right_boundary:
            self.change_x *= -1

        # if self.center_y < self.bottom_boundary:
        #   self.change_y *= -1

        if self.center_y > self.top_boundary:
            self.change_y *= -1


class BrickApplication(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.all_sprites_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.score_text = 0

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.brick_list = arcade.SpriteList()
        # Set up the player
        self.score = 0
        self.player_sprite = Player("images/paddle_02.png", SPRITE_SCALING)
        self.player_sprite.center_x = (SCREEN_WIDTH / 2)
        self.player_sprite.center_y = 40
        self.all_sprites_list.append(self.player_sprite)

        # Set up the ball
        self.ball_sprite = Ball("images/ballBlack_10.png", SPRITE_SCALING / 5)

        # Specify the boundaries for where a ball can be.
        # Take into account that we are specifying a center x and y for the
        # ball, and the ball has a size. So we can't have 0, 0 as the
        # position because 3/4 of the ball would be off-screen. We have to
        # start at half the width of the ball.
        self.ball_sprite.left_boundary = self.ball_sprite.width // 2
        self.ball_sprite.right_boundary = SCREEN_WIDTH - self.ball_sprite.width // 2
        self.ball_sprite.bottom_boundary = self.ball_sprite.height // 2
        self.ball_sprite.top_boundary = SCREEN_HEIGHT - self.ball_sprite.height // 2

        self.ball_sprite.center_x = (SCREEN_WIDTH / 2)
        self.ball_sprite.center_y = 70

        self.ball_sprite.change_x = 2
        self.ball_sprite.change_y = 2
        self.all_sprites_list.append(self.ball_sprite)

        # Set up the bricks
        gap = 0
        jgap = 0
        for j in range(4):
            for i in range(10):
                if j < 2:
                    hits = 1
                else:
                    hits = 2
                brick = Brick("images/brick_blue.png", 2, hits)
                brick.center_x = 50 + (i * brick.width) + gap
                brick.center_y = 399 + (j * brick.height) + jgap
                self.all_sprites_list.append(brick)
                self.brick_list.append(brick)
                gap += 1
            gap = 0
            jgap += 1

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.all_sprites_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"

        # Is this the same text as last frame? If not, set up a new text object
        if not self.score_text or output != self.score_text.text:
            self.score_text = arcade.create_text(output, arcade.color.BLACK, 14)
        # Render the text
        arcade.render_text(self.score_text, 0, 10)

    def update(self, delta_time):
        """ Movement and game logic """
        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.all_sprites_list.update()
        # change ball direction and speed on collision
        if arcade.check_for_collision(self.player_sprite, self.ball_sprite):
            self.ball_sprite.change_y *= -1
            self.ball_sprite.change_x -= (self.ball_sprite.position[0] - self.player_sprite.position[0]) / 10
        hit_list = arcade.check_for_collision_with_list(self.ball_sprite, self.brick_list)
        if hit_list:
            self.ball_sprite.change_y *= -1
        for brick in hit_list:
            brick.hits -= 1
            self.score += 1
            if brick.hits == 1:
                new_brick = Brick("images/brick_blue_cracked.png", 1, 1)
                new_brick.center_x = brick.center_x
                new_brick.center_y = brick.center_y
                self.all_sprites_list.append(new_brick)
                self.brick_list.append(new_brick)
                brick.kill()
            if brick.hits == 0:
                brick.kill()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """ Main method """
    window = BrickApplication(SCREEN_WIDTH, SCREEN_HEIGHT, "Brick")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
