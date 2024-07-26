import pgzrun
import time
import pygame
from pgzero.actor import Actor

WIDTH = 800
HEIGHT = 600

box_index = 0
settings_width = 451
settings_height = 451
settings_x = 70
settings_y = 76

key_pressed = None
icon_clicked = None

screen_clicked = False
password_done = False
digit_correct_list = [False, False, False, False, False, False, False, False]
on_home_page = False
setting_rect_open = False
windows_rect_open = False
backround_icon_open = False
settings_rect_full_screen = False

windows_rect = pygame.Rect(70, 200, 351, 312)

setting_icon = Actor("setting-icon", pos=(450, 570))

windows_icon = Actor("windows-icon", pos=(400, 572))

power_off = Actor("power-button", pos=(405, 500))

backround_icon = Actor("backround-setting", pos=(270, 150))

x_button_1 = Actor("x-button", pos=(500, 93))

x_button_2 = Actor("x-button", pos=(405, 210))

full_screen_icon_1 = Actor("full-screen-icon", pos=(465, 93))

full_screen_icon_2 = Actor("full-screen-icon", pos=(365, 210))

garden_icon = Actor("garden-background-icon", pos=(400, 250))

sky_icon = Actor("sky-background-icon", pos=(200, 250))

dungeon_icon = Actor("dungeon-background-icon", pos=(200, 400))

stage_icon = Actor("stage-background-icon", pos=(400, 400))

password_coding = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    "k": 11,
    "l": 12,
    "m": 13,
    "n": 14,
    "o": 15,
    "p": 16,
    "q": 17,
    "r": 18,
    "s": 19,
    "t": 20,
    "u": 21,
    "v": 22,
    "w": 23,
    "x": 24,
    "y": 25,
    "z": 26
}

def get_letter_from_number(digits, index_of_item):
    for letter, number in password_coding.items():
        if str(number) == digits[index_of_item]:
            return letter

def decode_password(digits):
    digit_1 = get_letter_from_number(digits, 0)
    digit_2 = get_letter_from_number(digits, 1)
    digit_3 = get_letter_from_number(digits, 2)
    digit_4 = get_letter_from_number(digits, 3)
    digit_5 = get_letter_from_number(digits, 4)
    digit_6 = get_letter_from_number(digits, 5)
    digit_7 = get_letter_from_number(digits, 6)
    digit_8 = get_letter_from_number(digits, 7)
    return [digit_1, digit_2, digit_3, digit_4, digit_5, digit_6, digit_7, digit_8]

def check_if_digits_are_coded(digits):
    try:
        for digit in digits:
            digit_int = int(digit)
        return True
    except ValueError:
        return False

def make_password_coded(digits):
    coded_digits_1_to_4 = [password_coding[digits[0]], password_coding[digits[1]], password_coding[digits[2]],password_coding[digits[3]]]
    coded_digits_5_to_8 = [password_coding[digits[4]], password_coding[digits[5]], password_coding[digits[6]], password_coding[digits[7]]]
    coded_digits = coded_digits_1_to_4 + coded_digits_5_to_8
    filename = r"C:\Projects\boy\pygame_game\computer-game\password.txt"
    with open(filename, "w") as file:
        for coded_digit in coded_digits:
            file.write(str(coded_digit) + " ")

def get_password_digits():
    filename = r"C:\Projects\boy\pygame_game\computer-game\password.txt"
    with open(filename, "r") as file:
        line = file.readline()
        password_digits_coded = line.split()
        coded = check_if_digits_are_coded(password_digits_coded)
        if coded:
            password_digits = decode_password(password_digits_coded)
            return password_digits
        else:
            password_digits = password_digits_coded
            make_password_coded(password_digits)
            return password_digits

def get_backround():
    global backround_image,blurred_backround_image
    filename = r"C:\Projects\boy\pygame_game\computer-game\background-setting.txt"
    with open(filename, "r") as file:
        line = file.readline()
        background_images = line.split()
        backround_image = background_images[0]
        blurred_backround_image = background_images[1]

def update_background(background):
    global backround_image,blurred_backround_image
    filename = r"C:\Projects\boy\pygame_game\computer-game\background-setting.txt"
    with open(filename, "w") as file:
        file.write(background + " " + background + "-blurred")

def get_answer_boxes():    
    global password_boxes_x
    password_boxes_x = [276, 306, 336, 366, 396, 426, 456, 486]
    password_boxes_1_to_4 = [pygame.Rect(276, 300, 43, 43), pygame.Rect(306, 300, 43, 43), pygame.Rect(336, 300, 43, 43), pygame.Rect(366, 300, 43, 43)]
    password_boxes_5_to_8 = [pygame.Rect(396, 300, 43, 43), pygame.Rect(426, 300, 43, 43), pygame.Rect(456, 300, 43, 43), pygame.Rect(486, 300, 43, 43)]
    password_boxes = password_boxes_1_to_4 + password_boxes_5_to_8
    return password_boxes

def draw_answer_boxes():
    global password_digits, password_boxes
    password_boxes = get_answer_boxes()
    for box in password_boxes:
        screen.draw.filled_rect(box, "sky blue")
    screen.draw.text("Password", color= "black", center = (WIDTH / 2, 250), fontsize = 60)

def get_x_of_circles():
    circle_1_x = password_boxes_x[0] + (43/2)
    circle_2_x = password_boxes_x[1] + (43/2)
    circle_3_x = password_boxes_x[2] + (43/2)
    circle_4_x = password_boxes_x[3] + (43/2)
    circle_5_x = password_boxes_x[4] + (43/2)
    circle_6_x = password_boxes_x[5] + (43/2)
    circle_7_x = password_boxes_x[6] + (43/2)
    circle_8_x = password_boxes_x[7] + (43/2)
    circles_x = [circle_1_x, circle_2_x, circle_3_x, circle_4_x, circle_5_x, circle_6_x, circle_7_x, circle_8_x]
    return circles_x

def draw_home_screen():
    screen.draw.filled_rect(pygame.Rect(0, 550, WIDTH, 50), (212,226,249))
    setting_icon.draw()
    windows_icon.draw()

def start_home_page():
    global settings_rect_full_screen
    draw_home_screen()
    if setting_rect_open:
        screen.draw.filled_rect(settings_rect, (239,244,249))
        x_button_1.draw()
        if not settings_rect_full_screen:
            full_screen_icon_1.draw()
        if backround_icon_open:
            backround_icon.draw()
        elif not backround_icon_open and icon_clicked == "background":
            screen.draw.text("Images", color= "black", center=(270, 170), fontsize = 30)
            sky_icon.draw()
            garden_icon.draw()
            dungeon_icon.draw()
            stage_icon.draw()
    if windows_rect_open:
        screen.draw.filled_rect(windows_rect, "gray")
        x_button_2.draw()
        power_off.draw()
        full_screen_icon_2.draw()

def rect_full_screen(rect):
    global settings_width, settings_height, settings_x, settings_y
    if rect == "settings":
        settings_width = WIDTH
        settings_height = HEIGHT - 50
        settings_x = 0
        settings_y = 0

def draw():
    global screen_clicked, box_index, key_pressed, password_boxes_x,digit_correct_list, on_home_page, password_done, setting_rect_open, backround_icon_open
    global settings_rect, settings_x, settings_y, settings_width, settings_height
    settings_rect = pygame.Rect(settings_x, settings_x, settings_width, settings_height)    
    get_backround()
    password_digits = get_password_digits()
    time_now = time.localtime()
    time_minutes = time.strftime("%M", time_now)
    time_hours = time.strftime("%I", time_now).lstrip("0")
    if screen_clicked == False:
        screen.blit(backround_image, (0, 0))
    if screen_clicked and not password_done:
        screen.blit(blurred_backround_image, (0, 0))
        draw_answer_boxes()
        circles_x = get_x_of_circles()
        circle_y = 300 + (43 / 2)
        for i in range(0, 8):
            if box_index > i:
                screen.draw.filled_circle((circles_x[i], circle_y), 10, "black")
    if screen_clicked == False and on_home_page == False:
        if backround_image == "stage":
            screen.draw.text(f"{time_hours}:{time_minutes}", color="dark gray", center=(WIDTH / 2, 50), fontsize=100)
        else:
            screen.draw.text(f"{time_hours}:{time_minutes}", color="black", center=(WIDTH / 2, 50), fontsize=100)
    if screen_clicked == True and key_pressed != None and password_done == False:
        screen.draw.textbox(key_pressed, password_boxes[box_index], color= "black")
        if box_index >= 0 and  box_index<=8 and key_pressed == password_digits[box_index]:
            digit_correct_list[box_index] = True   
        key_pressed = None
    if password_done == True and all(digit_correct_list):
        screen_clicked = False
        on_home_page = True
    elif password_done == True:
        screen_clicked = True
        password_done = False
        box_index = 0
        digit_correct_list = [False, False, False, False, False, False, False, False]
    if on_home_page:
        start_home_page()
                                
def on_key_up():
    global box_index, key_pressed, password_done, password_digits,digit_1

    if box_index < 7:
        box_index += 1
    else:
        password_done = True

def check_for_background_pressed(pos):
    global icon_clicked
    if sky_icon.collidepoint(pos) and icon_clicked == "background":
        update_background("sky")
        icon_clicked = None
    if garden_icon.collidepoint(pos) and icon_clicked == "background":
        update_background("garden")
        icon_clicked = None
    if dungeon_icon.collidepoint(pos) and icon_clicked == "background":
        update_background("dungeon")
        icon_clicked = None
    if stage_icon.collidepoint(pos) and icon_clicked == "background":
        update_background("stage")
        icon_clicked = None

def check_for_other_icons_pressed(pos):
    global on_home_page, setting_rect_open, backround_icon_open, backround_image, icon_clicked, windows_rect_open, settings_rect_full_screen
    if setting_icon.collidepoint(pos):
        setting_rect_open = True
    if windows_icon.collidepoint(pos):
        windows_rect_open = True
    if x_button_1.collidepoint(pos):
        setting_rect_open = False
        backround_icon_open = False
    if x_button_2.collidepoint(pos):
        windows_rect_open = False
    if power_off.collidepoint(pos) and windows_rect_open:
        pgzrun.sys.exit()
    if full_screen_icon_1.collidepoint(pos) and setting_rect_open:
        rect_full_screen("settings")
        settings_rect_full_screen = True
    if full_screen_icon_1.collidepoint(pos) and windows_rect_open:
        pass
    
def on_mouse_down(pos, button):
    global screen_clicked, on_home_page, setting_rect_open, backround_icon_open, backround_image, icon_clicked, windows_rect_open
    if on_home_page == False:
        screen_clicked = True
    elif on_home_page and button == mouse.LEFT:
        if backround_icon.collidepoint(pos) and backround_icon_open:
            backround_icon_open = False
            icon_clicked = "background"
        else:
            backround_icon_open = True
        check_for_background_pressed(pos)
        check_for_other_icons_pressed(pos)

def get_letter_pressed():
    if keyboard.q:
        return "q"
    if keyboard.w:
        return "w"
    if keyboard.e:
        return "e"
    if keyboard.r:
        return "r"
    if keyboard.t:
        return "t"
    if keyboard.y:
        return "y"
    if keyboard.u:
        return "u"
    if keyboard.i:
        return "i"
    if keyboard.o:
        return "o"
    if keyboard.p:
        return "p"
    if keyboard.a:
        return "a"
    if keyboard.s:
        return "s"
    if keyboard.d:
        return "d"
    if keyboard.f:
        return "f"
    if keyboard.g:
        return "g"
    if keyboard.h:
        return "h"
    if keyboard.j:
        return "j"
    if keyboard.k:
        return "k"
    if keyboard.l:
        return "l"
    if keyboard.z:
        return "z"
    if keyboard.x:
        return "x"
    if keyboard.c:
        return "c"
    if keyboard.v:
        return "v"
    if keyboard.b:
        return "b"
    if keyboard.n:
        return "n"
    if keyboard.m:
        return "m"

def update():
    global key_pressed, change_password_key_pressed
    if not password_done and screen_clicked:
        key_pressed = get_letter_pressed()

pgzrun.go()