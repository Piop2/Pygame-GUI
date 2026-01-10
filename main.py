import pygame

from core.screen import Screen, Viewport
from model.align import ContentAlign
from model.event import MouseButton
from view.button import ButtonView
from view.text import TextView
from view.shape import RectView
from view.input import InputView

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


@discord_box.on_mouse_down
def on_mouse_down(key: MouseButton, _):
    if key == MouseButton.LEFT:
        print("CLICK!!!")
        return True

    return False


text_box = TextView()
text_box.font = "asset/gg sans Medium.ttf"
text_box.font_size = 18
text_box.font_color.update(255, 255, 255)
text_box.value = "Hello, World!"
text_box.style.size = BUTTON_SIZE
text_box.content_align = ContentAlign.MIDDLE_CENTER

rect = RectView()
rect.transform.x = 10
rect.transform.y = 10
rect.style.background_color.update(255, 0, 0)
rect.style.width = 100
rect.style.height = 100

input_box = InputView()
input_box.transform.x = 150
input_box.transform.y = 150
input_box.style.size = (500, 45)
input_box.style.background_color.update(250, 250, 250)


ui_screen.add_node(discord_box)
ui_screen.add_node(rect)
ui_screen.add_node(input_box)
discord_box.add_node(text_box)

running = True
while running:
    delta = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        ui_screen.dispatch_event(event)

    # Update
    ui_screen.update(delta)

    # Render
    ui_screen.render(window)
    pygame.display.flip()

pygame.quit()
