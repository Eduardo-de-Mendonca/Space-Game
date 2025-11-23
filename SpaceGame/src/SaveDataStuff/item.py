import pygame

class ItemKind:
    def __init__(self, rarity_multiplier, image):
        self.rarity_multiplier = rarity_multiplier
        self.image = image

    def to_item(self, difficulty_level):
        ap = difficulty_level*self.rarity_multiplier
        return Item(ap, self.image)

class Item:
    def __init__(self, attack_power, image):
        assert isinstance(image, pygame.Surface)

        self.attack_power = attack_power
        self.image = image