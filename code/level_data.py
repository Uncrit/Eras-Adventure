
""" loading in of the level map

setup_world() : called in level_data
    putting all the levels into one list

setup_level() : called in level_data
    reads a level out of a file and puts them in a list
"""

level_map = []

def setup_world(l1,l2,l3,l4,l5,l6,l7,l8,l9,l0,l10):
    global level_map
    i = 0
    on = True
    one = False
    two = False
    while on:
        if one == False and two == False:
            level_top = l1[i] + l2[i] + l3[i]
            level_map.append(level_top)
            i += 1
            if i == 32:
                i = 0
                one = True
        elif one == True and two == False:
            level_mid = l4[i] + l5[i] + l6[i]
            level_map.append(level_mid)
            i += 1
            if i == 32:
                i = 0
                two = True
        elif one == True and two == True:
            level_bot = l7[i] + l8[i] + l9[i]
            level_map.append(level_bot)
            i += 1
            if i == 32:
                i = 0
                one =False
        elif one == False and two == True:
            level_bot2 = l0[i] + l0[i] + l10[i]
            level_map.append(level_bot2)
            i += 1
            if i == 32:
                on = False

def setup_level(level_name):
    level_file = open("../editor/" + level_name + ".map","r")
    level = level_file.readlines()
    level_file.close()
    for i in range(0,32):
        level[i] = level[i].replace("\n", "")
    return level

level_1 = setup_level("l1")
level_2 = setup_level("l2")
level_3 = setup_level("l3")
level_4 = setup_level("l6")
level_5 = setup_level("l5")
level_6 = setup_level("l4")
level_7 = setup_level("l7")
level_8 = setup_level("l8")
level_9 = setup_level("l9")
level_0 = setup_level("l0")
level_10= setup_level("l10")

setup_world(
    level_1,level_2,level_3,
    level_4,level_5,level_6,
    level_7,level_8,level_9,
    level_0,level_10)