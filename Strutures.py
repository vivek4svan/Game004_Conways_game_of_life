import pygame


class UnitObject(pygame.sprite.Sprite):

    def __init__(self, x, y, image_string):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_string)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
