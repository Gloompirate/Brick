import arcade

# Setup the constants that will be used
SPRITE_SCALING = 1
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 10
START_MENU = 0
GAME_RUNNING = 1
GAME_PAUSE = 2
GAME_OVER = 3
BALL_LOCKED = True


class Player(arcade.Sprite):

    def update(self):
        """
        Update the player variables.
        """
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Make sure the player cannot move out of the screen area.
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class Brick(arcade.Sprite):

    def __init__(self, filename: str=None, brick_type: int=1, hits: int=1, scale: float=1, image_x: float=0, image_y: float=0,
                 image_width: float=0, image_height: float=0, center_x: float=0, center_y: float=0):
        """Create a new Brick, extends the arcade.Sprite class.
        Attributes:
            brick_type (int): The type of brick.
            hits (int): The number of times the brick must be hit before it is destroyed.
        """
        # Call the parent class (Sprite) constructor.
        super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y)
        self.brick_type = brick_type
        self.hits = hits


class Ball(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):
        """ Constructor. """
        # Call the parent class (Sprite) constructor.
        super().__init__(filename, sprite_scaling)

        # Instance variables that control the edges of where the Ball will bounce.
        self.left_boundary = 0
        self.right_boundary = 0
        self.top_boundary = 0
        self.bottom_boundary = 0

        # Instance variables that control the rate of acceleration of the Ball.
        self.change_x = 0
        self.change_y = 0

    def update(self):
        """Updates the position of the Ball. """
        # Move the ball
        self.center_x -= self.change_x
        self.center_y -= self.change_y

        # If we are out-of-bounds, then 'bounce' by changing reversing the direction in which the Ball is accelerating.
        if self.center_x < self.left_boundary:
            self.change_x *= -1
        if self.center_x > self.right_boundary:
            self.change_x *= -1
        if self.center_y > self.top_boundary:
            self.change_y *= -1
        # un-comment to bounce off the bottom.
        # if self.center_y < self.bottom_boundary:
        #     self.change_y *= -1


class BrickApplication(arcade.Window):
    """
    Main application class, extends arcade.Window class.
    """

    def __init__(self, width, height, title):
        """
        Initialiser
        """

        # Call the parent class initialiser.
        super().__init__(width, height, title)

        # Variables that will hold the sprite lists.
        self.all_sprites_list = None

        # Set up the player info
        self.player_sprite = None

        # Set the background colour.
        arcade.set_background_color(arcade.color.WHITE)

        # Set the current game state.
        self.current_state = GAME_RUNNING
        self.ball_locked = BALL_LOCKED

    def setup(self):
        """ Set up the game and initialise the variables. """

        # Create Sprite Lists to hold the sprites.
        self.all_sprites_list = arcade.SpriteList()
        self.brick_list = arcade.SpriteList()

        # Set up the game.
        self.score = 0
        self.lives = 3
        self.lives_text = arcade.create_text("Lives: 0", arcade.color.WHITE, 14)
        self.score_text = arcade.create_text("Score: 0", arcade.color.WHITE, 14)
        # Load the background image, do it here so it isn't loaded more than once.
        self.background = arcade.load_texture("images/background2.jpg")

        # Set up the Player.
        self.player_sprite = Player("images/paddle_02.png", SPRITE_SCALING)
        self.player_sprite.center_x = (SCREEN_WIDTH / 2)
        self.player_sprite.center_y = 40
        self.all_sprites_list.append(self.player_sprite)

        # Set up the Ball.
        self.ball_sprite = Ball("images/ballBlack_10.png", SPRITE_SCALING / 5)

        # Specify the boundaries for where the Ball can be.
        # Take into account that we are specifying a center x and y for the
        # Ball, and the Ball has a size. So we can't have 0, 0 as the
        # position because 3/4 of the Ball would be off-screen. We have to
        # start at half the width of the Ball.
        self.ball_sprite.left_boundary = self.ball_sprite.width // 2
        self.ball_sprite.right_boundary = SCREEN_WIDTH - self.ball_sprite.width // 2
        self.ball_sprite.bottom_boundary = self.ball_sprite.height // 2
        self.ball_sprite.top_boundary = SCREEN_HEIGHT - self.ball_sprite.height // 2
        # Put the ball in the starting position
        self.ball_sprite.center_x = (SCREEN_WIDTH / 2)
        self.ball_sprite.center_y = 59
        # Set the initial acceleration rate of the Ball
        self.ball_sprite.change_x = 0
        self.ball_sprite.change_y = 0
        # Add the Ball to the Sprite List.
        self.all_sprites_list.append(self.ball_sprite)

        # Set up the bricks in a test pattern.
        # This will be replaced by a function to read a level from a data source
        # 4 rows of 10 bricks, top two rows take 2 hits
        """
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
        # 15 rows of 1 brick
        """
        """
        jgap = 0
        for j in range(1, 22):
            brick = Brick("images/brick_blue.png", 2, 1)
            brick.center_x = 0 + brick.width / 2
            brick.center_y = 0 + (j * brick.height) + jgap
            self.all_sprites_list.append(brick)
            self.brick_list.append(brick)
            jgap += 1
        """
        map1 = [[[1, 1] for i in range(10)] for j in range(10)]
        map1[5][5] = [0, 0]
        gap = 0
        igap = 0
        for i in range(len(map1)):
            for j in range(len(map1[0])):
                if map1[i][j][0]:
                    brick = Brick("images/brick_blue.png", map1[i][j][1], 1)
                brick.left = (j * brick.width) + gap
                brick.top = SCREEN_HEIGHT - (i * brick.height) - igap
                self.all_sprites_list.append(brick)
                self.brick_list.append(brick)
                gap += 3
            gap = 0
            igap += 3

    def draw_game_over(self):
            """
            Draw "Game over" across the screen.
            """
            output = "Game Over"
            arcade.draw_text(output, 100, 400, arcade.color.WHITE, 54)
            output = "Press Space to restart"
            arcade.draw_text(output, 100, 300, arcade.color.WHITE, 24)

    def draw_game_pause(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Game Paused"
        arcade.draw_text(output, 100, 400, arcade.color.WHITE, 54)
        output = "Press Escape to restart"
        arcade.draw_text(output, 100, 300, arcade.color.WHITE, 24)

    def draw_game(self):

        # Draw the background first.
        # Draw the background texture
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        # Draw all the sprites.
        self.all_sprites_list.draw()

        # Generate the text Strings.
        score_output = f"Score: {self.score}"
        lives_output = f"Lives: {self.lives}"

        # Is this the same text as last frame? If not, set up a new text object
        if score_output != self.score_text.text:
            self.score_text = arcade.create_text(score_output, arcade.color.WHITE, 14)
        if lives_output != self.lives_text.text:
            self.lives_text = arcade.create_text(lives_output, arcade.color.WHITE, 14)
        # Render the text
        arcade.render_text(self.score_text, 0, 10)
        arcade.render_text(self.lives_text, 500, 10)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before drawing anything to the screen.
        arcade.start_render()

        # Check what we need to draw based on what state the game is in.
        if self.current_state == GAME_RUNNING:
            self.draw_game()
        elif self.current_state == GAME_PAUSE:
            self.draw_game()
            self.draw_game_pause()  # Draw both screens so that the pause screen acts as an overlay.
        elif self.current_state == GAME_OVER:
            self.draw_game()
            self.draw_game_over()  # Draw both screen so the game over message acts as an overlay.

    def update(self, delta_time):
        """ Movement and game logic """
        # If the game is started and not currently paused or game over.
        if self.current_state == GAME_RUNNING:

            # Call update on all sprites
            self.all_sprites_list.update()

            # If the ball is locked to the paddle set the ball acceleration equal to the paddle acceleration,
            # also set the ball position to the same as the paddle
            if self.ball_locked:
                self.ball_sprite.change_x = -self.player_sprite.change_x
                self.ball_sprite.change_y = -self.player_sprite.change_y
                self.ball_sprite.center_x = self.player_sprite.center_x
            # Change the Ball direction and speed on collision with the paddle
            elif arcade.check_for_collision(self.player_sprite, self.ball_sprite):
                self.ball_sprite.change_y *= -1
                self.ball_sprite.change_x -= (self.ball_sprite.position[0] - self.player_sprite.position[0]) / 10

            # Make a list of any bricks that the Ball collided with.
            hit_list = arcade.check_for_collision_with_list(self.ball_sprite, self.brick_list)
            if hit_list:
                # See where the ball hit the brick
                if abs(self.ball_sprite.position[1] - hit_list[0].top) < 3 or abs(self.ball_sprite.position[1] - hit_list[0].bottom) < 3:
                    print("Hit top or bottom")
                    self.ball_sprite.change_y *= -1
                elif abs(self.ball_sprite.position[0] - hit_list[0].right) < 6 or abs(self.ball_sprite.position[0] - hit_list[0].left) < 6:
                        print("Hit side")
                        self.ball_sprite.change_x *= -1
                else:
                    print("Hit top or bottom")
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

            # Check to see if the ball has left the game area.
            # If it has reduce the number of lives by one and either reposition the Ball
            # if the player has lives left, or its game over.
            if self.ball_sprite.center_y < 0:
                self.lives -= 1
                self.ball_sprite.center_x = self.player_sprite.center_x
                self.ball_sprite.center_y = 59
                self.ball_sprite.change_x = 0
                self.ball_sprite.change_y = 0
                self.ball_locked = True
                if self.lives == 0:
                    self.ball_sprite.kill()
                    self.current_state = GAME_OVER

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        # Check the game has started, and isn't paused or finished before
        # updating the values. Escape can be used to pause the game here.
        if self.current_state == GAME_RUNNING:
            if key == arcade.key.LEFT:
                self.player_sprite.change_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = MOVEMENT_SPEED
            elif key == arcade.key.ESCAPE:
                self.current_state = GAME_PAUSE
            elif key == arcade.key.SPACE:
                if self.ball_locked:
                    self.ball_locked = False
                    self.ball_sprite.change_y = (MOVEMENT_SPEED / 5)
            """ UP and DOWN are not currently used.
            elif key == arcade.key.UP:
                self.player_sprite.change_y = MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -MOVEMENT_SPEED
            """
        elif self.current_state == GAME_PAUSE:
            if key == arcade.key.ESCAPE:
                self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER:
            if key == arcade.key.SPACE:
                self.current_state = GAME_RUNNING
                self.setup()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        # Check the game has started, and isn't paused or finished before
        # updating the values.
        if self.current_state == GAME_RUNNING:
            if key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.player_sprite.change_x = 0
            """ UP and DOWN are not currently used
            elif key == arcade.key.UP or key == arcade.key.DOWN:
                self.player_sprite.change_y = 0
            """


def main():
    """ Main method """
    window = BrickApplication(SCREEN_WIDTH, SCREEN_HEIGHT, "Brick")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
