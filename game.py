import os
import openai
from random import choice, randint
openai.api_key = "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"

import arcade

path = "assets//foliage"
dir_list = os.listdir(path)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Void Advancement"
CHARACTER_SCALING = 1
TILE_SCALING = 0.1

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.person_sprite = None

        self.physics_engine = None
        
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Person")
        self.scene.add_sprite_list("Buildings", use_spatial_hash=True)
        self.scene.add_sprite_list("Foliage", use_spatial_hash=False)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "assets/people/tan-green.gif"
        self.person_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.person_sprite.center_x = 64
        self.person_sprite.center_y = 20
        self.scene.add_sprite("Player", self.person_sprite)
        buildings = arcade.Sprite(
                "assets/buildings/Building1.png", .3
            )
        buildings.position = [1000,300]
        self.scene.add_sprite("Buildings", buildings)
        coordinate_list = [[0, 5], [101, 5], [201, 5], [301, 5],[401, 5],[501, 5],[601, 5],[701, 5],[801, 5],[901, 5],[1001, 5],[1101, 5],[1201, 5],[1301, 5],[1401, 5],[1501, 5],[1601, 5],[1701, 5],[1801, 5],[1901, 5]]
        coordinate_list2 = [[0, 75], [201, 75],[401, 75],[601, 75],[801, 75],[1001, 75],[1201, 75],[1401, 75],[1601, 75],[1801, 75]]
        for coordinate in coordinate_list:
            grass = arcade.Sprite(
                "assets/Grass.png", 1
            )
            grass.position = coordinate
            self.scene.add_sprite("Buildings", grass)
        for coordinate in coordinate_list2:
            foliage = arcade.Sprite(
                f"assets/foliage/{choice(dir_list)}", .25
            )
            foliage.position = coordinate
            self.scene.add_sprite("Foliage", foliage)
            
            
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.person_sprite, gravity_constant=GRAVITY, walls = self.scene["Buildings"]
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our Scene
        self.scene.draw()
    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.person_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.person_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.person_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.person_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.person_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.person_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.person_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.person_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()