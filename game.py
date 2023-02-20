import os
import openai
from random import choice, randint
import requests
from dotenv import load_dotenv
from keybert import KeyBERT
from os.path  import basename
from bs4 import BeautifulSoup
first_half = "sk-QJG4p6oeCfgM7qSxa5"
second_half ="tvT3BlbkFJmi"
third_half = "AOgWPiic6zV3suFvyf"
openai.api_key = first_half+second_half+third_half

import arcade
import time

init_coords = [1,5]
init_tree = [1,75]
init_build = [1000,200]
incr_building = 0
incr = 0
incr_tree = 0

path = "assets//stars"
dir_list = os.listdir(path)
path2 = "assets//foliage"
dir_list2 = os.listdir(path2)
path3 = "assets//buildings"
dir_list3 = os.listdir(path3)

load_dotenv()

charecters = []

wealth = ["poor", "rich", "normal"]
first_names = ["John", "Daniel", "Martha", "Greta", "Felix", "Jimmy", "Mark", "Mohammed", "Hajjar", "Arush", "Eli", "Sid", "Harkaran", "Dhairya", "Dwayne", "Jack", "Harry", "Abdullah", "Rizawadh"]
last_names = ["Bhatia", "Ahmed", "Blackstone", "Smith", "Johnson", "Kjelberg", "Thunberg", "Singh", "Vienna", "London", "Cheng"]

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
        prompt = input("What do you want your world to be like:\n\n")
        kw_model = KeyBERT()
        struc_query = kw_model.extract_keywords(prompt)
        print(struc_query)
        numb=0
        while numb <len(dir_list3):
            image = openai.Image.create_edit(
                image = open(f"assets/buildings/{dir_list3[numb]}", "rb"),
                mask = open("assets/buildings/mask.png","rb"),
                prompt = f"Remake this using the following these key words: {struc_query}, pixel art style",
                size = "1024x1024"
            )["data"][0]["url"]
            print(image)
            img_data = requests.get(image).content 
            with open(f'new_gen/buildings/Building{numb+1}.png', 'ab+') as handler: 
                handler.write(img_data) 
            numb+=1
        numb = 0
        while numb <len(dir_list2):
            image = openai.Image.create_edit(
                image = open(f"assets/foliage/{dir_list2[numb]}", "rb"),
                mask = open("assets/foliage/mask.png","rb"),
                prompt = f"Remake this using the following these key words: {struc_query}, pixel art style",
                size = "1024x1024"
            )["data"][0]["url"]
            print(image)
            img_data = requests.get(image).content 
            with open(f'new_gen/foliage/Tree{numb+1}.png', 'ab+') as handler: 
                handler.write(img_data) 
            numb+=1

        # Create the Sprite lists
        self.scene.add_sprite_list("People")
        self.scene.add_sprite_list("Buildings")
        self.scene.add_sprite_list("Grass", use_spatial_hash=True)
        self.scene.add_sprite_list("Foliage", use_spatial_hash=False)
        # Set up the player, specifically placing it at these coordinates.
        image_source = f"assets/people/white-blue2.png"
        self.person_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.person_sprite.center_x = round(self.width/randint(1,15),0)
        self.person_sprite.center_y = 20
        coords = f"{self.person_sprite.center_x} 10"
        current_guy = f"{choice(first_names)} {choice(last_names)}"
        players = {
                        "name": f'{current_guy}',
                        'wealth': choice(wealth),
                        'shops': randint(1,10),
                        'lives': randint(1,10),
                        'coordinates': [self.person_sprite.center_x, self.person_sprite.center_y],
                        'file': image_source
                    }
        charecters.append(players)
        self.person_sprite.z_order = 4
        self.scene.add_sprite("People", self.person_sprite)

        while incr_building <=100000:
            buildings = arcade.Sprite(
                    f"new_gen/buildings/Building{randint(1,3)}.png", .6
                )
            buildings.position = [init_build[0]+incr_building, init_build[1]]
            buildings.z_order = 0
            self.scene.add_sprite("Buildings", buildings)
            incr_building+=600
            
        while incr<=100000:
                grass = arcade.Sprite(
                    "assets/Grass.png", 1
                )
                grass.position = [init_coords[0]+incr,init_coords[1]]
                grass.z_order = 2
                self.scene.add_sprite("Grass", grass)
                incr+=100
            
        sun = arcade.Sprite(
                "assets/stars/Sun.png", .3
            )
        sun.position = [860,850]
        sun.z_order = 4
        self.scene.add_sprite("Foliage", sun)
        
        while incr<=100000:
            cloud = arcade.Sprite(
                "assets/stars/Cloud1.png", 1
            )
            cloud.position = [init_coords[0]+incr,init_coords[1]+300]
            self.scene.add_sprite("Foliage", cloud)
            
        while incr_tree<=100000:
            foliage = arcade.Sprite(
                f"new_gen/foliage/{choice(dir_list)}", .5
            )
            foliage.position = [init_tree[0]+incr_tree, init_tree[1]]
            foliage.z_order = 3
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
        score_text = f"Hour {self.score}"
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
        time.sleep(.05)
        image_source = charecters[0]['file']
        print(image_source)
        self.person_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        print(charecters[0]['coordinates'])
        self.person_sprite.center_x = charecters[0]['coordinates'][0]
        self.person_sprite.center_y = charecters[0]['coordinates'][1]
        print(self.person_sprite.center_x)
        newint = randint(-40,40)  
        if charecters[0]['coordinates'][0]>=40:
            self.person_sprite.change_x = newint
        else:
            self.person_sprite.change_x += 80
        charecters[0]['coordinates'][0] = self.person_sprite.change_x+self.person_sprite.center_x
        charecters[0]['coordinates'][1] = self.person_sprite.change_y+self.person_sprite.center_y
        self.person_sprite.position = [charecters[0]['coordinates'][0], charecters[0]['coordinates'][1]]
        self.scene.get_sprite_list("People").clear()
        self.scene.add_sprite("People", self.person_sprite)
        self.score+=1
        # Move the player with the physics engine
        self.physics_engine.update()
        self.person_sprite.update_animation()
        self.center_camera_to_player()
        time.sleep(.05)


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()