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