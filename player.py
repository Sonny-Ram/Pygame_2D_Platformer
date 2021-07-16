import pygame as pg
from pygame.locals import *
import os
from settings import *
from spritesheet import *
import random

# alias for easy vector creation
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        # subclass Sprite for useful sprite functions
        super().__init__(self.groups)
        # give player a reference of game for collision updates
        self.game = game
        self.walking = False
        self.jumping = False
        self.running = False
        self.on_ground = True
        self.jump_boost = False
        self.current_frame = 0
        self.last_updated = 0
        self.load_images()
        # temporary square - width, height
        # self.image = pg.Surface((50, 50))
        # colour square red
        # self.image.fill(RED)

        self.image = self.idle_frames[0]

        # get rect for image (bounding box)
        self.rect = self.image.get_rect()
        # set rect starting position; thus, the starting position of player
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT + 10
        self.pos = vec(15, SCREEN_HEIGHT - 100)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)

    def load_images(self):

        self.idle_frames = [self.game.spritesheet.get_image(0, 0, 146, 149),
                            self.game.spritesheet.get_image(146, 0, 146, 149),
                            self.game.spritesheet.get_image(292, 0, 146, 149),
                            self.game.spritesheet.get_image(438, 0, 145, 149),
                            self.game.spritesheet.get_image(583, 0, 146, 149),
                            self.game.spritesheet.get_image(729, 0, 146, 149),
                            self.game.spritesheet.get_image(875, 0, 146, 149),
                            self.game.spritesheet.get_image(1021, 0, 145, 149),
                            self.game.spritesheet.get_image(1166, 0, 146, 149),
                            self.game.spritesheet.get_image(1312, 0, 146, 149),
                            self.game.spritesheet.get_image(1458, 0, 146, 149)]


        self.running_frames = [self.game.spritesheet_run.get_image(0, 0, 171, 177),
                               self.game.spritesheet_run.get_image(228, 0, 169, 177),
                               self.game.spritesheet_run.get_image(456, 0, 169, 177),
                               self.game.spritesheet_run.get_image(684, 0, 172, 177),
                               self.game.spritesheet_run.get_image(912, 0, 166, 177),
                               self.game.spritesheet_run.get_image(1140, 0, 177, 177),
                               self.game.spritesheet_run.get_image(0, 177, 171, 177),
                               self.game.spritesheet_run.get_image(228, 177, 193, 177),
                               self.game.spritesheet_run.get_image(456, 177, 217, 177),
                               self.game.spritesheet_run.get_image(684, 177, 228, 177),
                               self.game.spritesheet_run.get_image(912, 177, 224, 171),
                               self.game.spritesheet_run.get_image(1140, 177, 227, 171),
                               self.game.spritesheet_run.get_image(0, 354, 212, 171),
                               self.game.spritesheet_run.get_image(228, 354, 197, 171),
                               self.game.spritesheet_run.get_image(456, 354, 174, 171),
                               self.game.spritesheet_run.get_image(684, 354, 170, 171),
                               self.game.spritesheet_run.get_image(912, 354, 172, 171),
                               self.game.spritesheet_run.get_image(1140, 354, 154, 171),
                               ]

        self.running_frames_left = []
        # flip right running frames for left running animation
        for frame in self.running_frames:
            frame.set_colorkey(BLACK)
            self.running_frames_left.append(pg.transform.flip(frame, True, False))

        # self.idle_frames = [self.game.spritesheet.get_image(0, 0, 167, 191),
        #                     self.game.spritesheet.get_image(1139, 0, 159, 191),
        #                     self.game.spritesheet.get_image(495, 0, 162, 191),
        #                     self.game.spritesheet.get_image(332, 0, 163, 191),
        #                     self.game.spritesheet.get_image(1455, 0, 156, 191),
        #                     self.game.spritesheet.get_image(1611, 0, 155, 191),
        #                     self.game.spritesheet.get_image(657, 0, 162, 191),
        #                     self.game.spritesheet.get_image(819, 0, 160, 191),
        #                     self.game.spritesheet.get_image(1298, 0, 157, 191),
        #                     self.game.spritesheet.get_image(979, 0, 160, 191),
        #                     self.game.spritesheet.get_image(167, 0, 165, 191)]

        for frame in self.idle_frames:
            frame.set_colorkey(BLACK)
            # frame.set_colorkey(WHITE)
        for frame in self.running_frames:
            frame.set_colorkey(BLACK)

        self.jump_frames = [self.game.spritesheet_jump.get_image(0, 0, 238, 206),
                            self.game.spritesheet_jump.get_image(238, 0, 238, 206)]

        for frame in self.jump_frames:
            frame.set_colorkey(BLACK)

        # self.moving_frames_right = []
        # self.moving_frames_left = []

    def animate(self):
        current_time = pg.time.get_ticks()
        if self.vel.x != 0:
            self.running = True
        else:
            self.running = False

        if self.running and not self.jumping:
            if current_time - self.last_updated > 100:
                self.last_updated = current_time
                self.current_frame = (self.current_frame + 1) % len(self.running_frames)
                bottom_rect = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.running_frames[self.current_frame]
                else:
                    self.image = self.running_frames_left[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom_rect

        if not self.jumping and not self.running:
            if current_time - self.last_updated > 300:
                self.last_updated = current_time
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                # retain bottom rect position for each previous frame to readjust players feet (keep them above ground)
                # bottom_rect = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                # self.rect.bottom = bottom_rect

        if self.jumping or self.jump_boost:
            if current_time - self.last_updated > 100:
                self.last_updated = current_time
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames)
                # bottom_rect = self.rect.bottom
                self.image = self.jump_frames[self.current_frame]
                self.rect = self.image.get_rect()
                if self.vel.y == 0:
                    self.jump_boost = False

            # collision = pg.sprite.spritecollide(self, self.game.buffs, True)
            #
            # # if player is on a surface - jump (space bar)
            # for buff in collision:
            #
            #     if buff and not self.jump_boost:
            #         self.jump_boost = True
            #         self.vel.y = JUMP_POWER
            #         self.jump_boost = False

        # self.mask = pg.mask.from_surface(self.image)

    def update(self):
        """""
        Updates Game Loop 
        
        """""
        self.animate()
        # reset players acceleration; apply small increase in y-value for gravity simulation
        self.acc = vec(0, PLAYER_Y_MOMENTUM)

        # an arry of boolean values for key states; T = key is pressed down
        keys_pressed = pg.key.get_pressed()
        # increase acceleration when moving right
        if keys_pressed[K_f] or keys_pressed[K_RIGHT]:
            self.acc.x += PLAYER_ACC
        # decrease acceleration when moving left
        if keys_pressed[K_s] or keys_pressed[K_LEFT]:
            self.acc.x -= PLAYER_ACC

        # modify acceleration with friction constant to simulate more realistic changing of direction and prevent
        # "forever sliding"; apply friction to X axis ONLY (don't want friction influencing falling/gravity effect)
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # print(self.acc)


        # equations of motion
        self.vel += self.acc
        ## TO PREVENT COASTING EFFECT ##
        # if velocity gets below a certain below > set it to zero; needed for idle/running transition
        # without this, running animation would not stop because although friction was slowing the sprite down
        # the x velocity was not necessarily at 0 (i.e. could have been between 0-1) and thus, transition
        # from running to idle was delayed
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # prevent leaving screen
        if self.pos.x >= SCREEN_WIDTH:
            self.pos.x = SCREEN_WIDTH
        if self.pos.x <= 0:
            self.pos.x = 0

        # update players position
        self.rect.midbottom = self.pos

    def jump(self):

        # allow jumping ONLY if on a solid surface i.e. prevents double jumping/jumping when airborne.
        # increases player's y pos prior to collision check >>> immediately changes y pos back to what it was
        # so player doesn't end up inside an obstacle/platform; since nothing is being drawn within the following
        # three lines of code, the change in y will not be seen/noticed but the collision check will be made
        self.rect.y += 1
        collision = pg.sprite.spritecollide(self, self.game.obstacles, False)
        self.rect.y -= 1
        # if player is on a surface - jump (space bar)
        if collision and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = JUMP_POWER

    def jump_modify(self):
        """ Implements variable jump """

        if self.jumping:
            if self.vel.y < -2.5:
                self.vel.y = -2.5

    def check_collisions(self):
        pass


class Obstacles(pg.sprite.Sprite):
    """
    Handles environmental sprites e.g. platforms, various obstacles
    """

    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.obstacles
        super().__init__(self.groups)
        self.game = game
        # self.image = pg.Surface((width, height))
        images = [self.game.spritesheet_obstacles.get_image(0, 672, 380, 94),
                  self.game.spritesheet_obstacles.get_image(208, 1879, 201, 100),
                  ]  # grass platform self.game.spritesheet_obstacles.get_image(0, 288, 380, 94)

        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)

        # self.image = pg.transform.scale(self.image, ())
        # self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100) < JUMP_BOOST_SPAWN_PCT:
            Buffs(self.game, self)
        self.mask = pg.mask.from_surface(self.image)


class Clouds(pg.sprite.Sprite):

    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds

        super().__init__(self.groups)

        self.game = game
        self.image = random.choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.image = pg.transform.scale(self.image, (self.rect.width // 2, self.rect.height // 2))
        # scale = random.randrange(50, 101)/100
        # self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height * scale)))
        self.rect.x = random.randrange(SCREEN_WIDTH)  # self.rect.x)
        self.rect.y = random.randrange(-500, -50)

    def update(self):
        if self.rect.top > SCREEN_HEIGHT * 2:
            self.kill()


class Buffs(pg.sprite.Sprite):
    """
    Temporary stat boosts for player
    """

    def __init__(self, game, obstacle):
        self._layer = JUMP_POWERUP_LAYER
        self.groups = game.all_sprites, game.buffs
        super().__init__(self.groups)
        self.game = game
        self.image = pg.image.load("assets/img/jump_boost.png")
        self.image.set_colorkey(WHITE)
        self.obstacle = obstacle
        self.type = "jump"
        self.rect = self.image.get_rect()
        self.rect.centerx = self.obstacle.rect.centerx
        self.rect.bottom = self.obstacle.rect.top - 5

    def update(self):
        # offset from top of platforms
        self.rect.bottom = self.obstacle.rect.top  # - 3
        if not self.game.obstacles.has(self.obstacle):
            self.kill()
