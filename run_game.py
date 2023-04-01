import arcade, random, math

screen_width = 640
screen_height = 480
game_title = 'Shadow Embiggener v0.5.0'

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__('sprites/player.png')
        # set initial values
        self.center_x = screen_width / 2
        self.center_y = screen_height / 2
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
        self.center_x = self.player.center_x - self.offset_x    # x position is tied to player x position
        self.center_y = self.player.center_y + self.offset_y    # y position is tied to player y position
        self.adjust_scale = 0
        self.z = player.z - 1

    def update(self):
        self.center_x = self.player.center_x - self.offset_x
        self.center_y = self.player.center_y + self.offset_y
        self.scale = 2.2 + self.adjust_scale
        if self.alpha <= 225:
            self.alpha = 225 - self.center_y * 0.4  # decrease opacity based on y position
        else:
            self.alpha = 225
  
class Barrier(arcade.Sprite):
    def __init__(self, shadow):
        super().__init__('sprites/barrier.png')
        self.shadow = shadow
        # set initial values
        self.move_speed = -10
        self.z = shadow.z
        self.scale = 1.1

    def update(self):
        self.center_x += self.move_speed
        # set respawn logic
        if self.right < 0:
            self.set_position(screen_width, random.randint(int(0 + self.height), int(screen_height - self.height)))
            self.respawn_timer = 0
        if self.alpha <= 225:
            self.alpha = 225 - self.center_y * 0.4  # decrease opacity based on y position
        else:
            self.alpha = 225
            
class Power(arcade.Sprite):
    def __init__(self, player):
        super().__init__('sprites/power.png')
        self.player = player
        # set initial values
        self.z = player.z
        self.scale = 0.6

    def update(self):
        # set respawn logic
        if self.right < 0 or self.alpha <= 50:
            self.set_position(screen_width, random.randint(int(0 + self.height), int(screen_height - self.height)))
            self.alpha = 255
        if self.center_x == screen_width / 2:
            self.move_speed = 0
            self.alpha -= 1
        else:
            self.move_speed = -2.5
        self.center_x += self.move_speed

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

class GamePlay(arcade.Window):
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
        self.bg_music = arcade.load_sound(':resources:music/funkyrobot.mp3')
        self.bg_music_player = None
        self.energy_sound = arcade.load_sound(':resources:sounds/laser1.wav')
        self.shadow_hit_sound = arcade.load_sound(':resources:sounds/hurt1.wav')
        self.barrier_hit_sound = arcade.load_sound(':resources:sounds/hurt4.wav')
        self.power_hit_sound = arcade.load_sound(':resources:sounds/upgrade3.wav')
        self.game_on = False
        self.setup_game()   # call the setup/new game function
        
    def setup_game(self):
        self.game_over = False
        self.timer = 0
        self.hit_count = 0
        self.player = Player()
        self.energy_list = arcade.SpriteList()
        self.shadow = Shadow(self.player)
        self.barrier = Barrier(self.shadow)
        self.power = Power(self.player)
        
    def on_draw(self):
        arcade.start_render()
        if not self.game_on:
            self.title_screen() # show title screen on launch
        elif self.game_over:
            self.end_screen()   # show end screen on win/loss
        else:
            if not self.bg_music_player or not self.bg_music_player.playing:
                self.bg_music_player = arcade.play_sound(self.bg_music, .2)
            # set two copies of the background texture for seamless scrolling
            arcade.draw_texture_rectangle(screen_width / 2 + self.background_pos, screen_height / 2, screen_width, screen_height, self.background)
            arcade.draw_texture_rectangle(screen_width / 2 + self.background_pos + screen_width, screen_height / 2, screen_width, screen_height, self.background)
            # set display text on game screen
            arcade.draw_text(f'Embiggen %: {round((self.shadow.width / screen_width) * 100) - 1}', 10, screen_height - 20, arcade.color.BLACK, 14)
            # draw the game elements
            self.energy_list.draw()
            self.shadow.draw()
            self.barrier.draw()
            self.power.draw()
            self.player.draw()

    def update(self, delta_time):
        self.background_pos -= 2
        if self.background_pos < -screen_width:
            self.background_pos = screen_width - (self.background_pos % screen_width)
        elif self.background_pos > screen_width:
            self.background_pos = self.background_pos % screen_width
        # only update game elements if not in a game_over status
        if not self.game_over and self.game_on:
            self.timer += 1 / 30 # timer
            self.player.update()
            self.energy_list.update()
            self.shadow.update()
            self.barrier.update()
            self.power.update()
        # check for collisions
        if arcade.check_for_collision(self.shadow, self.barrier):
            arcade.play_sound(self.shadow_hit_sound)
            self.shadow.adjust_scale -= 1
            self.hit_count += 1
            self.barrier.set_position(screen_width, random.randint(int(0 + self.barrier.height), int(screen_height - self.barrier.height)))
        if arcade.check_for_collision(self.player, self.power):
            arcade.play_sound(self.power_hit_sound)
            self.shadow.adjust_scale += 0.85
            self.power.set_position(screen_width, random.randint(int(0 + self.power.height), int(screen_height - self.power.height)))  
            self.power.alpha = 255
        energy_collision = arcade.check_for_collision_with_list(self.barrier, self.energy_list)
        if energy_collision:
            arcade.play_sound(self.barrier_hit_sound)
            for energy in energy_collision:
                energy.kill()
            self.barrier.set_position(screen_width, random.randint(int(0 + self.barrier.height), int(screen_height - self.barrier.height)))
        # check for game_over
        if self.shadow.scale <= 0 or self.shadow.width >= screen_width:
            self.game_over = True

    def on_key_press(self, key, modifiers):
        if key in self.move_keys:
            x_dir, y_dir = self.move_keys[key]
            diagonal_speed = self.player.move_speed / math.sqrt(2)  # approximate diagonal movement speed to cardinal movement
            self.player.change_x += x_dir * diagonal_speed
            self.player.change_y += y_dir * diagonal_speed
        elif key == arcade.key.SPACE and (self.game_on and not self.game_over):
            arcade.play_sound(self.energy_sound)
            energy_blast = Energy(self.player)
            energy_blast.center_x = self.player.right
            energy_blast.center_y = self.player.center_y
            self.energy_list.append(energy_blast)
        elif key == arcade.key.ENTER and (not self.game_on or self.game_over):
            self.game_on = True  # make sure the title screen isn't called back
            self.setup_game()   # call the setup/new game function

    def on_key_release(self, key, modifiers):
        if key in self.move_keys:
            x_dir, y_dir = self.move_keys[key]
            diagonal_speed = self.player.move_speed / math.sqrt(2)  # approximate diagonal movement speed to cardinal movement
            if self.player.change_x == x_dir * diagonal_speed and (y_dir == 0 or self.player.change_y == y_dir * diagonal_speed):
                self.player.change_x = 0
            if self.player.change_y == y_dir * diagonal_speed and (x_dir == 0 or self.player.change_x == x_dir * diagonal_speed):
                self.player.change_y = 0
                
    def title_screen(self):
        arcade.set_background_color(arcade.color.BLACK)
        arcade.draw_text('Shadow Embiggener', 0, screen_height / 2 + 40, arcade.color.WHITE, 40, screen_width, 'center', font_name=('calibri', 'arial'))
        arcade.draw_text('Move with WSAD or Arrow keys. Space to shoot.\nDestroy the incoming barriers to avoid getting hit.\nIf your shadow gets hit, it shrinks. Don\'t let it disappear!\nCollect blue powerups to grow your shadow to the size of the screen!', 0, screen_height / 2, arcade.color.WHITE, 10, screen_width, 'center', font_name=('calibri', 'arial'))
        arcade.draw_text('Press "Enter" to start', 0, screen_height / 2 - 100, arcade.color.WHITE, 20, screen_width, 'center', font_name=('calibri', 'arial'))
        
    def end_screen(self):
        max_score = 1000
        time_penalty = 3600
        hit_penalty = 2400
        score = max_score * (1 - (self.timer / (time_penalty * 2)) - (self.hit_count / hit_penalty))
        if score <= 0:
            score = 1
        arcade.set_background_color(arcade.color.BLACK)
        # loss
        if self.shadow.scale <= 0:
            arcade.draw_text('GAME OVER', 0, screen_height // 2, arcade.color.WHITE, 40, screen_width, 'center', font_name=('calibri', 'arial'))
            arcade.draw_text('The goggles do nothing!', 0, screen_height // 2 - 40, arcade.color.WHITE, 10, screen_width, 'center', font_name=('calibri', 'arial'))
            arcade.draw_text('Press "Enter" to restart', 0, screen_height // 2 - 80, arcade.color.WHITE, 20, screen_width, 'center', font_name=('calibri', 'arial'))
        # win
        elif self.shadow.width >= screen_width:
            arcade.draw_text('YOU WIN', 0, screen_height // 2, arcade.color.WHITE, 40, screen_width, 'center', font_name=('calibri', 'arial'))
            arcade.draw_text(f'You have cromulently embiggened your shadow!\nYour time was {int(self.timer)} and your shadow was hit {self.hit_count} times', 0, screen_height // 2 - 40, arcade.color.WHITE, 10, screen_width, 'center', font_name=('calibri', 'arial'))
            arcade.draw_text(f'Your Score: {int(score)}\nPress "Enter" to restart', 0, screen_height // 2 - 90, arcade.color.WHITE, 20, screen_width, 'center', font_name=('calibri', 'arial'))

def main():
    game = GamePlay(screen_width, screen_height, game_title)
    arcade.run()

if __name__ == '__main__':
    main()