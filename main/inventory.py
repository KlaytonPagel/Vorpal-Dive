import json
import sys
import platform
import pygame
from sprites import HUDobject


class Inventory:
    def __init__(self, hud_group):
        self.inventory_slots = {}
        self.load_inventory()
        self.inventory_items = []
        self.inventory_group = pygame.sprite.Group()
        self.inventory_menu = None
        self.item_IDs = None
        self.get_item_ids()

        self.hud_group = hud_group

    def save_inventory(self):
        if sys.platform == 'emscripten':
            for slot, item in self.inventory_slots.items():
                platform.window.localStorage.setItem(str(slot), str(item))
        else:
            with open('json/player_inventory.json', 'w') as player_inventory:
                json.dump(self.inventory_slots, player_inventory)

    def load_inventory(self):
        with open('json/player_inventory.json') as player_inventory:
            self.inventory_slots = json.load(player_inventory)

        if sys.platform == 'emscripten':
            if platform.window.localStorage.getItem('equipped') == None:
                self.save_inventory()
            for slot, item in self.inventory_slots.items():
                stored_item = platform.window.localStorage.getItem(str(slot)).split(',')[2].split("'")[1]
                self.inventory_slots[slot] = [item[0], stored_item]

    def get_item_ids(self):
        with open('json/item_IDs.json') as item_id_file:
            self.item_IDs = json.load(item_id_file)

    def update_inventory(self):
        self.inventory_items.clear()

        # the inventory in its open state
        inventory_image = pygame.image.load('textures/32X32/HUD/inventory.png').convert_alpha()
        inventory = HUDobject((84, 50), inventory_image,
                              self.inventory_group, 'inventory')
        self.inventory_menu = inventory

        # load each occupied slot in the inventory
        for slot in self.inventory_slots:
            item = pygame.image.load(self.item_IDs[self.inventory_slots[slot][1]][0]).convert_alpha()
            item = pygame.transform.scale(item, (64, 64))
            item = HUDobject(self.inventory_slots[slot][0], item, self.inventory_group,
                             self.inventory_slots[slot][1], slot)
            self.inventory_items.append(item)

    # keep the players inventory open______________________________________________________________
    def display_inventory(self):
        screen = pygame.display.get_surface()
        screen.blit(self.inventory_menu.image, self.inventory_menu.rect.topleft)

        for item in self.inventory_items:
            screen.blit(item.image, item.rect.topleft)

    # creates the buttons to swap selected item with the equipped or secondary item________________
    def swap_item_buttons(self, position):
        equip_button_image = pygame.image.load('textures/32X32/HUD/equip_button.png')
        equip_button = HUDobject(position, equip_button_image, self.hud_group, 'equip')
        secondary_button_image = pygame.image.load('textures/32X32/HUD/secondary_button.png')
        HUDobject(equip_button.rect.bottomleft, secondary_button_image, self.hud_group, 'secondary')

    # swaps the players selected item with the equipped or secondary item__________________________
    def swap_items(self, option, item):

        if option.name == 'equip':
            self.inventory_slots[item.slot][1] = self.inventory_slots['equipped'][1]
            self.inventory_slots['equipped'][1] = item.name

        if option.name == 'secondary':
            self.inventory_slots[item.slot][1] = self.inventory_slots['secondary'][1]
            self.inventory_slots['secondary'][1] = item.name

        self.update_inventory()

    def add_item(self, item_id):
        for slot in self.inventory_slots:
            if self.inventory_slots[slot][1] == '0':
                self.inventory_slots[slot][1] = item_id
                return