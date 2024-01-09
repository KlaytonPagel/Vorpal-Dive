import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, group, image, position):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
