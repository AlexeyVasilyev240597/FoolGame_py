import pygame
from enum import Enum

from params import WIDTH, HEIGHT, FPS, MAGIC_CONST
from params import COLOR_CLOTH 
from elems import Deck, Pile, Stock, Table, Dealer
from player import Status, Word
from user import User


# ----------------- Fool methods -----------------
def swapRole(players):
    players['active'], players['passive'] = players['passive'], players['active']

def isChoiceCorrect(status, table, card, trump):
    if table.vol() == 0:
        return True
    if status == Status.ATTACKER or status == Status.ADDING:
        for c in table.cards.sprites():
            if card.rank == c.rank:
                return True
        return False
    if status == Status.DEFENDING:
        last = table.cards.sprites()[-1]
        return last.suit == card.suit and last.rank < card.rank or not last.suit == card.suit and card.suit == trump

# TODO: rewrite with switch by all Status values 
# and check last case because there is BUG!
#def canCardBeThrown(players, table):
def canCardBeThrown(status, table, rival_vol):
    # 6*2 = 12 cards on table => ATTACKER should say BEATEN
    # or DEFENDING player do not have cards
    if table.last_down == MAGIC_CONST:
        return False
    # number of cards added by ADDING player on table equals 
    # number of TAKING player's cards => ADDING should say TAKE_AWAY
    if status == Status.ADDING:
        if (table.last_down - table.last_up) == rival_vol:
            return False
    return True

def addFromStock(players, stock):
    pv = {'active': players['active'].vol(), 'passive': players['passive'].vol()}
    dv = {'active': 0, 'passive': 0}
    s  = stock.vol()
    while s > 0 and (pv['active'] < MAGIC_CONST or pv['passive'] < MAGIC_CONST):
        if pv['active'] < pv['passive']:
            dv['active'] += 1
            pv['active'] += 1
        else:
            dv['passive'] += 1
            pv['passive'] += 1
        s -= 1    
    for role in players:       
        for i in range(dv[role]):
            players[role].addCard(stock.getCard(True))

def reactToChoise(player, table, trump):
    player.chooseCard()
    card = player.showChosenCard()
    if not card == []:
        
        right_card = isChoiceCorrect(player.status, table, card, trump)
        print(right_card)
        enough_space = canCardBeThrown(players['active'].status, table, players['passive'].vol())
        print(enough_space)
        move_correct = right_card and enough_space
        if move_correct:
            card = player.getCard()
            table.addCard(card, player.status == Status.DEFENDING)
            if not players['active'].status == Status.ADDING:
                swapRole(players)
        else:
            player.wrong_choice = True

def isGameOver(stock, players):
    stock_vol = stock.vol()
    p1_vol    = players['active'].vol()
    p2_vol    = players['passive'].vol()
    return stock_vol == 0 and (p1_vol == 0 or p2_vol == 0)

def howIsFool(players):
    p1_vol    = players['active'].vol()
    p2_vol    = players['passive'].vol()
    if p1_vol == 0 and p2_vol == 0:
        players['active'].box.setResult(0)
        players['passive'].box.setResult(0)
        return 'neither'
    elif p2_vol == 0:
        players['active'].box.setResult(-1)
        players['passive'].box.setResult(1)
        return players['active'].name
    elif p1_vol == 0:
        players['active'].box.setResult(1)
        players['passive'].box.setResult(-1)
        return players['passive'].name
    else:
        return 'neither yet'

def reactToWord(word, players, table, pile, stock):
    if word == Word.BEATEN:
        table.getAllCards(pile)
        players['active'].status  = Status.DEFENDING
        players['passive'].status = Status.ATTACKER
        addFromStock(players, stock)
        swapRole(players)
    if word == Word.TAKE:
        players['active'].status  = Status.TAKING
        players['passive'].status = Status.ADDING
        swapRole(players)
    if word == Word.TAKE_AWAY:
        table.getAllCards(players['passive'], True)
        players['active'].status  = Status.ATTACKER
        players['passive'].status = Status.DEFENDING
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
    
pl1 = User("Alexey V", 1)
pl2 = User("Robert", 2)
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
                trump = Dealer.deal(deck, players, stock)
                game_stage = GameStage.PLAYING        
            
            if players['active'] == pl1:
                if event.key == pygame.K_s:
                    reactToChoise(pl1, table, trump)

                if event.key == pygame.K_a:
                    pl1.joystick.shiftLeft()
                    
                if event.key == pygame.K_d:
                    pl1.joystick.shiftRight()
                    
                if event.key == pygame.K_w:
                    if table.vol() > 0:
                        word = pl1.sayWord()                
                        game_stage = reactToWord(word, players, table, pile, stock)
            
            if players['active'] == pl2:
                if event.key == pygame.K_DOWN:
                    reactToChoise(pl2, table, trump)              
                                    
                if event.key == pygame.K_LEFT:
                    pl2.joystick.shiftLeft()
                    
                if event.key == pygame.K_RIGHT:
                    pl2.joystick.shiftRight()              

                if event.key == pygame.K_UP:
                    if table.vol() > 0:
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
    
    screen.fill(COLOR_CLOTH)
    
    all_sprites.draw(screen)    
    pl1.draw(screen)  
    pl2.draw(screen)  
    stock.draw(screen)
    table.draw(screen)
    pile.draw(screen)
    
    pygame.display.flip()
    

pygame.quit()