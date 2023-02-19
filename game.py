import arcade
import os
import openai
from random import choice, randint
openai.api_key = "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"

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Void Advancement"

path = "assets//people"
dir_list = os.listdir(path)
print(dir_list)
people = dir_list

charecters = []

wealth = ["poor", "rich", "normal"]
first_names = ["John", "Daniel", "Martha", "Greta", "Felix", "Jimmy", "Mark", "Mohammed", "Hajjar", "Arush", "Eli", "Sid", "Harkaran", "Dhairya", "Dwayne", "Jack", "Harry", "Abdullah", "Rizawadh"]
last_names = ["Bhatia", "Ahmed", "Blackstone", "Smith", "Johnson", "Kjelberg", "Thunberg", "Singh", "Vienna", "London", "Cheng"]

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.scene = None
        self.person = None
        self.gui_camera = None
        self.score = 0
        arcade.set_background_color(arcade.color.AMAZON)


    def setup(self):
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("People")
        self.scene.add_sprite_list("Buildings", use_spatial_hash=True)
        self.scene.add_sprite_list("Foliage", use_spatial_hash=True)
        x = 0
        y = 0
        while x<=10:
            persons_file = choice(people)
            self.person = arcade.Sprite(f"assets/people/{persons_file}")
            self.person.center_y = 20
            self.person.left = round(self.width/randint(1,11),0)
            current_guy = f"{choice(first_names)} {choice(last_names)}"
            coords = f"{self.person.left} 20"
            players = {
                    "name": f'{current_guy}',
                    'wealth': choice(wealth),
                    'shops': randint(1,10),
                    'lives': randint(1,10),
                    'coordinates': [self.person.left, 20],
                    'file': persons_file
                }
            charecters.append(players)
            list_len = len(charecters)
            while y<list_len and list_len!=1 and charecters[y]["name"] != current_guy:
                print(list_len)
                print(charecters[y]["name"])
                print(current_guy)
                print(y)
                print(charecters)
                if float((coords.split(" "))[0])-40<charecters[y]['coordinates'][0]<float((coords.split(" "))[0])+40:
                    y+=1
                else:
                    self.scene.add_sprite("People", self.person)
                    y+=1
            x+=1

    def on_draw(self):
        self.clear()
        self.scene.draw()
        
    def on_update(self, delta_time: float):
        list_len = len(charecters)
        y=0
        while y<list_len:
            print(list_len)
            file_name = charecters[y]["file"]
            print(charecters[y]["coordinates"][0])
            self.person = arcade.Sprite(f"assets/people/{file_name}")
            coords = charecters[y]["coordinates"][0] + randint(-40,40)
            self.person.left = coords
            charecters[y]["coordinates"][0] = coords
            print(coords)
            print(charecters[y]["coordinates"][0])
            y+=1
            
            
    def on_key_press(self, key, key_modifiers):
        pass

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
