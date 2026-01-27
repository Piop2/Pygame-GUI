import pygame

from core.input_manager import INPUT_MANAGER
from core.screen import Screen, Viewport
from view.button import ButtonView

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

ui_screen.add_node(discord_box)

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
