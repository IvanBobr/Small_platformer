import os
import pygame
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def check_in(pos_in, polygon):
    # здесь должен быть код проверки, находится ли точка внутри многоугольника
    pass


def check_walls(pos, pol):
    pass
    # здесь должен быть код проверки, пересекает ли атака стену


class Weapon:
    def __init__(self, name, image, attack_image, polygon, damage):
        self.name = name
        self.image = load_image(image)
        self.attack_image = attack_image
        self.polygon = polygon
        self.damage = damage

    def transpose_pol(self, pol, orientation):
        # по умолчанию ориентация вниз для зрителя, т.е. вверх по координатам, 1- вниз, 2 - влево, 3 - вверх, 4 - вправо
        if orientation == 2:
            for i in range(pol):
                pol[i] = (pol[i][1], pol[i][0])
        if orientation == 3:
            for i in range(pol):
                pol[i] = (pol[i][0], -pol[i][1])
        if orientation == 4:
            for i in range(pol):
                pol[i] = (-pol[i][1], pol[i][0])
        return pol

    def damage(self, position, orientation, enemies):
        pol = self.transpose_pol(self.polygon, orientation)
        for i in enemies:
            if check_in(position, pol):
                if check_walls(position, pol):
                    i.hit(self.damage)
