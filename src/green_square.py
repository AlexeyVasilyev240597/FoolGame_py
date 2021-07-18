import pygame

from params import WIDTH, HEIGHT, FPS, COLOR_CLOTH 
from elems  import Deck, Pile, Stock, Table, Dealer
from player import Status
from user   import User
from ai     import NikitaA
from rules  import GameStage, swapRole, isChoiceCorrect, canCardBeThrown, reactToWord

# TODO: write log file contained all moves of players and their cards on hands
# TODO: customize 'new game' by press 'N' key after 'game over'
     
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
pl2 = NikitaA(2)
players = {'active': pl1, 'passive': pl2}
stock     = Stock()
pile      = Pile()
table     = Table()

game_stage = GameStage.START
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
            
            if players['active'] == pl1 and game_stage == GameStage.PLAYING:
                if event.key == pygame.K_a:
                    pl1.joystick.shiftLeft()
                    
                if event.key == pygame.K_d:
                    pl1.joystick.shiftRight()
                    
                if event.key == pygame.K_s:
                    pl1.chooseCard()
                    card = pl1.showChosenCard()
                    if not card == []:
                        right_card = isChoiceCorrect(pl1.status, table, card, trump)
                        # print(right_card)
                        enough_space = canCardBeThrown(pl1.status, table, pl2.vol())
                        # print(enough_space)
                        move_correct = right_card and enough_space
                        if move_correct:
                            card = pl1.getCard()
                            table.addCard(card, pl1.status == Status.DEFENDING)
                            if not pl1.status == Status.ADDING:
                                swapRole(players)
                        else:
                            pl1.wrong_choice = True
                        start_ticks = pygame.time.get_ticks()
                        pl2.mess_box.setText('')

                if event.key == pygame.K_w:
                    if table.vol() > 0:
                        word = pl1.sayWord()                
                        game_stage = reactToWord(word, players, table, pile, stock)
                        if game_stage == GameStage.PLAYING:
                            start_ticks = pygame.time.get_ticks()
                            pl2.mess_box.setText('')
    
    # if pl2 is AI
    if players['active'] == pl2 and game_stage == GameStage.PLAYING:
        sec = (pygame.time.get_ticks()-start_ticks)/1000
        if sec > 1:
            mv = pl2.move(table, stock.vol(), pl1.vol())
            if 'card' in mv:
                card = mv.get('card')
                # print(card)
                table.addCard(card, pl2.status == Status.DEFENDING)
                if not pl2.status == Status.ADDING:
                    swapRole(players)
                start_ticks = pygame.time.get_ticks()
                pl1.mess_box.setText('')
            if 'word' in mv:
                word = mv.get('word')
                # print(word.name)
                game_stage = reactToWord(word, players, table, pile, stock)
                if game_stage == GameStage.PLAYING:
                    start_ticks = pygame.time.get_ticks()
                    pl1.mess_box.setText('')

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