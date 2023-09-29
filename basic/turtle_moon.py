import turtle as t
t.colormode(255)
t.setup(600,520)
t.screensize(bg="#121212")
t.hideturtle()
# t.tracer(3,50)
# t.speed(10)
def moveTo(pen, pos):
    pen.penup()
    pen.goto(pos)
    pen.pendown()

def rect(pen, width, height):
    for i in range(2):
        for i in (width, height):
            pen.fd(i)
            pen.right(90)

def dashed(pen, pos1, pos2, size = 3):
    moveTo(pen, pos1)
    x, y = pos1
    step = 100
    dx = (pos2[0] - pos1[0]) / step
    dy = (pos2[1] - pos1[1]) / step
    for i in range(step):
        x += dx
        y += dy
        if i % 2 == 1:
            pen.penup()
        else:
            pen.pendown()
        pen.goto(x, y)
import time
import math
def elliptical(pen, a, b, px = 0, py = 0):
    pen.penup()
    pen.goto(a * math.sin(math.radians(-180)) + px, b * math.cos(math.radians(-180)) + py)
    pen.pendown()
    for i in range(-180, 180 + 1, 5):
        x = a * math.sin(math.radians(i)) + px
        y = b * math.cos(math.radians(i)) + py
        pen.goto(x, y)

def polygon(pen, step, sidelength):
    if step < 3:
        return
    angle = 360 / step
    for i in range(step):
        pen.left(angle)
        pen.fd(sidelength)

# ============
pen = t.Pen()
pen.speed(10)
pen.color("white")
pen.hideturtle()
dashed(pen, (-300,-100), (300,-50)) # 地平线

# == moon ==
pen.color(214,236,240)
pen.fillcolor(247,238,203)
pen.begin_fill()

elliptical(pen, 90 / 2, 89 / 2, -200, 200)
pen.end_fill()

# == star ==
import random
for i in range(1,15):
    pen.up()
    pen.goto(random.randint(-300,300), random.randint(120,300))
    pen.down()
    pen.dot(random.randint(2,3))

# == building ==
for i in range(5):
    w = random.randint(25,30)#30
    x = random.randint(80,230)#250
    y = random.randint(-110,-70)#-70
    moveTo(pen, (x,y))
    polygon(pen, 3, w)
    moveTo(pen, (x -(w - 5),y))
    rect(pen, w - 10, w - 10)

# t.tracer(True)

t.mainloop()