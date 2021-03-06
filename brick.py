"""
TODO:
    Sort out physics of hitting the side of the bricks, <------ this!!!!!!!!!!!!!!
    Add some randomness when the ball hits the centre of the paddle
    Title / reset screens
    Powerup bricks
    Powerups
    More Levels
    Sounds?
"""

import arcade
import random

# Setup the constants that will be used
SPRITE_SCALING = 1
BRICK_SCALING = 1.5
BALL_SCALING = 1.3
SCREEN_WIDTH = 610
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 10
START_MENU = 0
GAME_RUNNING = 1
GAME_PAUSE = 2
GAME_OVER = 3
BALL_LOCKED = True
BRICK_GAP_HORIZONTAL = 3
BRICK_GAP_VERTICAL = 3

# Bricks, in format ["Image path", Number of hits, next brick once destroyed, special ability]
# This is just a prototype, will need to change this to add special bick types
BRICK_TYPES = {
    0: ["", 0, 0, 0],
    1: ["images/bricks/blue.png", 1, 0, 0],
    2: ["images/bricks/red.png", 1, 1, 0],
    3: ["images/bricks/green.png", 1, 2, 0],
    4: ["images/bricks/purple.png", 1, 3, 0],
    5: ["images/bricks/black_red.png", 1, 0, 1]
}


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

    def __init__(self, brick_type: int=1, scale: float=1, image_x: float=0, image_y: float=0,
                 image_width: float=0, image_height: float=0, center_x: float=0, center_y: float=0):
        """Create a new Brick, extends the arcade.Sprite class.
        Attributes:
            brick_type (int): The type of brick.
            hits (int): The number of times the brick must be hit before it is destroyed.
        """
        filename = BRICK_TYPES[brick_type][0]
        # Call the parent class (Sprite) constructor.
        super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y)
        self.brick_type = brick_type
        self.hits = BRICK_TYPES[brick_type][1]
        self.special = BRICK_TYPES[brick_type][3]


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
        self.effect_list = arcade.SpriteList()

        # Set up the game.
        self.score = 0
        self.lives = 3
        self.lives_text = arcade.create_text("Lives: 0", arcade.color.WHITE, 14)
        self.score_text = arcade.create_text("Score: 0", arcade.color.WHITE, 14)
        # Load the background image, do it here so it isn't loaded more than once.
        self.background = arcade.load_texture("images/backgrounds/background2.jpg")

        # Set up the Player.
        self.player_sprite = Player("images/paddles/red.png", SPRITE_SCALING)
        self.player_sprite.center_x = (SCREEN_WIDTH // 2)
        self.player_sprite.center_y = 40
        self.all_sprites_list.append(self.player_sprite)

        # Set up the Ball.
        self.ball_sprite = Ball("images/balls/red.png", BALL_SCALING)

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
        self.ball_sprite.center_x = (SCREEN_WIDTH // 2)
        self.ball_sprite.bottom = self.player_sprite.top + 1
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
        random_bricks = [0] * 9 + [1] * 20 + [2] * 10 + [3] * 8 + [4] * 5 + [5] * 30
        # random_bricks = [1]
        map1 = [[random.choice(random_bricks) for i in range(12)] for j in range(12)]
        map1[5][5] = 2
        gap = 0
        igap = 0
        for i in range(len(map1)):
            for j in range(len(map1[0])):
                if map1[i][j]:
                    brick = Brick(map1[i][j], BRICK_SCALING)
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

            # Show first effect
            if len(self.effect_list):
                self.all_sprites_list.append(self.effect_list[0])
                self.effect_list.pop()

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
                # Make sure the ball wont just bounce up and down in the centre of the paddle.
                speed_change = (self.ball_sprite.position[0] - self.player_sprite.position[0])
                if speed_change == 0:
                    self.ball_sprite.change_x -= random.uniform(-0.5, 0.5)
                else:
                    self.ball_sprite.change_x -= speed_change / 10

            # Make a list of any bricks that the Ball collided with.
            hit_list = arcade.check_for_collision_with_list(self.ball_sprite, self.brick_list)
            # Check each brick that was hit.
            x_change_count = 0
            y_change_count = 0
            for brick in hit_list:
                # See where the ball hit the brick
                if self.side_collision(self.ball_sprite, brick):
                    if self.ball_sprite.change_x == 0:
                        x_change_count += 1
                    else:
                        x_change_count += 1
                else:
                    y_change_count += 1
                # Check the Brick that was hit and remove it and replace it with the next brick,
                # or just remove it if it has been destroyed.
                brick.hits -= 1
                self.score += 1
                if brick.hits == 0:
                    # Check if we are making a new brick.
                    if BRICK_TYPES[brick.brick_type][2]:
                        new_brick = Brick(BRICK_TYPES[brick.brick_type][2], BRICK_SCALING)
                        new_brick.center_x = brick.center_x
                        new_brick.center_y = brick.center_y
                        self.all_sprites_list.append(new_brick)
                        self.brick_list.append(new_brick)
                        brick.kill()
                    else:
                        brick.kill()
                    # Code to do special abilities here.
                    if brick.special:
                        if brick.special == 1:  # explode cardinal bricks
                            matches = self.find_bricks_cardinal(brick)
                            for match in matches:
                                if match.special:
                                    more_bricks = self.find_bricks_cardinal(match)
                                    for more in more_bricks:
                                        if more not in matches:
                                            matches.append(more)
                                fire_effect = arcade.Sprite("images/effects/fire_centre.png", BRICK_SCALING)
                                fire_effect.center_x = match.center_x
                                fire_effect.center_y = match.center_y
                                # self.all_sprites_list.append(fire_effect)
                                self.effect_list.append(fire_effect)
                                match.kill()
                                self.score += 1
                        fire_effect = arcade.Sprite("images/effects/fire_centre.png", BRICK_SCALING)
                        fire_effect.center_x = brick.center_x
                        fire_effect.center_y = brick.center_y
                        # self.all_sprites_list.append(fire_effect)
                        self.effect_list.append(fire_effect)
                        brick.kill()
            # If the ball hit something figure out which way to make it bounce.
            if hit_list:
                if x_change_count >= y_change_count:
                    self.ball_sprite.change_x *= -1
                else:
                    self.ball_sprite.change_y *= -1
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

    def find_bricks_row_left(self, brick):
        return [x for x in self.brick_list if (x.center_x - brick.width - BRICK_GAP_HORIZONTAL) <= brick.center_x >= (x.center_x + brick.width + BRICK_GAP_HORIZONTAL) and x.center_y == brick.center_y]

    def find_bricks_adjacent(self, brick):
        return [x for x in self.brick_list if (x.center_x - brick.width - BRICK_GAP_HORIZONTAL) <= brick.center_x <= (x.center_x + brick.width + BRICK_GAP_HORIZONTAL) and x.center_y == brick.center_y]

    def find_bricks_stacked(self, brick):
        return [x for x in self.brick_list if (x.center_y - brick.height - BRICK_GAP_VERTICAL) <= brick.center_y <= (x.center_y + brick.height + BRICK_GAP_VERTICAL) and x.center_x == brick.center_x]

    def find_bricks_cardinal(self, brick):
        bricks = self.find_bricks_adjacent(brick)
        bricks.extend(self.find_bricks_stacked(brick))
        return bricks

    def side_collision(self, obj1, obj2):
        """
        Check for a side collision between two sprites.
        Expects obj1 to be the ball, and obj2 to be the brick.
        """
        # test right hand side.
        right = obj2._get_right()
        left = right - 1
        top = obj2._get_top() - 1
        bottom = obj2._get_bottom() + 1
        right_hit = self.range_overlap(obj1._get_left(), obj1._get_right(), left, right) and self.range_overlap(obj1._get_bottom(), obj1._get_top(), bottom, top)
        # test left hand side.
        left = obj2._get_left()
        right = left + 1
        left_hit = self.range_overlap(obj1._get_left(), obj1._get_right(), left, right) and self.range_overlap(obj1._get_bottom(), obj1._get_top(), bottom, top)
        return left_hit or right_hit

    def range_overlap(self, a_min, a_max, b_min, b_max):
        """ See if one set of coords overlaps another set or coords.
        """
        return (a_min <= b_max) and (b_min <= a_max)

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
