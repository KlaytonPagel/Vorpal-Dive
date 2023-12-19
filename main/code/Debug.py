import pygame
from config import *


def debug(data):
    display = pygame.display.get_surface()
    font = pygame.font.Font(None, 50)
    image = font.render(data, True, (255, 255, 255))
    display.blit(image, (screen_width - 70, 20))
