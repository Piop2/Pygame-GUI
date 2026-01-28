import pygame
from pygame.math import Vector2

from core.input_manager import INPUT_MANAGER
from core.screen import Screen, Viewport
from event.handler import MouseHandler
from view import InputView
from view.button.button import ButtonView
from model import MouseButton

WINDOW_SIZE = (800, 800)
BUTTON_SIZE = (150, 45)

pygame.init()

window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Pygame GUI")
clock = pygame.Clock()

ui_screen = Screen(Viewport(WINDOW_SIZE))
ui_screen.style.background_color.update(31, 31, 31)

discord_box = ButtonView()
discord_box.transform.x = (WINDOW_SIZE[0] // 2) - (BUTTON_SIZE[0] // 2)
discord_box.transform.y = 40
discord_box.style.background_color.update(88, 101, 242)
discord_box.style.size = BUTTON_SIZE
discord_box.style.border_radius = 11
discord_box.add_handler((mouse_handler := MouseHandler()))


@mouse_handler.on_mouse_down
def on_mouse_down(_view: ButtonView, key: MouseButton, _pos: Vector2) -> bool:
    if key == MouseButton.LEFT:
        print("PUSH DOWN!")
        return True
    return False


@mouse_handler.on_mouse_up
def on_mouse_up(_view: ButtonView, key: MouseButton, _pos: Vector2) -> bool:
    if key == MouseButton.LEFT:
        print("PUSH UP!")
        return True
    return False

@mouse_handler.on_click
def on_click(_view: ButtonView, key: MouseButton) -> None:
    if key == MouseButton.LEFT:
        print("CLICK!")
    return


input_box = InputView()
input_box.transform.x = 150
input_box.transform.y = 150
input_box.style.size = (500, 45)
input_box.style.background_color.update(250, 250, 250)

ui_screen.add_node(discord_box)
ui_screen.add_node(input_box)

INPUT_MANAGER.activate_screen(ui_screen)

running = True
while running:
    delta = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        INPUT_MANAGER.dispatch(event)

    # Update
    ui_screen.update(delta)

    # Render
    ui_screen.render(window)
    pygame.display.flip()

pygame.quit()
