#################################
### Game and Player Constants ###
#################################

## GAME SETTINGS ##
GAME_TITLE = "Blobby Blobson"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 200
FPS = 60
FONT = 'corbel'  # to check available: pg.font.get_fonts()
HIGHSCORE_FILE = "Highest_Score.txt"
CLOUD_LAYER = 0
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
JUMP_POWERUP_LAYER = 1
ENEMY_LAYER = 2

####################################
## Enemies ##
ENEMY_ONE_SPAWN_FREQ = 2000

#################################
## ITEM SPAWNS ##
JUMP_BOOST = -60
JUMP_BOOST_SPAWN_PCT = 10

#################################
## COLOUR PALETTE ##
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
DARK_RED = (60, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
SKY_DARKER_BLUE = (90, 128, 255)
DEEP_SKY_BLUE = (0, 162, 232)
LIGHT_BLUE = (146, 244, 255)
#################################
## PLAYER SETTINGS ##
PLAYER_ACC = 2
# PLAYER_VELO = 0
PLAYER_FRICTION = -0.20
JUMP_POWER = -25
PLAYER_Y_MOMENTUM = 0.7  # gravity effect
TIME_AIRBORNE = 0

#################################
## SPRITESHEETS ##
SPRITESHEET_PLAYER_IDLE = "red_blob_idle_two.png"
SPRITESHEET_PLAYER_IDLE_FRAMES = ["2x_02.png", "2x_03.png", "2x_04.png", "2x_05.png", "2x_06.png", "2x_07.png",
                                  "2x_08.png", "2x_09.png", "2x_10.png", "2x_11.png", "2x_12.png"]

SPRITESHEET_PLAYER_RUN = "red_blob_run.png"
SPRITESHEET_PLAYER_RUN_FRAMES = ["red_blob_run_03.png", "red_blob_run_04.png", "red_blob_run_05.png",
                                 "red_blob_run_06.png", "red_blob_run_07.png", "red_blob_run_08.png",
                                 "red_blob_run_09.png", "red_blob_run_10.png", "red_blob_run_11.png",
                                 "red_blob_run_12.png", "red_blob_run_16.png", "red_blob_run_17.png",
                                 "red_blob_run_18.png", "red_blob_run_19.png", "red_blob_run_20.png",
                                 "red_blob_run_21.png", "red_blob_run_22.png", "red_blob_run_23.png",
                                 ]

SPRITESHEET_PLAYER_JUMP = "red_blob_jump_SS.png"
SPRITESHEET_PLAYER_JUMP_FRAMES = ["red_blob_jump_03.png", "red_blob_jump_05.png"]

SPRITESHEET_OBSTACLES = "spritesheet_jumper.png"


ENEMY_T1 = "angry_head.png"
ENEMY_T1_RED = "angry_head.png"
ENEMY_T1_PINK = "angry_head_2.png"
## OLD PLATFORM LIST  - WIDTH, HEIGHT VARS ARGUMENTS ##
# PLATFORM_LIST = [(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),
#                  (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT * 3 / 4, 100, 20),
#                  (125, SCREEN_HEIGHT - 350, 100, 20), (350, 200, 100, 20),
#                  (170, 100, 50, 20)]
PLATFORM_LIST = [(0, SCREEN_HEIGHT - 50), (100, 20), (125, SCREEN_HEIGHT - 350), (350, 200),
                 (170, 100)]
