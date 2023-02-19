import arcade
import os
from time import sleep
import openai
from random import choice, randint

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Void Advancement"

path = "assets//people"
dir_list = os.listdir(path)
print(dir_list)
people = dir_list

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.people_list = None
        self.buildings_list = None
        self.foliage_list = None
        self.person = None
        arcade.set_background_color(arcade.color.AMAZON)


    def setup(self):
        self.people_list = arcade.SpriteList()
        self.buildings_list = arcade.SpriteList(use_spatial_hash=True)
        self.foliage_list = arcade.SpriteList(use_spatial_hash=True)
        self.all_sprites = arcade.SpriteList()
        self.person = arcade.Sprite(f"assets/people/{choice(people)}")
        self.person.center_y = self.height/2
        self.person.left = 10
        self.people_list.append(self.person)
        arcade.schedule(self.add_people, 0.25)
        
    def add_people(self, delta_time: float):
        self.people = arcade.Sprite(f"assets/people/{choice(people)}")
        self.people.left = randint(self.width, self.width + 80)
        self.people.top = randint(10, self.height - 10)

    def on_draw(self):
        self.clear()
        self.people_list.draw()

    def on_update(self, delta_time):
        pass

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
