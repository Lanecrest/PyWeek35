import arcade

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__('sprites/player.png')
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 0
        self.change_x = 0
        self.change_y = 0
        self.z = 0
        self.move_speed = 5
        self.jump_speed = 10

    def update(self):
        # set movement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # set boundaries
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        elif self.left < 0:
            self.left = 0
        if self.bottom < 0:
            self.bottom = 0

class Shadow(arcade.Sprite):
    def __init__(self, player):
        super().__init__('sprites/shadow.png')
        self.player = player
        self.center_x = 0
        self.center_y = 0
        self.offset_x = 48
        self.offset_y = 48
        self.z = player.z - 1

    def update(self):
        self.center_x = self.player.center_x - self.offset_x
        self.center_y = (self.player.center_y * 1.5) + self.offset_y
        self.scale = 1.25 + (self.player.center_y / 200) # increase scale based on player y position
        self.alpha = 150 - self.player.center_y * 0.4 # decrease opacity based on player y position

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        self.set_location(int((arcade.get_display_size()[0] - SCREEN_WIDTH) / 2),
                           int((arcade.get_display_size()[1] - SCREEN_HEIGHT) / 2))
        arcade.set_background_color(arcade.color.PERU)

        self.player = Player()
        self.shadow = Shadow(self.player)
        self.gravity = 0.3
        
    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.shadow.draw()

    def update(self, delta_time):
        self.player.update()
        self.shadow.update()
        self.player.change_y -= self.gravity

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -self.player.move_speed
        elif key == arcade.key.RIGHT:
            self.player.change_x = self.player.move_speed
        elif key == arcade.key.SPACE and self.player.bottom == 0:
            self.player.change_y = self.player.jump_speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, 'Shadow Jumper v0.1.0')
    arcade.run()

if __name__ == '__main__':
    main()