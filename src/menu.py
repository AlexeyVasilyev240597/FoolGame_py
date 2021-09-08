__all__ = ['main']

import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

from typing import Optional

from params import FPS, COLOR_CLOTH, HEIGHT, WIDTH
from ai     import AIGenerator
from fool   import play_fool_game

names = AIGenerator.getNames()
ai_name   = [names[0]]

clock: Optional['pygame.time.Clock'] = None
main_menu: Optional['pygame_menu.Menu'] = None
surface: Optional['pygame.Surface'] = None

def start_f(user_name):
    play_fool_game(user_name.get_value(), ai_name[0])

def change_name(value, name) -> None:
    ai_name[0] = name    

def main_background() -> None:
    global surface
    surface.fill(COLOR_CLOTH)


def main(test: bool = False) -> None:
    global clock
    global main_menu
    global surface

    surface = create_example_window('Fool Game: Menu', (WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    main_theme = pygame_menu.themes.THEME_GREEN

    main_menu = pygame_menu.Menu(
        height=HEIGHT*0.6,
        theme=main_theme,
        title='Menu',
        width=WIDTH*0.6)

    user_name = main_menu.add.text_input('Your name: ', default='Alexey_V', maxchar=15) 
    sel_arg = []
    for n in names:
        sel_arg.append((n, n))
    main_menu.add.selector('Select AI ',
                            sel_arg,
                            onchange=change_name,
                            selector_id='select_ai_name')
    main_menu.add.button('Start', start_f, user_name)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
