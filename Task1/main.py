import pygame as pg
import math
import os
import tkinter as tk

configuration = [85,
                 4000,
                 2000,
                 20000,
                 650,
                 1000]

PLANET_MASS = 6000000000000000000000000
PLANET_R = 6371000
g = 6.6720*PLANET_MASS/(PLANET_R**2)/10**11


FPS = 60
WIDTH = 800
HEIGHT = 600
FONT_SIZE = 36
FONT_COLOR = (255, 255, 255)


def clicked():
    global configuration
    for ind in range(len(configuration)):
        configuration[ind] = int(entry_list[ind].get())
    window_configuration.destroy()


window_configuration = tk.Tk()
window_configuration.title("Input configuration")
window_configuration.geometry('400x250')

tk.Label(window_configuration, text="Угол старта").grid(column=0, row=0)
tk.Label(window_configuration, text="Масса ракеты").grid(column=0, row=1)
tk.Label(window_configuration, text="Масса топлива").grid(column=0, row=2)
tk.Label(window_configuration, text="Скорость газа").grid(column=0, row=3)
tk.Label(window_configuration, text="Сгорость сгорания топлива").grid(column=0, row=4)
tk.Label(window_configuration, text="Машстаб (1 к )").grid(column=0, row=5)


entry_list = []
for i in range(6):
    entry_list.append(tk.Entry(window_configuration, width=10))

for i in range(6):
    entry_list[i].grid(column=1, row=i)

tk.Button(window_configuration, text="click", command=clicked).grid(column=2, row=2)
window_configuration.mainloop()

pg.font.init()
pg.init()

rocket_img = pg.image.load("rocket.png")
font = pg.font.Font(None, FONT_SIZE)
bg = pg.image.load("background.png")
scale = configuration[5]


class Point:
    def __init__(self, x, y):
        self.x = x // scale
        self.y = y // scale

    def blit(self, scr, biasX_, biasY_):
        pg.draw.circle(scr, (255, 255, 255), (int(self.x + biasX_), int(HEIGHT - self.y + biasY_)), 3)


class Rocket:
    def __init__(self, angle, rocketM, fuelM, gasSpeed, burningV, image, width, height):
        self.angle = angle
        self.variableAngle = angle
        self.rocketM = rocketM + fuelM
        self.fuelM = fuelM
        self.gasSpeed = gasSpeed
        self.burningV = burningV
        self.image = image
        self.width = width
        self.height = height
        self.x = 20 * scale
        self.y = (20 + self.height) * scale
        self.velocityX = 0
        self.velocityY = 0

    def changeGravity(self):
        global PLANET_MASS, PLANET_R, g
        g = 6.6720*PLANET_MASS/((PLANET_R + self.y)**2)/10**11

    def gravity(self):
        global FPS, g
        self.velocityY -= g / FPS

    def changeAngel(self):
        self.variableAngle = math.atan2(self.velocityY, self.velocityX) * 180 / math.pi

    def changeVelocity(self):
        global FPS
        self.velocityX += (self.burningV / FPS) * (self.gasSpeed * math.cos(self.angle * math.pi / 180)) / (
            self.rocketM - (self.burningV / FPS))
        self.velocityY += (self.burningV / FPS) * (self.gasSpeed * math.sin(self.angle * math.pi / 180)) / (
            self.rocketM - (self.burningV / FPS))

    def changeCoordinates(self):
        global FPS
        self.x += self.velocityX / FPS
        self.y += self.velocityY / FPS

    def blit(self, scr):
        rotate_img = pg.transform.rotate(self.image, -90 + self.variableAngle)
        rect = self.image.get_rect(topleft=(int(self.x // scale), int(HEIGHT - (self.y // scale))))
        scr.blit(rotate_img, rect)

    def checkCollision(self):
        if (self.y // scale) - self.height // 2 < 20:
            return "crash"
        if (self.y // scale) - self.height // 2 > HEIGHT:
            return "space"
        return "flight"


def pause(message):
    global run
    isPause = True
    while isPause:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                isPause = False
                run = False
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_SPACE:
                    isPause = False
                    run = False
        text = font.render(message, True, FONT_COLOR)
        screen.blit(text, (300, 100))
        pg.display.update()


screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

run = True

rocket = Rocket(configuration[0], configuration[1], configuration[2], configuration[3], configuration[4], rocket_img,
                rocket_img.get_width(),
                rocket_img.get_height())
trajectory = []
t = 0
second = 0
minute = 0
sec_str = "00"
min_str = "00"
timer = ""
s = font.render("00:00", True, FONT_COLOR)

while run:
    clock.tick(FPS)
    rocket.changeGravity()
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    # pg.draw.circle(screen, (255, 255 ,255), (int(rocket.x // scale), int(HEIGHT - (rocket.y // scale))), 3)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                run = False

    if rocket.fuelM > 0:
        rocket.fuelM -= rocket.burningV / FPS
        rocket.changeVelocity()

    if rocket.y > 30 + rocket.height:
        rocket.gravity()
    rocket.changeAngel()
    rocket.changeCoordinates()
    t = (t + 1) % FPS
    if t == 0:
        second += 1
        trajectory.append(Point(rocket.x, rocket.y))
        os.system('cls')
        print("g =", g
              , "\nvelocityY =", rocket.velocityY
              , "\nfuel mass ="
              , max(rocket.fuelM, 0)
              , "\nX ="
              , rocket.x
              , "\nY ="
              , rocket.y)
        if second % 60 == 0:
            minute += 1
            second = 0
            if minute < 10:
                min_str = "0" + str(minute)
            else:
                min_str = str(minute)

        if second < 10:
            sec_str = "0" + str(second)
        else:
            sec_str = str(second)

        timer = min_str + ":" + sec_str
        print("\n" + timer)
        s = font.render(timer, True, FONT_COLOR)

    for point in trajectory:
        point.blit(screen, rocket.width // 2, rocket.height // 2)
    rocket.blit(screen)

    state = rocket.checkCollision()
    if state == "crash":
        pause("Crash")
    if state == "space":
        pause("We are in SPACE!")
    screen.blit(s, (700, 100))
    pg.display.update()
