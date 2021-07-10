import pygame
# import random
# import os
from enum import Enum

from params import WIDTH, HEIGHT, FPS, CLOTH_COLOR, FRAME_COLOR, MAGIC_CONST, CARD_W, CARD_H
from items import Suit, Rank, Card
from elems import Deck, Pile, Stock, Table, Dealer


CARD_ACTIVE_COLOR = (173, 255, 47)
CARD_WRONG_COLOR = (139, 0, 0)
MESSAGE_BOX_COLOR = (152, 251, 152)

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

        def __init__(self, MAX_IN_ROW, id, name, type):            
            self.MAX_IN_ROW = MAX_IN_ROW
            self.id = id
            self.type = type
            self.joystick = self.Joystick()            
            self.wrong_choice = False
            
            self.width = MAGIC_CONST*CARD_W            
            self.height = 3/2*CARD_H
            self.thickness = 4   
            x = WIDTH/2 - self.width/2
            if id == 1:
                y = HEIGHT - self.height - self.thickness
            elif id == 2:
                y = self.thickness
            self.pos = [x, y]
            self.rect = pygame.Rect(x, y, self.width, self.height)
        
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
        
        def drawAllStuff(self, screen, cards, message_box):            
            pygame.draw.rect(screen, FRAME_COLOR, self.rect, self.thickness)  
                        
            pygame.draw.rect(screen, MESSAGE_BOX_COLOR, message_box.rect)
            pos  = message_box.pos            
            font = message_box.font
            text = font.render(message_box.name, True, (0,0,0))                
            screen.blit(text, (pos))            
            if not message_box.res == []:
                text = font.render(message_box.res, True, (0,0,0))                
                screen.blit(text, (pos[0], pos[1]+20))
                
            
            if self.joystick.active_card >= 0:                
                rect = cards[self.joystick.active_card].rect
                pygame.draw.rect(screen, CARD_ACTIVE_COLOR, rect, self.thickness)
            if self.joystick.chosen_card >= 0 and self.wrong_choice:                
                rect = cards[self.joystick.chosen_card].rect
                pygame.draw.rect(screen, CARD_WRONG_COLOR, rect, self.thickness)                

    class MessageBox:
        def __init__(self, x, y, name):
            self.font = pygame.font.Font('freesansbold.ttf', 20)
            self.pos = [x, y]
            self.name = name
            w, h = 2*CARD_W, CARD_H
            self.rect = pygame.Rect(x, y, w, h)
            self.res = []
        
        def setResult(self, res):
            if res == -1:
                self.res = "You are fool"
            elif res == 1:
                self.res = "You win"
            else:
                self.res = "Dead head"
                

    def __init__(self, id, name, type = "user"):
        pygame.sprite.LayeredUpdates.__init__(self)
        self.name = name        
        self.manager = self.DrawingManager(2*MAGIC_CONST, id, name, type)
        x, y = self.manager.pos[0] + self.manager.width + CARD_W/4, self.manager.pos[1]
        self.message_box = self.MessageBox(x, y, name)
        self.trump = []
        
    def setTrump(self, suit):
        self.trump = suit
        
    def draw(self, screen):
        pygame.sprite.LayeredUpdates.draw(self, screen)
        self.manager.drawAllStuff(screen, self.sprites(), self.message_box)        
        
    def addCard(self, card):        
        self.add(card)
        self.manager.joystick.num += 1
        self.updateCards()

    def updateCards(self):        
        get_weight = lambda card : ((card.suit == self.trump)*Rank.ACE.value + card.rank.value)
        cards = sorted(self.sprites(), key = get_weight)
        n = len(cards)
        self.manager.joystick.active_card = -1
        self.manager.joystick.chosen_card = -1
        l = 0
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
        FOOL      = 5
        
    class Word(Enum):
        BEATEN    = 1
        TAKE      = 2
        TAKE_AWAY = 3
        
    def __init__(self, id, name):
        PlayerHand.__init__(self, id, name)
        self.status = self.Status(id)        
        
    def sayWord(self):
        if self.status == self.Status.ATTACKER:
            return self.Word.BEATEN
        if self.status == self.Status.DEFENDING:
            return self.Word.TAKE
        if self.status == self.Status.ADDING:
            return self.Word.TAKE_AWAY
        return []


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
    # or DEFENDING player do not have cards
    if table.last_up == MAGIC_CONST or len(players['passive'].sprites()) == 0:
        return False
    # number of cards added by ADDING player on table equals 
    # number of TAKING player's cards => ADDING should say TAKE_AWAY
    if players['active'] == Player.Status.ADDING:
        if (table.last_down - table.last_up) == len(players['passive'].sprites()):
            return False
    return True

# TODO: rewrite this func that cards will 
#       distribute equally for players after the last fight
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

def isGameOver(stock, players):
    stock_vol = len(stock.sprites())
    p1_vol    = len(players['active'].sprites())
    p2_vol    = len(players['passive'].sprites())
    return stock_vol == 0 and (p1_vol == 0 or p2_vol == 0)

def howIsFool(players):
    p1_vol = len(players['active'].sprites())
    p2_vol = len(players['passive'].sprites())
    if p1_vol == 0 and p2_vol == 0:
        players['active'].message_box.setResult(0)
        players['passive'].message_box.setResult(0)
        return 'neither'
    elif p2_vol == 0:
        players['active'].message_box.setResult(-1)
        players['passive'].message_box.setResult(1)
        return players['active'].name
    elif p1_vol == 0:
        players['active'].message_box.setResult(1)
        players['passive'].message_box.setResult(-1)
        return players['passive'].name
    else:
        return 'neither yet'

def reactToWord(word, players, table, pile, stock):
    if word == Player.Word.BEATEN:
        table.getAllCards(pile)
        players['active'].status  = Player.Status.DEFENDING
        players['passive'].status = Player.Status.ATTACKER
        addFromStock(players, stock)
        swapRole(players)
    if word == Player.Word.TAKE:
        players['active'].status  = Player.Status.TAKING
        players['passive'].status = Player.Status.ADDING
        players['active'].updateCards()
        swapRole(players)
    if word == Player.Word.TAKE_AWAY:
        table.getAllCards(players['passive'], True)
        players['active'].status  = Player.Status.ATTACKER
        players['passive'].status = Player.Status.DEFENDING
        addFromStock(players, stock)    
    if isGameOver(stock, players):
        print(howIsFool(players))
        return GameStage.GAME_OVER
    else:
        return GameStage.PLAYING
        
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fool Game")


clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

deck = Deck()
deck.shuffle()
for c in deck.cards:
    all_sprites.add(c)
    
pl1 = Player(1, "Alexey V")
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
running = True
while running:
    clock.tick(FPS)
        
    for event in pygame.event.get():        
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n and game_stage == GameStage.START:
                Dealer.deal(deck, players, stock)
                trump = stock.showTrump()
                pl1.setTrump(trump)
                pl2.setTrump(trump)
                game_stage = GameStage.PLAYING        
            
            if players['active'] == pl1:
                if event.key == pygame.K_s:
                    reactToChoise(pl1, table, trump)
                            
                if event.key == pygame.K_a:
                    pl1.manager.joystick.shiftLeft()
                    
                if event.key == pygame.K_d:
                    pl1.manager.joystick.shiftRight()
                    
                if event.key == pygame.K_w:
                    if len(table.sprites()) > 0:
                        word = pl1.sayWord()                
                        game_stage = reactToWord(word, players, table, pile, stock)
            
            if players['active'] == pl2:
                if event.key == pygame.K_DOWN:
                    reactToChoise(pl2, table, trump)              
                                    
                if event.key == pygame.K_LEFT:
                    pl2.manager.joystick.shiftLeft()
                    
                if event.key == pygame.K_RIGHT:
                    pl2.manager.joystick.shiftRight()              

                if event.key == pygame.K_UP:
                    if len(table.sprites()) > 0:
                        word = pl2.sayWord()   
                        game_stage = reactToWord(word, players, table, pile, stock)

            # if event.key == pygame.K_x:            
            #     pl1.addCard(stock.getCard(True))
                
            # if event.key == pygame.K_c:
            #     pl2.addCard(stock.getCard(True))

    all_sprites.update()
    pl1.update()
    pl2.update()
    stock.update()
    table.update()
    pile.update()
    
    screen.fill(CLOTH_COLOR)
    
    all_sprites.draw(screen)    
    pl1.draw(screen)  
    pl2.draw(screen)  
    stock.draw(screen)
    table.draw(screen)
    pile.draw(screen)
    
    pygame.display.flip()
    

pygame.quit()