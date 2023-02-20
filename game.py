import os
import openai
from random import choice, randint
openai.api_key = "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"

import arcade

init_coords = [1,5]
init_tree = [1,75]
init_build = [1000,200]
incr_building = 0
incr = 0
incr_tree = 0

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
        
        self.camera = None

        self.end_of_map = 0
        
        self.gui_camera = None

        self.score = 0      
        
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        global incr, incr_tree, init_coords, init_tree, init_build, incr_building
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.score = 0
        
        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Person")
        self.scene.add_sprite_list("Buildings")
        self.scene.add_sprite_list("Grass", use_spatial_hash=True)
        self.scene.add_sprite_list("Foliage", use_spatial_hash=False)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "assets/people/tan-green.gif"
        self.person_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.person_sprite.center_x = 64
        self.person_sprite.center_y = 10
        self.scene.add_sprite("Player", self.person_sprite)
        while incr_building <=100000:
            buildings = arcade.Sprite(
                    f"assets/buildings/Building{randint(1,3)}.png", .3
                )
            buildings.position = [init_build[0]+incr_building, init_build[1]]
            self.scene.add_sprite("Buildings", buildings)
            incr_building+=600
            
        coords_list = [[0,300], [353,300]]
        while incr<=100000:
                grass = arcade.Sprite(
                    "assets/Grass.png", 1
                )
                grass.position = [init_coords[0]+incr,init_coords[1]]
                self.scene.add_sprite("Grass", grass)
                incr+=100
            
        sun = arcade.Sprite(
                "assets/stars/Sun.png", .3
            )
        sun.position = [860,850]
        self.scene.add_sprite("Foliage", sun)
            
        for coordinate in coords_list:
            cloud = arcade.Sprite(
                "assets/stars/Cloud1.png", 1
            )
            
            
        while incr_tree<=100000:
            foliage = arcade.Sprite(
                f"assets/foliage/{choice(dir_list)}", .25
            )
            foliage.position = [init_tree[0]+incr_tree, init_tree[1]]
            self.scene.add_sprite("Foliage", foliage)
            incr_tree+=200
            
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.person_sprite, gravity_constant=GRAVITY, walls = self.scene["Grass"]
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()
        
        self.camera.use()

        # Draw our Scene
        self.scene.draw()
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )
        
    
    def center_camera_to_player(self):
        screen_center_x = self.person_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.person_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.score +=1
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
        self.center_camera_to_player()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()