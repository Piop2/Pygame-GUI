import pygame

from core.screen import Screen, Viewport
from view.button import ButtonView

WINDOW_SIZE = (800, 800)
BUTTON_SIZE = (150, 60)

pygame.init()

window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Pygame GUI")
clock = pygame.Clock()

ui_screen = Screen(Viewport(WINDOW_SIZE))
ui_screen.style.background_color.update(31, 31, 31)

discord_box = ButtonView()
discord_box.transform.x = (WINDOW_SIZE[0] // 2) - (BUTTON_SIZE[0] // 2)
discord_box.transform.y = (WINDOW_SIZE[1] // 2) - (BUTTON_SIZE[1] // 2)
discord_box.style.background_color.update(88, 101, 242)
discord_box.style.width = BUTTON_SIZE[0]
discord_box.style.height = BUTTON_SIZE[1]
discord_box.style.border_radius = 12

ui_screen.add_node(discord_box)

running = True
while running:
    delta = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        ui_screen.dispatch_event(event)

    ui_screen.update(delta)

    ui_screen.render(window)
    pygame.display.flip()

pygame.quit()
