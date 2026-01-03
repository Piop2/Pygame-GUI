import pygame
from pygame import Surface

from core.canvas_item import CanvasItem
from view.image import ImageView

pygame.init()

window: Surface = pygame.display.set_mode((800, 800))
pygame.display.set_caption("GUI TEST")
clock = pygame.Clock()


root_node = CanvasItem()
image1 = ImageView(pygame.image.load("asset/spk.jpg"))

image2 = ImageView(pygame.image.load("asset/spk2.jpg"))
image2.x = 50
image2.y = 50

root_node.add_node(image1)
image1.add_node(image2)

running = True
while running:
    delta: int = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # render
    window.fill("white")
    root_node.render(window)

    pygame.display.flip()

pygame.quit()
