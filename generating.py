import pygame
import sys
import os
import random


def load_and_processingLVL(name_lvl=None, kol_enemies=5, spawn_boss=False, percent_spawnTRAPS=50, coins=5,
                           add_bafs=True):
    if not name_lvl:
        print("Error - no name of file with lvl")
    else:
        with open(name_lvl, "r") as read_file:
            with open("data/levels/tmp.txt", "w") as output_file:
                strings = read_file.read()
                output_file.truncate(0)
                while kol_enemies or coins:
                    for i in strings:
                        skip_string = random.randint(0, 100) % 10
                        i_copy = i
                        if not skip_string:
                            output_file.write(i_copy)
                        else:
                            for symb in range(len(i)):
                                spawn_random = random.randint(0, 100)
                                if i[symb] == "." and spawn_random % 3 == 0 and kol_enemies:
                                    i_copy = i[:symb] + "+" + i[symb + 1:]
                                    kol_enemies -= 1
                                elif spawn_random % 17 == 0 and coins:
                                    i_copy = i[:symb] + "0" + i[symb + 1:]
                                    coins -= 1
                                on_this_string = random.randint(0, 100)
                                if on_this_string % 13 != 0:
                                    break
                            output_file.write(i_copy)


def generate_lvls_v2(name_lvl_udate):
    # задаем необходимые переменные
    name_lvl_udate_2 = name_lvl_udate.split("/")[-1]
    if "_0" in name_lvl_udate_2 and "1_0" not in name_lvl_udate_2 and "0_0" not in name_lvl_udate_2:  # боссы спавнятся каждые 10 лвлов, уровень с боссом имеет тип 2_0, 3_0
        spawn_boss = True
    else:
        spawn_boss = False
    with open(name_lvl_udate, "r") as input_file:
        lvl_startV = input_file.readlines()
    kol_enemies = len(lvl_startV) // 2
    kol_coins = (int(name_lvl_udate_2.split(".")[0].split("_")[0])
                 + int(name_lvl_udate_2.split(".")[0].split("_")[1])) \
                // int(name_lvl_udate_2.split(".")[0].split("_")[0])
    kol_traps = int(name_lvl_udate_2.split(".")[0].split("_")[0]) * 2

    spawn_str_enemy = kol_enemies // len(lvl_startV) + 1
    spawn_str_coins = kol_enemies // len(lvl_startV) + 1

    '''
    spawn_boss      - переменная спавна боссов, спавнятся каждые 10 лвлов тип 2_0, 3_0, 4_0 и т.д.
    lvl_startV      - поступающий на вход лвл в виде списка строк из файла
    kol_enemies     - количество врагов, зависит от размера лвла
    kol_coins       - количество монеток, зависит от уровня
    kol_traps       - количество ловушек, зависит от уровня
    spawn_str_enemy - количество врагов на одной строчке
    spawn_str_coins - колиество монеток на одной строчке
    '''

    with open("tmp.txt", "w") as work_file:
        work_file.truncate(0)
        for strings_lvl in lvl_startV:
            copy_spawn1 = spawn_str_enemy
            copy_spawn2 = spawn_str_coins
            string_refacting = strings_lvl
            for kl in range(len(strings_lvl)):
                if string_refacting[kl] == "." and copy_spawn1 >= 1 and kol_enemies >= 1:
                    copy_spawn1 -= 1
                    kol_enemies -= 1
                    string_refacting = string_refacting[:kl] + "+" + string_refacting[kl + 1:]
                if string_refacting[kl] == "." and copy_spawn2 >= 1 and kol_coins >= 1:
                    copy_spawn2 -= 1
                    kol_coins -= 1
                    string_refacting = string_refacting[:kl] + "!" + string_refacting[kl + 1:]
                if spawn_boss and string_refacting[kl] == ".":
                    spawn_boss = False
                    string_refacting = string_refacting[:kl] + "$" + string_refacting[kl + 1:]
            work_file.write(string_refacting)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print("Cannot load image:", fullname)
        print(str(message))
        raise SystemExit(message)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# clock = pygame.time.Clock()
# size = WIDTH, HEIGHT = 500, 500
# screen = pygame.display.set_mode(size)
# tile_width = tile_height = 50
# FPS = 50
# player = None
#
# all_sprites = pygame.sprite.Group()
# tiles_group = pygame.sprite.Group()
# player_group = pygame.sprite.Group()
# corob_group = pygame.sprite.Group()
#
# pygame.init()
# tile_images = {
#     'wall': load_image('box.png'),
#     'empty': load_image('grass.png')
# }
# player_image = load_image('mario.png', colorkey=-1)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == "wall":
            super().__init__(tiles_group, all_sprites, corob_group)
        else:
            super().__init__(tiles_group, all_sprites)

        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

        self


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update_(self, coords):
        self.rect = self.rect.move(coords[0], coords[1])
        if pygame.sprite.spritecollideany(self, corob_group):
            self.rect = self.rect.move(-coords[0], -coords[1])


def load_level(filename):
    filename = "data/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))

        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except Exception:
        print(f"Ошибка. Файла {filename} не существует в памяти")


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    name_lvl = input("Введите название файла с уровнем\n")
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                player, level_x, level_y = generate_level(load_level(name_lvl))
                return player
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


# camera = Camera()
# player = start_screen()
#
# fps = 100
# running = True
# while running:
#     # внутри игрового цикла ещё один цикл
#     # приема и обработки сообщений
#     for event in pygame.event.get():
#         # при закрытии окна
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP:
#                 player.update_([0, -50])
#             elif event.key == pygame.K_LEFT:
#                 player.update_([-50, 0])
#             elif event.key == pygame.K_RIGHT:
#                 player.update_([50, 0])
#             elif event.key == pygame.K_DOWN:
#                 player.update_([0, 50])
#     camera.update(player);
#     # обновляем положение всех спрайтов
#     for sprite in all_sprites:
#         camera.apply(sprite)
#     # отрисовка и изменение свойств объектов
#     screen.fill((0, 0, 0))
#     all_sprites.update()
#     all_sprites.draw(screen)
#     player_group.draw(screen)
#     # обновление экрана
#     clock.tick(fps)
#     pygame.display.flip()
# pygame.quit()
generate_lvls_v2("data/levels/1_1.txt")
