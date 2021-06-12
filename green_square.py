import pygame
import random
import os
from enum import Enum

WIDTH = 960
HEIGHT = 640
FPS = 30

CLOTH_COLOR = (46, 139, 87)
FRAME_COLOR = (128, 128, 0)
CARD_ACTIVE_COLOR = (173, 255, 47)
CARD_WRONG_COLOR = (139, 0, 0)

# "magic" for Fool game
MAGIC_CONST = 6

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'pic')

ranks = range(6, 15)
suits = ['S', 'H', 'D', 'C']

class Card(pygame.sprite.Sprite):        
    def __init__(self, suit, rank):
        pygame.sprite.Sprite.__init__(self)
        self.suit = suit
        self.rank = rank        
        face = pygame.image.load(os.path.join(img_folder, suit, str(rank) + '.png')).convert()
        back = pygame.image.load(os.path.join(img_folder, 'back.png')).convert()        
        self.sides = [back, face]
        self.image = self.sides[0]
        self.rect = self.image.get_rect()
        self.target_pos = [self.rect.x, self.rect.y]        
        
    def __repr__(self):
        return repr((self.suit, self.rank))
        
    def turnOver(self):
        self.sides[0], self.sides[1] = self.sides[1], self.sides[0]
        self.image = self.sides[0]
        
    # moving funcs
    def setTargetPos(self, pos):
        self.target_pos = pos

    def update(self):
        if not (self.target_pos[0] == self.rect.x and self.target_pos[1] == self.rect.y):
            N = [self.target_pos[0] - self.rect.x, self.target_pos[1] - self.rect.y]
            L = abs(N[0]) + abs(N[1])
            # number of pixels per shot
            dl = min(10, L)
            dx = round(N[0]/L*dl)
            dy =   int(N[1]/L*dl)
            self.rect.x += dx
            self.rect.y += dy
            
class Deck:
    def __init__(self):
        self.cards = []
        for s in suits:
            for r in ranks:
                c = Card(s, r)
                self.cards.append(c)
                
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, cards_set, num = 1, by_open = False):
        if len(self.cards) >= num:
            for n in range(num):
                c = self.cards.pop(0)
                if by_open:
                    c.turnOver()
                cards_set.addCard(c)
    
    def putToPile(self, pile):
        while len(self.cards) > 0:
            pile.addCard(self.cards.pop())

class PlayerHand(pygame.sprite.LayeredUpdates):
    class DrawingManager:
        class Joystick:
            def __init__(self):
                self.active_card = -1
                self.chosen_card = -1
                self.num = 0
                
            def shiftRight(self):
                if not self.chosen_card == -1:
                    self.chosen_card = -1
                self.active_card += 1            
                if self.active_card == self.num:
                    self.active_card = self.num-1
                
            def shiftLeft(self):
                if not self.chosen_card == -1:
                    self.chosen_card = -1
                self.active_card -= 1
                if self.active_card < 0:
                    self.active_card = 0
                    
            def chooseCard(self):
                if self.active_card >= 0:
                    self.chosen_card = self.active_card


        def __init__(self, MAX_IN_ROW, id, type):            
            self.MAX_IN_ROW = MAX_IN_ROW
            self.id = id
            self.type = type
            self.joystick = self.Joystick()
            self.wrong_choice = False
            
            self.width = MAGIC_CONST*CARD_W            
            self.height = 3/2*CARD_H
            self.thickness = 4   
            if id == 1:
                self.pos = [WIDTH/2 - self.width/2, HEIGHT-self.height-self.thickness]
            elif id == 2:
                self.pos = [WIDTH/2 - self.width/2, self.thickness]
            self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
            
        
        def getCardPos(self, i, n):
            if n == 1:
                x = 0
                y = 0
            else:
                # index of row
                ir = i // self.MAX_IN_ROW
                y = int(CARD_H*ir/4)
                            
                # row number
                rn = n // self.MAX_IN_ROW
                if ir == rn:
                    # number of elems in row
                    nr = n % self.MAX_IN_ROW
                else:
                    nr = self.MAX_IN_ROW
                
                # index of column
                ic = i % self.MAX_IN_ROW
                if nr < MAGIC_CONST:
                    x = ic*CARD_W
                else: # squeeze mode
                    x = int((MAGIC_CONST-1)*CARD_W*ic/(nr-1))
            pos = [self.pos[0] + x, self.pos[1] + y]
            return pos
        
        def drawAllStuff(self, screen, cards):            
            pygame.draw.rect(screen, FRAME_COLOR, self.rect, self.thickness)        
            if self.joystick.active_card >= 0:                
                rect = cards[self.joystick.active_card].rect
                pygame.draw.rect(screen, CARD_ACTIVE_COLOR, rect, self.thickness)
            if self.joystick.chosen_card >= 0 and self.wrong_choice:                
                rect = cards[self.joystick.chosen_card].rect
                pygame.draw.rect(screen, CARD_WRONG_COLOR, rect, self.thickness)

    def __init__(self, id, type = "user"):
        pygame.sprite.LayeredUpdates.__init__(self)        
        self.manager = self.DrawingManager(2*MAGIC_CONST, id, type)   
        
    def draw(self, screen):
        pygame.sprite.LayeredUpdates.draw(self, screen)
        self.manager.drawAllStuff(screen, self.sprites())
        
    def addCard(self, card):        
        self.add(card)
        self.manager.joystick.num += 1
        self.updateCards()

    def updateCards(self):        
        cards = sorted(self.sprites(), key=lambda card: card.rank)
        n = len(cards)
        self.manager.joystick.active_card = -1
        self.manager.joystick.chosen_card = -1
        l = 0
        print("user #" + str(self.manager.id))
        for c in cards:
            self.change_layer(c, l)
            l += 1
            pos = self.manager.getCardPos(self.get_layer_of_sprite(c), n)
            c.setTargetPos(pos)            

    def showChosenCard(self):
        # chosen card index
        cci = self.manager.joystick.chosen_card
        if cci >= 0:
            card = self.sprites()[cci]
        else:
            card = []
        return card
            
    def getChosenCard(self):
        card = self.showChosenCard()
        if not card == []:
            self.remove(card)
            self.manager.joystick.num -= 1
            self.updateCards()
        return card

class Player(PlayerHand):
    class Status(Enum):
        ATTACKER  = 1
        DEFENDING = 2
        ADDING    = 3
        TAKING    = 4
        
    class Word(Enum):
        BEATEN    = 1
        TAKE      = 2
        TAKE_AWAY = 3
        
    def __init__(self, id, name):
        PlayerHand.__init__(self, id)
        self.name = name
        self.status = self.Status(id)
        
    def sayWord(self):
        if self.status == self.Status.ATTACKER:
            return self.Word.BEATEN
        if self.status == self.Status.DEFENDING:
            return self.Word.TAKE
        if self.status == self.Status.ADDING:
            return self.Word.TAKE_AWAY
        return []


class Pile(pygame.sprite.LayeredUpdates):
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)
        self.pos = [WIDTH - CARD_W, HEIGHT/2 - CARD_H/2]
    
    def addCard(self, card):
        self.add(card)        
        card.setTargetPos(self.pos)        
        self.change_layer(card, 1)

    def putToDeck(self, deck):
        while len(self.sprites()) > 0:
            card = self.get_top_sprite()
            deck.cards.append(card)
            card.setTargetPos([0, 0])
            self.remove(card)
    

class Stock(pygame.sprite.LayeredUpdates):
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)  
        self.pos = [0, HEIGHT/2 - CARD_H/2]
        
    def addCard(self, card):
        self.add(card)
        card.setTargetPos(self.pos)        
        self.change_layer(card, 1)
    
    def showTrump(self):        
        last_card = self.get_top_sprite()
        last_card.turnOver()
        last_card.setTargetPos([self.pos[0], self.pos[1] + CARD_W/4])
        last_card.image = pygame.transform.rotate(last_card.image, -90)
        self.change_layer(last_card, 0)
        return last_card.suit
    
    def getCard(self, by_open = False):
        n = len(self.sprites())        
        if n > 0:
            card = self.get_top_sprite()              
            if n == 1:
                card.image = pygame.transform.rotate(card.image, 90)
                self.move_to_front(card)
            else:
                card.turnOver()
            if not by_open:
                card.turnOver()
            self.remove(card)
        else:
            card = []
        return card
        
class Table(pygame.sprite.LayeredUpdates):
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)  
        self.pos = [WIDTH/2 -  MAGIC_CONST*CARD_W/2, 13/8*CARD_H]
        self.last_down = 0
        self.last_up   = 0
        
    def addCard(self, card, atop):
        if atop:
            l = 2*(self.last_up + 1)
            self.last_up += 1
        else:
            l = 2*self.last_down + 1
            self.last_down += 1
        
        self.add(card, layer = l)
        pos = self.getCardPos(l)
        card.setTargetPos(pos)
        
    def getCardPos(self, layer):
        i    = layer - 1
        atop = layer % 2
        x = (i %  MAGIC_CONST) * CARD_W        
        y = (i // MAGIC_CONST) * CARD_H
        if atop:
            x += CARD_W / 4
            y += CARD_H / 4
        x += self.pos[0]
        y += self.pos[1]
        pos = [x, y]
        return pos
        
    def getAllCards(self, cards_set, by_open = False):
        while len(self.sprites()) > 0:
            card = self.get_top_sprite()
            if not by_open:
                card.turnOver()
            cards_set.addCard(card)
            self.remove(card)
        self.last_down = 0
        self.last_up   = 0

# ----------------- Fool methods -----------------
def swapRole(players):
    players['active'], players['passive'] = players['passive'], players['active']

def isChoiceCorrect(status, table, card, trump):
    if len(table.sprites()) == 0:
        return True
    if status == Player.Status.ATTACKER or status == Player.Status.ADDING:
        for c in table.sprites():
            if card.rank == c.rank:
                return True
        return False
    if status == Player.Status.DEFENDING:
        last = table.sprites()[-1]
        return card.suit == last.suit and card.rank > last.rank or card.suit == trump

def canCardBeThrown(players, table):
    # 6*2 = 12 cards on table => ATTACKER should say BEATEN
    if table.last_up == MAGIC_CONST:
        return False
    # number of cards added by ADDING player on table equals 
    # number of TAKING player's cards => ADDING should say TAKE_AWAY
    if (table.last_down - table.last_up) == len(players['passive'].sprites()):
        return False
    return True

# TODO: rewrite this func that cards will 
#       distribute equally for players after the last fight
# useful to check game over
def addFromStock(players, stock):
    for role in players:
        ns = len(stock.sprites())    
        if ns > 0:            
            n = len(players[role].sprites())
            if n < MAGIC_CONST:
                for i in range(min(MAGIC_CONST-n, ns)):
                    players[role].addCard(stock.getCard(True))
        
def reactToChoise(player, table, trump):
    player.manager.joystick.chooseCard()
    card = player.showChosenCard()
    if not card == []:
        move_correct = isChoiceCorrect(player.status, table, card, trump) and canCardBeThrown(players, table)
        if move_correct:
            card = player.getChosenCard()
            table.addCard(card, player.status == Player.Status.DEFENDING)
            if not players['active'].status == Player.Status.ADDING:
                swapRole(players)
        else:
            player.manager.wrong_choice = True

def reactToWord(word, players, table, pile):
    if word == Player.Word.BEATEN:
        table.getAllCards(pile)
        players['active'].status =  Player.Status.DEFENDING
        players['passive'].status =  Player.Status.ATTACKER
        addFromStock(players, stock)
        swapRole(players)
    if word == Player.Word.TAKE:
        players['active'].status = Player.Status.TAKING
        players['passive'].status = Player.Status.ADDING
        players['active'].updateCards()
        swapRole(players)
    if word == Player.Word.TAKE_AWAY:
        table.getAllCards(players['passive'], True)
        players['active'].status =  Player.Status.ATTACKER
        players['passive'].status =  Player.Status.DEFENDING
        addFromStock(players, stock)        
        
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fool Game")

(CARD_W, CARD_H) = Card('S', 6).image.get_rect().size

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

deck = Deck()
# deck.shuffle()
for c in deck.cards:
    all_sprites.add(c)
    
pl1 = Player(1, "Alexey")
pl2 = Player(2, "Robert")
players = {'active': pl1, 'passive': pl2}
stock     = Stock()
pile      = Pile()
table     = Table()

class GameStage(Enum):
    START     = 1
    PLAYING   = 2
    GAME_OVER = 3
    
game_stage = GameStage(1)

while not game_stage == GameStage.GAME_OVER:
    clock.tick(FPS)
        
    for event in pygame.event.get():        
        # check for closing window
        if event.type == pygame.QUIT:
            game_stage = GameStage.GAME_OVER
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n and game_stage == GameStage.START:
                deck.deal(pl1, MAGIC_CONST, True)
                deck.deal(pl2, MAGIC_CONST, True)
                deck.putToPile(stock)
                trump = stock.showTrump()
                game_stage = GameStage.PLAYING        
            
            if players['active'] == pl1:
                if event.key == pygame.K_SPACE:
                    reactToChoise(pl1, table, trump)
                            
                if event.key == pygame.K_a:
                    pl1.manager.joystick.shiftLeft()
                    
                if event.key == pygame.K_d:
                    pl1.manager.joystick.shiftRight()
                    
                if event.key == pygame.K_s:
                    if len(table.sprites()) > 0:
                        word = pl1.sayWord()                
                        reactToWord(word, players, table, pile)
            
            if players['active'] == pl2:
                if event.key == pygame.K_RETURN:
                    reactToChoise(pl2, table, trump)              
                                    
                if event.key == pygame.K_LEFT:
                    pl2.manager.joystick.shiftLeft()
                    
                if event.key == pygame.K_RIGHT:
                    pl2.manager.joystick.shiftRight()              

                if event.key == pygame.K_UP:
                    if len(table.sprites()) > 0:
                        word = pl2.sayWord()   
                        reactToWord(word, players, table, pile)

            if event.key == pygame.K_x:            
                pl1.addCard(stock.getCard(True))
                
            if event.key == pygame.K_c:
                pl2.addCard(stock.getCard(True))

    # stock_vol = len(stock.sprites())
    # u1_vol    = len(pl1.sprites())
    # u2_vol    = len(pl2.sprites())
    # if game_stage == "playing" and stock_vol == 0 and (u1_vol == 0 or u2_vol == 0):
    #     game_over = True

    all_sprites.update()
    pl1.update()
    pl2.update()
    stock.update()
    table.update()
    
    screen.fill(CLOTH_COLOR)
    
    all_sprites.draw(screen)    
    pl1.draw(screen)  
    pl2.draw(screen)  
    stock.draw(screen)
    table.draw(screen)
    
    pygame.display.flip()
    

pygame.quit()