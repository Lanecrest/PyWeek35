import arcade, random

screen_width = 640
screen_height = 480

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__('sprites/player.png')
        # set initial values
        self.center_x = screen_width // 2
        self.center_y = 0
        self.z = 0
        self.move_speed = 5
        self.jump_speed = 10

    def update(self):
        # set movement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # set boundaries
        if self.right > screen_width:
            self.right = screen_width
        elif self.left < 0:
            self.left = 0
        if self.bottom < 0:
            self.bottom = 0

class Shadow(arcade.Sprite):
    def __init__(self, player):
        super().__init__('sprites/shadow.png')
        self.player = player
        # set initial values
        self.offset_x = 40
        self.offset_y = 40
        self.adjust_scale = 0
        self.z = player.z - 1

    def update(self):
        self.center_x = self.player.center_x - self.offset_x    # x position is tied to player x position
        self.center_y = (self.player.center_y * 1.5) + self.offset_y    # y position is tied to player y position
        self.scale = 1 + self.adjust_scale
        self.alpha = 175 - self.center_y * 0.4  # decrease opacity based on y position
        self.height = (32 * self.scale) + (self.player.center_y * 0.25)  # increase height based on y position
        
class ShadowRay(arcade.Sprite):
    def __init__(self, shadow):
        super().__init__('sprites/shadow.png')
        self.shadow = shadow
        # set initial values
        self.move_speed = -15
        self.alpha = 200
        self.z = shadow.z
        self.height = 64
        self.width = 16

    def update(self):
        self.center_y += self.move_speed
        # set respawn logic
        if self.top < 0:
            self.center_x = random.randint(0, screen_width)
            self.bottom = screen_height
        
class Energy(arcade.Sprite):
    def __init__(self, player):
        super().__init__('sprites/energy.png')
        # set initial values
        self.move_speed = -10
        self.scale = 0.3
        self.z = player.z

    def update(self):
        self.center_x += self.move_speed
        # set respawn logic
        if self.right < 0:
            self.left = screen_width
            self.bottom = random.randint(0, screen_height) / 3

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        self.set_location(int((arcade.get_display_size()[0] - screen_width) / 2),
                           int((arcade.get_display_size()[1] - screen_height) / 2))
        arcade.set_background_color(arcade.color.SIENNA)
        self.gravity = 0.3
        self.setup_game()
        
    def setup_game(self):
        self.game_over = False
        self.time = 200
        self.player = Player()
        self.energy = Energy(self.player)
        self.shadow = Shadow(self.player)
        self.shadow_ray = ShadowRay(self.shadow)
        
    def on_draw(self):
        arcade.start_render()
        if not self.game_over:
            self.shadow_ray.draw()
            self.shadow.draw()
            self.player.draw()
            self.energy.draw()
            arcade.draw_text(f'Time: {int(self.time)}', 10, screen_height - 20, arcade.color.BLACK, 14)
        elif self.game_over and self.time <= 0:
            arcade.draw_text('YOU LOSE', 0, screen_height // 2,
                             arcade.color.BLACK, 40, screen_width, 'center',
                             font_name=('calibri', 'arial'))
            arcade.draw_text(f'Your shadow has to go now, its planet needs it.\nPress "Enter" to restart', 0, screen_height // 2 - 40,
                             arcade.color.BLACK, 20, screen_width, 'center',
                             font_name=('calibri', 'arial'))
        elif self.game_over and self.shadow.scale <= 0.11:
            arcade.draw_text('YOU LOSE', 0, screen_height // 2,
                             arcade.color.BLACK, 40, screen_width, 'center',
                             font_name=('calibri', 'arial'))
            arcade.draw_text(f'The goggles do nothing!\nPress "Enter" to restart', 0, screen_height // 2 - 40,
                             arcade.color.BLACK, 20, screen_width, 'center',
                             font_name=('calibri', 'arial'))
        elif self.game_over and self.shadow.width >= 101:
            arcade.draw_text('YOU WIN', 0, screen_height // 2,
                             arcade.color.BLACK, 40, screen_width, 'center',
                             font_name=('calibri', 'arial'))
            arcade.draw_text(f'You have cromulently embiggened your shadow!\nYour Score: {int(self.time)}\nPress "Enter" to restart', 0, screen_height // 2 - 40,
                             arcade.color.BLACK, 20, screen_width, 'center',
                             font_name=('calibri', 'arial'))

    def update(self, delta_time):
        if not self.game_over:
            self.player.update()
            self.energy.update()
            self.shadow.update()
            self.shadow_ray.update()
            self.player.change_y -= self.gravity
            self.time -= 1 / 30
        # check for collisions
        if arcade.check_for_collision(self.shadow, self.shadow_ray):
            self.shadow.adjust_scale -= 0.1
            self.shadow_ray.center_x = random.randint(0, screen_width)
            self.shadow_ray.bottom = screen_height
            print(f'Scale: {self.shadow.scale}')    # for debugging
            print(f'Width: {self.shadow.width}')    # for debugging
        if arcade.check_for_collision(self.player, self.energy):
            self.shadow.adjust_scale += 0.1
            self.energy.left = screen_width
            print(f'Scale: {self.shadow.scale}')    # for debugging
            print(f'Width: {self.shadow.width}')    # for debugging
            self.energy.bottom = random.randint(0, screen_height) / 3
        if self.shadow.scale <= 0.11 or self.shadow.width > 101 or self.time <= 0:
            self.game_over = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -self.player.move_speed
        elif key == arcade.key.RIGHT:
            self.player.change_x = self.player.move_speed
        elif key == arcade.key.SPACE and self.player.bottom == 0:
            self.player.change_y = self.player.jump_speed
        elif self.game_over and key == arcade.key.ENTER:
            self.setup_game()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

def main():
    game = MyGame(screen_width, screen_height, 'Shadow Embiggener v0.2.1')
    arcade.run()

if __name__ == '__main__':
    main()