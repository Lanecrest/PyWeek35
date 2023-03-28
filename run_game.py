import arcade, random, math

screen_width = 640
screen_height = 480
game_title = 'Shadow Embiggener v0.3.0'

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__('sprites/player.png')
        # set initial values
        self.center_x = screen_width // 2
        self.center_y = 0
        self.z = 0
        self.move_speed = 6.5
        self.scale = 2

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
        elif self.top > screen_height:
            self.top = screen_height

class Shadow(arcade.Sprite):
    def __init__(self, player):
        super().__init__('sprites/shadow.png')
        self.player = player
        # set initial values
        self.offset_x = 32
        self.offset_y = 32
        self.adjust_scale = 0
        self.z = player.z - 1
        self.scale = 1

    def update(self):
        self.center_x = self.player.center_x - self.offset_x    # x position is tied to player x position
        self.center_y = self.player.center_y + self.offset_y    # y position is tied to player y position
        self.scale = 1 + self.adjust_scale
        self.height = (32 * self.scale) + (self.player.center_y * 0.25)  # increase height based on y position
        if self.alpha <= 200:
            self.alpha = 200 - self.center_y * 0.4  # decrease opacity based on y position
        else:
            self.alpha = 200
  
class ShadowRay(arcade.Sprite):
    def __init__(self, shadow):
        super().__init__('sprites/shadow_ray.png')
        self.shadow = shadow
        # set initial values
        self.move_speed = -15
        self.z = shadow.z
        self.height = 10
        self.width = 80

    def update(self):
        self.center_x += self.move_speed
        # set respawn logic
        if self.right < 0:
            self.left = screen_width
            self.bottom = random.randint(0, screen_height)
        if self.alpha <= 255:
            self.alpha = 255 - self.center_y * 0.4  # decrease opacity based on y position
        else:
            self.alpha = 255
        
class Energy(arcade.Sprite):
    def __init__(self, player):
        super().__init__('sprites/energy.png')
        self.player = player
        # set initial values
        self.move_speed = 10
        self.scale = 0.3
        self.z = player.z

    def update(self):
        self.center_x += self.move_speed

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        self.set_location(int((arcade.get_display_size()[0] - screen_width) / 2),
                           int((arcade.get_display_size()[1] - screen_height) / 2))
        # set movement keys, arrow keys or WSAD
        self.move_keys = {
            arcade.key.UP: (0, 1),
            arcade.key.DOWN: (0, -1),
            arcade.key.W: (0, 1),
            arcade.key.S: (0, -1),
            arcade.key.LEFT: (-1, 0),
            arcade.key.RIGHT: (1, 0),
            arcade.key.A: (-1, 0),
            arcade.key.D: (1, 0)
        }                                 
        self.background = arcade.load_texture('sprites/background.png')
        self.background_pos = 0
        self.setup_game()   # call the setup/new game function
        
    def setup_game(self):
        self.game_over = False
        self.time = 200
        self.player = Player()
        self.energy_list = arcade.SpriteList()
        self.shadow = Shadow(self.player)
        self.shadow_ray = ShadowRay(self.shadow)
        
    def on_draw(self):
        arcade.start_render()
        # set two copies of the background texture for seamless scrolling
        arcade.draw_texture_rectangle(screen_width / 2 + self.background_pos, screen_height / 2, screen_width, screen_height, self.background)
        arcade.draw_texture_rectangle(screen_width / 2 + self.background_pos + screen_width, screen_height / 2, screen_width, screen_height, self.background)
        # set display text on game screen
        arcade.draw_text(f'Time: {int(self.time)}', 10, screen_height - 20, arcade.color.BLACK, 14)
        arcade.draw_text(f'Embiggen %: {round((self.shadow.width / screen_width) * 100)}', 10, screen_height - 40, arcade.color.BLACK, 14)
        # only draw the game elements if not in a game_over status
        if not self.game_over:
            self.shadow_ray.draw()
            self.shadow.draw()
            self.player.draw()
            self.energy_list.draw()
        # time limit game_over lose
        elif self.game_over and self.time <= 0:
            arcade.draw_text('YOU LOSE', 0, screen_height // 2,
                             arcade.color.BLACK, 40, screen_width, 'center',
                             font_name=('calibri', 'arial'))
            arcade.draw_text(f'Your shadow has to go now, its planet needs it.\nPress "Enter" to restart', 0, screen_height // 2 - 40,
                             arcade.color.BLACK, 20, screen_width, 'center',
                             font_name=('calibri', 'arial'))
        # shadow loss game_over lose
        elif self.game_over and self.shadow.scale <= 0:
            arcade.draw_text('YOU LOSE', 0, screen_height // 2,
                             arcade.color.BLACK, 40, screen_width, 'center',
                             font_name=('calibri', 'arial'))
            arcade.draw_text(f'The goggles do nothing!\nPress "Enter" to restart', 0, screen_height // 2 - 40,
                             arcade.color.BLACK, 20, screen_width, 'center',
                             font_name=('calibri', 'arial'))
        # shadow embiggen game_over win
        elif self.game_over and self.shadow.width >= screen_width:
            arcade.draw_text('YOU WIN', 0, screen_height // 2,
                             arcade.color.BLACK, 40, screen_width, 'center',
                             font_name=('calibri', 'arial'))
            arcade.draw_text(f'You have cromulently embiggened your shadow!\nYour Score: {int(self.time)}\nPress "Enter" to restart', 0, screen_height // 2 - 40,
                             arcade.color.BLACK, 20, screen_width, 'center',
                             font_name=('calibri', 'arial'))

    def update(self, delta_time):
        self.background_pos -= 2
        if self.background_pos < -screen_width:
            self.background_pos = screen_width - (self.background_pos % screen_width)
        elif self.background_pos > screen_width:
            self.background_pos = self.background_pos % screen_width
        # only update game elements if not in a game_over status
        if not self.game_over:
            self.player.update()
            self.energy_list.update()
            self.shadow.update()
            self.shadow_ray.update()
            self.shadow.adjust_scale += 0.01
            self.time -= 1 / 30
        # check for collisions
        if arcade.check_for_collision(self.shadow, self.shadow_ray):
            self.shadow.adjust_scale -= 1
            self.shadow_ray.left = screen_width
            self.shadow_ray.bottom = random.randint(0, screen_height)
        if arcade.check_for_collision_with_list(self.shadow_ray, self.energy_list):
            self.shadow_ray.left = screen_width
            self.shadow_ray.bottom = random.randint(0, screen_height)
        # check for game_over
        if self.shadow.scale <= 0 or self.shadow.width > screen_width or self.time <= 0:
            self.game_over = True

    def on_key_press(self, key, modifiers):
        if key in self.move_keys:
            x_dir, y_dir = self.move_keys[key]
            diagonal_speed = self.player.move_speed / math.sqrt(2)  # approximate diagonal movement speed to cardinal movement
            self.player.change_x += x_dir * diagonal_speed
            self.player.change_y += y_dir * diagonal_speed
        elif key == arcade.key.SPACE:
            energy_blast = Energy(self.player)
            energy_blast.center_x = self.player.right
            energy_blast.center_y = self.player.center_y
            self.energy_list.append(energy_blast)
        elif self.game_over and key == arcade.key.ENTER:
            self.setup_game()   # call the setup/new game function

    def on_key_release(self, key, modifiers):
        if key in self.move_keys:
            x_dir, y_dir = self.move_keys[key]
            diagonal_speed = self.player.move_speed / math.sqrt(2)  # approximate diagonal movement speed to cardinal movement
            if self.player.change_x == x_dir * diagonal_speed and (y_dir == 0 or self.player.change_y == y_dir * diagonal_speed):
                self.player.change_x = 0
            if self.player.change_y == y_dir * diagonal_speed and (x_dir == 0 or self.player.change_x == x_dir * diagonal_speed):
                self.player.change_y = 0

def main():
    game = MyGame(screen_width, screen_height, game_title)
    arcade.run()

if __name__ == '__main__':
    main()