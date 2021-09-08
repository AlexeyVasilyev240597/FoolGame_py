
WIDTH = 960
HEIGHT = 640
FPS = 30

CARD_W  = 80
CARD_H  = 116
BADGE_S = 40

COLOR_CLOTH       = (46, 139, 87)
COLOR_FRAME       = (128, 128, 0)
COLOR_CARD_ACTIVE = (173, 255, 47)
COLOR_CARD_WRONG  = (139, 0, 0)
COLOR_MESSAGE_BOX = (255, 255, 255)
# MESSAGE_BOX_COLOR = (152, 251, 152)

# "magic" for Fool game
MAGIC_CONST = 6

POS_STOCK   = [0, HEIGHT/2 - CARD_H/2]
POS_PILE    = [WIDTH - CARD_W, HEIGHT/2 - CARD_H/2]
POS_TABLE   = [WIDTH/2 - MAGIC_CONST*CARD_W/2, 13/8*CARD_H]
PLAYER_W    = MAGIC_CONST*CARD_W
PLAYER_H    = 3/2*CARD_H
POS_PLAYERS = {'down': [WIDTH/2 - PLAYER_W /2, HEIGHT - PLAYER_H], 
               'up':   [WIDTH/2 - PLAYER_W /2, 0]}

FLAG_DEBUG = False