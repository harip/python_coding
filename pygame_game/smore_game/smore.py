import pgzrun
import pygame
from PIL import Image, ImageSequence
from pgzero.actor import Actor
from pgzero.rect import Rect
from pgzero.clock import clock
from pygame.rect import Rect

# image = Image.open('path_to_your_image.jpg')

# # Resize the image
# new_size = (250, 250)  # Specify the new size
# resized_image = image.resize(new_size, Image.LANCZOS)

# # Convert the resized image to a Pygame surface
# image_bytes = resized_image.tobytes()
# mode = resized_image.mode
# size = resized_image.size

# # Initialize Pygame
# pygame.init()

# # Create a Pygame surface from the image bytes
# actor_image = pygame.image.fromstring(image_bytes, size, mode)

# # Create an actor (sprite) with the image
# actor = pygame.sprite.Sprite()
# actor.image = actor_image
# actor.rect = actor_image.get_rect()
WIDTH = 800
HEIGHT = 600

TIME_TO_ROAST = 5 # seconds
TIME_TO_BURN = 10 # seconds

items = {
    "stick": {
        "image": Actor("stick", (700, 300)),
        "is_clicked": False,
        "disappear": False
    },
    "marshmellow": {
        "image": Actor("marshmellow", (33.5, 37.5)),
        "is_clicked": False,
        "disappear": False
    },
}

smore_items = {
    "cracker": {
            "image": Actor("cracker", (WIDTH / 2, HEIGHT / 2)),
        }
    }

rects = {
    "marshmellow_stick_rect": Rect(items["stick"]["image"].x - 40, items["stick"]["image"].y - 170, 75, 100),
    "fire_rect": Rect(300, 80, 200, 350),
    "arrow_rect": Rect(WIDTH / 2 + 300, 0, 80, 80)
}

frames = [frame.copy() for frame in ImageSequence.Iterator(Image.open(r'boy/pygame_game/smore_game/images/fire.gif'))]

arrow_clicked = False
time_roasted = 0
current_frame = 0
frame_delay = 0.1
last_update_time = 0

def draw_fire_gif(pos):
    frame_image = frames[current_frame]
    size = frame_image.size
    data = frame_image.convert("RGBA").tobytes()
    frame_surface = pygame.image.fromstring(data, size, "RGBA")
    screen.blit(frame_surface, pos)

def update_marshmellow(stick_image, marshmellow_image):
    marshmellow_image.image = "marshmellow" if stick_image.image == "stick" else stick_image.image.removeprefix("stick_")
    marshmellow_image.pos = WIDTH / 2, HEIGHT / 2
    marshmellow_image.angle = 90

def draw():
    global time_roasted, current_frame, last_update_time
    if not arrow_clicked:
        screen.fill("black")
        draw_fire_gif((WIDTH / 2 - Actor("fire").width / 2, 50))
        items["stick"]["image"].angle = 55
        screen.draw.text("Press the arrow to continue", fontsize=60, topleft=(WIDTH / 2 - 300, 10), color=(255, 255, 255))
        screen.draw.text("->", fontsize=80, topleft=(WIDTH / 2 + 300, 0), color="purple")
        for item in items.values():
            if not item["disappear"]:
                item["image"].draw()
        if time_roasted >= TIME_TO_ROAST and time_roasted < TIME_TO_BURN:
            items["stick"]["image"].image = "stick_roasted_marshmellow"
        elif time_roasted == TIME_TO_BURN:
            items["stick"]["image"].image = "stick_burnt_marshmellow"
        screen.draw.rect(rects["marshmellow_stick_rect"], "white")
    else:
        screen.fill("white")
        update_marshmellow(items["stick"]["image"], items["marshmellow"]["image"])
        for item in smore_items.values():
            item["image"].draw()
        items["marshmellow"]["image"].draw()
        
def update():
    global current_frame, last_update_time
    if pygame.time.get_ticks() - last_update_time > frame_delay * 1000 and not arrow_clicked:
        current_frame = (current_frame + 1) % len(frames)
        last_update_time = pygame.time.get_ticks()

def on_mouse_down(pos):
    global arrow_clicked
    if not arrow_clicked:
        if items["marshmellow"]["image"].collidepoint(pos) and not items["marshmellow"]["disappear"]:
            items["marshmellow"]["is_clicked"] = True
        if items["stick"]["image"].collidepoint(pos) and items["marshmellow"]["disappear"]:
            items["stick"]["is_clicked"] = True
        if rects["arrow_rect"].collidepoint(pos):
            arrow_clicked = True
    else:
        pass

def on_mouse_up():
    if not arrow_clicked:
        if not items["marshmellow"]["disappear"]:
            items["marshmellow"]["is_clicked"] = False
        if not items["stick"]["disappear"] and items["marshmellow"]["disappear"]:
            items["stick"]["is_clicked"] = False

def on_mouse_move(pos):
    global rects
    if not arrow_clicked:
        if not items["marshmellow"]["image"].colliderect(rects["marshmellow_stick_rect"]):
            if items["marshmellow"]["is_clicked"] and pos[0] > 0 and pos[0] < WIDTH and pos[1] > 0 and pos[1] < HEIGHT:
                items["marshmellow"]["image"].pos = pos
        else:
            items["marshmellow"]["disappear"] = True
            if items["stick"]["image"].image == "stick":
                items["stick"]["image"].image = "stick_marshmellow"
        if items["stick"]["is_clicked"] and pos[0] > 0 and pos[0] < WIDTH and pos[1] > 0 and pos[1] < HEIGHT:
            if items["marshmellow"]["disappear"]:
                items["stick"]["image"].pos = pos

def update_time_roasted():
    global time_roasted, rects
    if not arrow_clicked:
        if time_roasted < TIME_TO_ROAST and items["stick"]["image"].colliderect(rects["fire_rect"]) and items["stick"]["image"].image == "stick_marshmellow":
            time_roasted += 1
        if time_roasted >= TIME_TO_ROAST and time_roasted < TIME_TO_BURN and items["stick"]["image"].colliderect(rects["fire_rect"]) and items["stick"]["image"].image == "stick_roasted_marshmellow":
            time_roasted += 1

clock.schedule_interval(update_time_roasted, 1)

pgzrun.go()