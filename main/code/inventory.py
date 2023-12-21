import pygame
from sprites import HUD_object


class Inventory:
    def __init__(self):
        self.inventory_slots = {'1': ['occupied', (284, 54), 1], '2': ['occupied', (353, 54), 1],
                                '3': ['occupied', (422, 54), 1], '4': ['occupied', (491, 54), 1],
                                '5': ['occupied', (560, 54), 1], '6': ['occupied', (284, 123), 1],
                                '7': ['occupied', (353, 123), 1], '8': ['occupied', (422, 123), 1],
                                '9': ['occupied', (491, 123), 1], '10': ['occupied', (560, 123), 1],
                                '11': ['occupied', (284, 192), 1], '12': ['occupied', (353, 192), 1],
                                '13': ['occupied', (422, 192), 1], '14': ['occupied', (491, 192), 1],
                                '15': ['occupied', (560, 192), 1], '16': ['occupied', (284, 261), 1],
                                '17': ['occupied', (353, 261), 1], '18': ['occupied', (422, 261), 1],
                                '19': ['occupied', (491, 261), 1], '20': ['occupied', (560, 261), 1],
                                '21': ['occupied', (284, 330), 1], '22': ['occupied', (353, 330), 1],
                                '23': ['occupied', (422, 330), 1], '24': ['occupied', (491, 330), 1],
                                '25': ['occupied', (560, 330), 1], 'equipped': ['occupied', (87, 330), 1]
                                }
        self.inventory_items = []
        self.inventory_group = pygame.sprite.Group()
        self.inventory_menu = None

    def load_inventory(self):
        # the inventory in its open state
        inventory_image = pygame.image.load('../textures/32X32/HUD/inventory.png')
        inventory = HUD_object((84, 50), inventory_image,
                               self.inventory_group, 'inventory')
        self.inventory_menu = inventory

        # load each occupied slot in the inventory
        for slot in self.inventory_slots:
            if self.inventory_slots[slot][0] == 'occupied':
                item = pygame.image.load('../textures/32X32/HUD/wooden_sword_hud.png').convert()
                item = pygame.transform.scale(item, (64, 64))
                item = HUD_object(self.inventory_slots[slot][1], item, self.inventory_group)
                self.inventory_items.append(item)

    # keep the players inventory open______________________________________________________________
    def update_inventory(self):
        screen = pygame.display.get_surface()
        screen.blit(self.inventory_menu.image, self.inventory_menu.rect.topleft)

        for item in self.inventory_items:
            screen.blit(item.image, item.rect.topleft)
