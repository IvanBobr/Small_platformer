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
    # fullname = os.path.join('data', name)
    fullname = name
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


clock = pygame.time.Clock()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
tile_width = tile_height = 50
FPS = 50
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
corob_group = pygame.sprite.Group()
group_pyls = pygame.sprite.Group()
trap_group = pygame.sprite.Group()
group_rewards = pygame.sprite.Group()

pygame.init()
player_image = load_image('data/heroes/boss2.jpg', colorkey=-1)
tile_images = {
    'wall': load_image('data/floors_walls/wall.jpg'),
    'empty': load_image('data/floors_walls/floor2.jpg'),
    'traps': load_image('data/floors_walls/trap_1_lava.jpg'),
    'enemy': load_image('data/heroes/slime.jpg'),
    'trap': load_image('data/floors_walls/trap_1_lava.jpg'),
    'chest': load_image('data/bafs&dops/reward.jpg'),
    'key': load_image('data/bafs&dops/key_for_chest.jpg')
}


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
            elif level[y][x] == '!':
                Trap('trap', x, y)  # ловушка
            elif level[y][x] == '?':
                Tile('empty', x, y)  # замедление
            elif level[y][x] == '%':
                Tile('empty', x, y)  # ускорение
            elif level[y][x] == '*':
                Chest('chest', x, y)  # сундук
            elif level[y][x] == '$':
                Tile('empty', x, y)  # босс
            elif level[y][x] == '+':
                Tile('empty', x, y)  # враг
            elif level[y][x] == '0':
                Tile('moneys', x, y)  # монетки
            elif level[y][x] == '_':
                Key('key', x, y)  # баф
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


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


class Trap(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(trap_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[image], (50, 50))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == "wall":
            super().__init__(tiles_group, all_sprites, corob_group)
        else:
            super().__init__(tiles_group, all_sprites)

        self.image = pygame.transform.scale(tile_images[tile_type], (50, 50))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(player_image, (40, 40))
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 5)
        self.health = 3
        self.napr = "up"
        self.x_napr = "right"

    def update_(self, coords):
        self.rect = self.rect.move(coords[0], coords[1])
        if pygame.sprite.spritecollideany(self, corob_group):
            self.rect = self.rect.move(-coords[0], -coords[1])
        if pygame.sprite.spritecollideany(self, enemy_group):
            self.update_health(-1)
            for i in enemy_group:
                if pygame.sprite.collide_mask(self, i):
                    i.update_health(-1)
        if pygame.sprite.spritecollideany(self, trap_group):
            self.update_health(-1)
        x_add = coords[0]
        y_add = coords[1]
        if x_add == 50:
            if self.x_napr != "right":
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.napr = "right"
                self.x_napr = "right"
        elif x_add == -50:
            if self.x_napr != "left":
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.napr = "left"
                self.x_napr = "left"
        elif y_add == 50:
            self.napr = "up"
        else:
            self.napr = "down"
        if pygame.sprite.spritecollideany(self, group_rewards):
            self.kill()
            # КОНЕЦ ИГРЫ
            pygame.quit()

    def update_health(self, wht):
        if type(wht) == int:
            self.health += wht
        if self.health > 3:
            self.health = 3
        elif self.health <= 0:
            self.kill()
            # КОНЕЦ ИГРЫ
            pygame.quit()

    def return_napr(self):
        return self.napr

    def return_coords(self):
        return [self.rect.x, self.rect.y]

    def return_xp(self):
        return self.health


class Key(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(group_keys, all_sprites)
        self.image = pygame.transform.scale(tile_images[image], (50, 50))
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


class Chest(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(group_rewards, all_sprites)
        self.image = pygame.transform.scale(tile_images[image], (50, 50))
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y + 5)


class Pyla(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_pyl, napr):
        super().__init__(group_pyls, all_sprites)
        self.image = pygame.transform.scale(load_image(image_pyl), (30, 30))
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.x = pos_x
        self.y = pos_y
        self.napr = napr

    def update_(self):
        if self.napr == "left":
            self.add = [-50, 0]
        elif self.napr == "right":
            self.add = [50, 0]
        elif self.napr == "down":
            self.add = [0, -50]
        else:
            self.add = [0, 50]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.image = pygame.transform.scale(player_image, (30, 30))
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.wht = 3

    def update_(self, coords):
        self.rect = self.rect.move(coords[0], coords[1])
        if pygame.sprite.spritecollideany(self, corob_group):
            self.rect = self.rect.move(-coords[0], -coords[1])

    def update_health(self, wht):
        if type(wht) == int:
            self.health += wht
        if self.health > 10:
            self.health = 10
        elif self.health <= 0:
            self.kill()
            # ВРАГ УБИТ


def load_level(filename):
    filename = "data/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        print(level_map)
        max_width = max(map(len, level_map))

        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except Exception:
        print(f"Ошибка. Файла {filename} не существует в памяти")


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    name_lvl = input("Введите название файла с уровнем\n")
    intro_text = ["                                          ТАЙНЫ ПОДЗЕМЕЛИЙ", "",
                  "Управление:",
                  "   W, A, S, D - движение",
                  "   R - атака",
                  "   Esc - меню"]
    screen = pygame.display.set_mode((720, 439))
    fon = pygame.transform.scale(load_image('data/floors_walls/fon.jpg'), (720, 439))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
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
                screen = pygame.display.set_mode(size)
                return player
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


hp_1, hp_2, hp_3 = pygame.transform.scale(load_image("data/heroes/cerd.jpg", -1), (40, 40)), pygame.transform.scale(
    load_image("data/heroes/cerd.jpg", -1), (40, 40)), pygame.transform.scale(load_image("data/heroes/cerd.jpg", -1),
                                                                              (40, 40))
hp_1r = hp_1.get_rect(center=(370, 20))
hp_2r = hp_2.get_rect(center=(420, 20))
hp_3r = hp_3.get_rect(center=(470, 20))

sp_images_hp = [hp_3, hp_2, hp_1]
sp_rects_hp = [hp_3r, hp_2r, hp_1r]

camera = Camera()
player = start_screen()
fps = 100
running = True
pygameSurface = pygame.transform.scale(pygame.image.load('data/floors_walls/EEhho.png'), (500, 500))
pygameSurface.set_alpha(190)
sp_pyls = []
while running:
    # внутри игрового цикла ещё один цикл
    # приема и обработки сообщений
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.update_([0, -50])
            elif event.key == pygame.K_LEFT:
                player.update_([-50, 0])
            elif event.key == pygame.K_RIGHT:
                player.update_([50, 0])
            elif event.key == pygame.K_DOWN:
                player.update_([0, 50])
            elif event.key == pygame.K_SPACE:
                # происходит выстрел пулей
                x, y = player.return_coords()[0], player.return_coords()[1]
                sp_pyls.append(
                    Pyla(x, y, "data/bafs&dops/pyl.jpg", player.return_napr()))
    camera.update(player)
    screen.fill((0, 0, 0))
    # screen.blit(picture, (0, 0), (0, 0, 500, 500))
    # screen.blit(world, pygame.rect.Rect(0, 0, 500, 500))
    # обновляем положение всех спрайтов
    for i in sp_pyls:
        i.update_()
    for sprite in all_sprites:
        camera.apply(sprite)
    # отрисовка и изменение свойств объектов
    # screen.fill((139, 0, 0))
    all_sprites.update()
    all_sprites.draw(screen)
    # player_group.draw(screen)
    # обновление экрана
    # clock.tick(fps)
    screen.blit(pygameSurface, pygameSurface.get_rect(center=screen.get_rect().center))
    for i in range(player.return_xp()):
        screen.blit(sp_images_hp[i], sp_rects_hp[i])
    player_group.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
