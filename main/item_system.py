import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, group, image, position, item_id, name):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.item_id = item_id
        self.name = name
