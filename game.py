import pygame as pg
from pygame.locals import *
import os
import sys
import random
from settings import *
from player import *
from spritesheet import *


class Game():

    def __init__(self):
        # initialise pygame
        pg.init()
        pg.mixer.init()
        # Create clock for time:frame tracking - used as a reference for maintaining desired fps
        self.clock = pg.time.Clock()
        self.running = True
        # create game screen - requires width, height but can take additional flags
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Name the game window/screen
        pg.display.set_caption(GAME_TITLE)
        self.font = pg.font.match_font(FONT)
        self.load_game_data()

    def load_game_data(self):

        self.dir = os.path.dirname(__file__)
        img_dir = os.path.join(self.dir, 'assets/img/')
        # 'r+' allows read + write; creates file if it doesn't exist
        with open(os.path.join(self.dir, HIGHSCORE_FILE), 'r+') as file:

            # in case the file does not have a high score written in it
            try:
                self.highscore = int(file.read())

            except:
                self.highscore = 0
        # SFX
        self.sound_dir = os.path.join(self.dir, 'assets/sound')
        self.jump_sound = pg.mixer.Sound(os.path.join(self.sound_dir, 'jump'))
        self.jump_sound.set_volume(0.4)

        self.music = pg.mixer.Sound(os.path.join(self.sound_dir, 'happy.ogg'))

        # Images
        self.spritesheet_idle = Spritesheet_Loader(os.path.join(img_dir, SPRITESHEET_PLAYER_IDLE))
        self.spritesheet_run = Spritesheet_Loader(os.path.join(img_dir, SPRITESHEET_PLAYER_RUN))
        self.spritesheet_jump = Spritesheet_Loader(os.path.join(img_dir, SPRITESHEET_PLAYER_JUMP))
        self.spritesheet_obstacles = Spritesheet(os.path.join(img_dir, SPRITESHEET_OBSTACLES))

        self.spritesheet_enemies = Spritesheet_Loader(os.path.join(img_dir, ENEMY_T1))
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(os.path.join(img_dir, 'cloud{}.png'.format(i))).convert())

    def start(self):
        # start game #
        self.score = 0

        # self.main_menu() # moved main menu call so that sprite was initialised to be used on main menu screen4

        # Layered system allows you to specify which object/image gets drawn first; without this draw call issues
        # arise, e.g. enemy sprite was sometimes moving in front of player and other times behind
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.enemy = pg.sprite.Group()
        # obstacle group for collisions
        self.obstacles = pg.sprite.Group()
        self.buffs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        # here self is providing the Player class with a Game object
        self.player = Player(self)
        # self.all_sprites.add(self.player)
        # self.main_menu()

        for plat in PLATFORM_LIST:
            Obstacles(self, *plat)
            # platform = Obstacles(*plat) # call self too? vid 15:powerups
            # self.all_sprites.add(platform)
            # self.obstacles.add(platform)
        self.enemy_timer = 0
        # spawn obstacle
        ob1 = Obstacles(self, 0, 0)
        # self.all_sprites.add(ob1)
        # self.obstacles.add(ob1)
        pg.mixer.music.load(os.path.join(self.sound_dir, 'happy.ogg'))
        pg.mixer.music.set_volume(0.05)
        pg.mixer.music.play(loops=-1)  # infinitely repeat

        self.playing = True
        while self.playing:
            # maintain desired loop run speed
            self.clock.tick(FPS)
            self.get_events()
            self.update()
            self.draw()

        pg.mixer.music.fadeout(200)

    def update(self):
        """
        Updates Game Loop -

        """
        self.all_sprites.update()

        # spawn enemy
        current_time = pg.time.get_ticks()
        global enemy_spawn_mod
        enemy_spawn_mod = 0
        enemy_spawn_mod -= self.score/2 #difficulty modifier; as players score increases, enemy spawn rate increased
        print(enemy_spawn_mod)
        if current_time - self.enemy_timer > ENEMY_ONE_SPAWN_FREQ + enemy_spawn_mod + \
                random.choice([-1000, -500, 0, 500, 1000]):
            # enemy_spawn_mod -= self.score
            # print(enemy_spawn_mod)
            self.enemy_timer = current_time
            Enemy(self)
        # else:
        #     if current_time - self.enemy_timer > ENEMY_ONE_SPAWN_FREQ + random.choice([-1000, -500, 0, 500, 1000]):
        #         self.enemy_timer = current_time
        #         Enemy(self)

        # collision with = game over; using collision mask for crisper interaction
        enemy_collision = pg.sprite.spritecollide(self.player, self.enemy, False, pg.sprite.collide_mask)
        if enemy_collision:
            self.playing = False

        # checks if player collides with obstacle/platform/ground etc, ONLY if falling. Without this check, jumping up
        # through platforms will snap the Player to the obstacle/platform. HENCE, NOT NEEDED IF INTEND TO DISALLOW
        # JUMPING UP THROUGH PLATFORMS
        if self.player.vel.y > 0:

            # collision check between player and environment (obstacles); False = obstacle not deleted upon collision
            collide = pg.sprite.spritecollide(self.player, self.obstacles, False)  # pg.sprite.collide_mask

            # if a collision is detected, set the players new position on y axis to the top
            # of the obstacles rect
            if collide:
                # track relative obstacle/platform height (y coord)
                lowest_plat = collide[0]
                # for platforms that spawn proximal to one another, i.e. one slightly above/beneath the other -
                # make sure the lowest platform is evaluated first
                for collision in collide:
                    if collision.rect.bottom > lowest_plat.rect.bottom:
                        lowest_plat = collision

                if lowest_plat.rect.right > self.player.pos.x > lowest_plat.rect.left:
                    if self.player.pos.y < lowest_plat.rect.centery:
                        self.player.pos.y = lowest_plat.rect.top  # + 20#+ 13 # increase value so sprite was flush with ground
                        self.player.vel.y = 0
                        self.player.jumping = False

                # # ensures that players feet are above the platform before snapping to rect.top (previously players head
                # # area could make contact with underside of platform and snap model above platform
                # if self.player.pos.y < lowest_plat.rect.bottom:
                #     # without using +1 the player seemed to vibrate; adding 1 creates a 1 pixel offset between the
                #     # obstacle and player (i.e. technically player is not in contact with the obstacle/ground)
                #     # ANY OTHER SOLUTIONS???
                #     self.player.pos.y = lowest_plat.rect.top + 1
                #     # reset players y velocity to prevent gravity effect from pulling player through the floor
                #     self.player.vel.y = 0
                #     self.player.jumping = False

        jump_boost_collides = pg.sprite.spritecollide(self.player, self.buffs, True)

        for buff in jump_boost_collides:
            if buff.type == "jump":
                self.player.jump_boost = True
                self.player.vel.y = JUMP_BOOST
                # for i in range(200):
                #     self.player.vel.y -=2
                self.player.jumping = False  # so that you can't jump during boost

        # if player reaches top 1/5 of screen - scroll vertically #
        if self.player.rect.top <= SCREEN_HEIGHT / 5:
            if random.randrange(100) < 6:
                Clouds(self)
            for enemy in self.enemy:
                enemy.rect.y += max(abs(self.player.vel.y), 2)
            # using abs to circumvent negative player y velocity i.e. so that player.pos.y always increases
            # adding in the max func with integer 2 makes scrolling smoother
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 2)
            # shift obstacles with player
            for plat in self.obstacles:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                # remove obstacles as the screen scrolls to prevent unnecessary build up
                if plat.rect.top >= SCREEN_HEIGHT:
                    plat.kill()
                    self.score += 10

        if self.player.rect.bottom > SCREEN_HEIGHT:
            # for a camera falling type effect; otherwise player will fall to death and screen stays static
            for sprite in self.all_sprites:
                # approximates the velocity of obstacles/platforms to that of the falling player for nicer screen
                # fall effect; using a constant here is not good - as it doesn't give the same polished feel
                # between player falling from a low jump vs player falling from top of screen
                sprite.rect.y -= max(self.player.vel.y, 10)
                # if the sprite (obstacle) leaves the top of the screen - kill it
                if sprite.rect.bottom < 0:
                    sprite.kill()
            # when no more obstacles left on screen - restart game
        if len(self.obstacles) == 0:
            self.playing = False

        # continue to spawn obstacles as screen scrolls
        while len(self.obstacles) < 6:
            # randomise dimensions and pos of spawned obstacles
            width = random.randrange(50, 100)

            Obstacles(self, random.randrange(0, SCREEN_WIDTH - width),
                      random.randrange(-75, -30))

            ## PRIOR TO ADDING IN OBSTACLE SPRITES
            # obstacle = Obstacles(random.randrange(100, SCREEN_WIDTH - width),
            #                         random.randrange(-75, -30), width, 20)

            # self.obstacles.add(obstacle)
            # self.all_sprites.add(obstacle)

    def draw_text(self, text, size, colour, x, y):
        font = pg.font.Font(self.font, size)
        # True for anti-aliasing
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_interaction(self):
        interaction = False

        while not interaction:
            self.clock.tick(FPS)
            for event in pg.event.get():
                # allow exiting game at main menu
                if event.type == pg.QUIT:
                    interaction = True
                    self.running = False
                # press any key to start game - breaks loop and exits method
                # preferred using KEYDOWN because sometimes I would die while still holding
                # the jump key and result in immediately skipping the game over screen

                if event.type == pg.KEYDOWN:
                    interaction = True

    def main_menu(self):

        # splash/start screen #
        self.screen.fill(DEEP_SKY_BLUE)
        self.draw_text(GAME_TITLE, 72, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text("Press any key to begin", 36, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text("Highest Score: " + str(self.highscore), 36, BLACK, SCREEN_WIDTH / 2, 40)

        # NEED TO CLEAN THIS UP - DISPLAY PRIMARY PLAYER ON START SCREEN #
        # self.main_menu_blob = pg.transform.scale(self.player.image, (self.player.rect.width*2, self.player.rect.height*2))
        # self.main_menu_blob_rect = self.main_menu_blob.get_rect()
        # self.main_menu_blob_rect.centerx = SCREEN_WIDTH/3
        # self.screen.blit(self.main_menu_blob, (self.main_menu_blob_rect.centerx, 500))
        pg.display.flip()
        self.wait_for_interaction()

    def game_over(self):

        " If player hits bottom of screen or health reaches 0"
        #
        if not self.running:
            return

        self.screen.fill(DARK_RED)
        self.draw_text("LOSER!", 72, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text("Your Score: " + str(self.score), 24, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text("Press any key to play again...", 24, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)

        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE FUCKER!", 36, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40)
            with open(os.path.join(self.dir, HIGHSCORE_FILE), 'w') as file:
                file.write(str(self.score))
        else:
            self.draw_text("Highest Score: " + str(self.highscore), 36, BLACK, SCREEN_WIDTH / 2, 15)

        pg.display.flip()
        # press any key to restart game
        self.wait_for_interaction()
        pg.mixer.music.fadeout(500)

    def get_events(self):

        for event in pg.event.get():

            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                # pg.quit()
                # sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.player.jump()
            if event.type == KEYUP and event.key == K_SPACE:
                self.player.jump_modify()

    def draw(self):

        #
        self.screen.fill(SKY_DARKER_BLUE)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)  ## NEEDED??
        self.draw_text(str(self.score), 30, BLUE, SCREEN_WIDTH / 2, 15)
        # more efficient updating method - flip the display AFTER drawing everything
        pg.display.flip()
