from OpenGL.GL import *
from OpenGL.GLUT import *
from random import randint as rdn
import numpy as np
import time
import random


inputTaken = False
inp = None
fireAt = None

# Human position
h_x0 = rdn(-900, -100)
h_y0 = -150
h_x1 = rdn(100, 980)
h_y1 = -150

# Initial square coordinates
d_x0 = -1100   # left to right ashar moving point
d_y0 = 550

count=0

def draw_points(x, y, defult):
    glPointSize(defult)
    glBegin(GL_POINTS)
    glVertex2f(x ,y)
    glEnd()

def convert_and_draw_pixel(x, y, zone, default):
    if zone == 0:
        draw_points(x, y, default)
    if zone == 1:
        draw_points(y, x, default)
    if zone == 2:
        draw_points(-y, x, default)
    if zone == 3:
        draw_points(-x, y, default)
    if zone == 4:
        draw_points(-x, -y, default)
    if zone == 5:
        draw_points(-y, -x, default)
    if zone == 6:
        draw_points(y, -x, default)
    if zone == 7:
        draw_points(x, -y, default)


def draw_line_at_zone_0(x1, y1, x2, y2, zone, default):
    dx = x2 - x1
    dy = y2 - y1
    d = 2* dy - dx
    del_E = 2 * dy
    del_NE = 2 * (dy - dx)
    x = x1
    y = y1
    convert_and_draw_pixel(x, y, zone, default)
    while x < x2:
        if d < 0:
            d += del_E
            x += 1
        else:
            d += del_NE
            x += 1
            y += 1
        convert_and_draw_pixel(x, y, zone, default)


def draw_line(x1, y1, x2, y2, default=2):
    dx = x2 - x1
    dy = y2 - y1
    if (abs(dx) > abs(dy)):
        if dx >= 0:  # zone 0 or 7
            if dy >= 0:  # zone 0
                z = 0
                draw_line_at_zone_0(x1, y1, x2, y2, z, default)
            else:
                z = 7
                draw_line_at_zone_0(x1, -y1, x2, -y2, z, default)
        else:  # zone 3 or 4
            if dy >= 0:
                z = 3
                draw_line_at_zone_0(-x1, y1, -x2, y2, z, default)
            else:
                z = 4
                draw_line_at_zone_0(-x1, -y1, -x2, -y2, z, default)
    else:  # zone 1 or 2 or 5 or 6
        if dx >= 0:  # zone 1 or 6
            if dy >= 0:
                z = 1
                draw_line_at_zone_0(y1, x1, y2, x2, z, default)
            else:
                z = 6
                draw_line_at_zone_0(-y1, x1, -y2, x2, z, default)
        else:  # zone 2 or 5
            if dy >= 0:
                z = 2
                draw_line_at_zone_0(y1, -x1, y2, -x2, z, default)
            else:
                z = 5
                draw_line_at_zone_0(-y1, -x1, -y2, -x2, z, default)


def draw_8_way_points(x, y, x0, y0, full, default):
    draw_points(x + x0, y + y0, default)
    draw_points(y + x0, x + y0, default)
    draw_points(-y + x0, x + y0, default)
    draw_points(-x + x0, y + y0, default)
    if full:
        draw_points(y + x0, -x + y0, default)
        draw_points(x + x0, -y + y0, default)
        draw_points(-x + x0, -y + y0, default)
        draw_points(-y + x0, -x + y0, default)


def draw_one_circle(radius, x0, y0, full, default):
    d = 1 - radius
    x = 0
    y = radius

    draw_8_way_points(x, y, x0, y0, full, default)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
            x += 1
        else:
            d = d + 2 * x - 2 * y + 5
            x += 1
            y = y - 1

        draw_8_way_points(x, y, x0, y0, full, default)


def draw_circle(radius, x0, y0, full=True, default= 2):
    while radius > 0:
        draw_one_circle(radius, x0, y0, full, default)
        radius -= 1


def draw_building(center, width, height, view="Front"):
    left = center - width
    right = center + width

    draw_line(left, 0, right, 0)  # Bottom
    draw_line(left, 0, left, height)  # Left
    draw_line(right, 0, right, height)  # Right
    draw_line(left, height, right, height)  # Top
    lineHeight = height
    while lineHeight > 0:
        draw_line(left, lineHeight, right, lineHeight)
        lineHeight -= 1

    if view == "Front":
        designTop = height
        designRight = center + 50

        glColor3f(0 / 255, 128 / 255, 255 / 255)
        while designRight > left and designTop > 0:
            draw_line(left, designTop, designRight, designTop)
            designRight -= 3
            designTop -= 12

        glColor3f(0 / 255, 128 / 255, 255 / 255)
        draw_building(center + 125, 25, height, "Side")

def draw_human(x0, y0):
    headRadius = 15
    bodyLength = 40
    handLength = 20
    legLength = 20
    bodyStart = y0-headRadius
    bodyEnd = bodyStart-bodyLength

    draw_circle(headRadius, x0, y0, True) #Head
    draw_line(x0, bodyStart, x0, bodyEnd) #Body
    draw_line(x0, bodyStart, x0-handLength, bodyStart-handLength) #Left hand
    draw_line(x0, bodyStart, x0+handLength, bodyStart-handLength) #Right hand
    draw_line(x0, bodyEnd, x0-legLength, bodyEnd-legLength) #Left leg
    draw_line(x0, bodyEnd, x0+legLength, bodyEnd-legLength) #Right leg



def human_movement(x, y):
    global fireAt
    if abs(fireAt - x) <= 50:
        return x
    elif x < fireAt:
        tx = 50
        t = np.array([[1, 0, tx],
                      [0, 1, 0],
                      [0, 0, 1]])

        v1 = np.array([[x],
                       [y],
                       [1]])

        v11 = np.matmul(t, v1)
        return v11[0][0]
    else:

        tx = -50
        t = np.array([[1, 0, tx],
                      [0, 1, 0],
                      [0, 0, 1]])

        v1 = np.array([[x],
                       [y],
                       [1]])

        v11 = np.matmul(t, v1)
        return v11[0][0]


######################################## zaima
def draw_drone(x0, y0):
    global d_x0
    if d_x0==None:
        x0=fireAt
    g=50

    draw_line(x0+g, y0+g, x0-g, y0+g)
    draw_line(x0-g, y0+g, x0 - g, y0-g)
    draw_line(x0 - g, y0-g, x0 + g, y0-g)
    draw_line(x0 + g, y0-g, x0+g, y0+g)

    draw_line(x0 + g, y0 + g, x0 + g+ g, y0 + g + g)
    draw_line(x0 - g, y0 + g, x0 - g- g, y0 + g + g)
    draw_line(x0 - g, y0 - g, x0 -g - g, y0 - g - g)
    draw_line(x0 + g, y0 - g, x0 + g + g, y0 - g - g)

    draw_circle(8, x0 + g+ g, y0 + g + g, True)
    draw_circle(8, x0 - g- g, y0 + g + g, True)
    draw_circle(8, x0 -g - g, y0 - g - g, True)
    draw_circle(8, x0 + g + g, y0 - g - g, True)

    draw_circle(10, x0 -25, y0 +25, True)
    draw_circle(10, x0 + 25, y0 + 25, True)

def drone_movement(x, y):
    global fireAt,count
    if d_x0==None:
        x=fireAt


    if x < fireAt:   # left to right
        if (count<10) and (inp==1) :
            tx = 50
            t = np.array([[1, 0, tx],
                          [0, 1, 0],
                          [0, 0, 1]])

            v1 = np.array([[x],
                           [y],
                           [1]])

            v11 = np.matmul(t, v1)
            count=count+1
            print(count)

            return v11[0][0]

        elif (count<27) and (inp==2) :
            tx = 50
            t = np.array([[1, 0, tx],
                          [0, 1, 0],
                          [0, 0, 1]])

            v1 = np.array([[x],
                           [y],
                           [1]])

            v11 = np.matmul(t, v1)
            count=count+1
            print(count)

            return v11[0][0]

        elif (count<45) and (inp==3):
            tx = 50
            t = np.array([[1, 0, tx],
                          [0, 1, 0],
                          [0, 0, 1]])

            v1 = np.array([[x],
                           [y],
                           [1]])

            v11 = np.matmul(t, v1)
            count = count + 1
            print(count)

            return v11[0][0]

    if (count>=11) and (inp==1):  # after compleating water drop
        tx = -50
        t = np.array([[1, 0, tx],
                      [0, 1, 0],
                      [0, 0, 1]])

        v1 = np.array([[x],
                       [y],
                       [1]])

        v11 = np.matmul(t, v1)
        return v11[0][0]

    if (count>=28) and (inp==2):  # after compleating water drop
        tx = -50
        t = np.array([[1, 0, tx],
                      [0, 1, 0],
                      [0, 0, 1]])

        v1 = np.array([[x],
                       [y],
                       [1]])

        v11 = np.matmul(t, v1)
        return v11[0][0]

    if (count>=46) and (inp==3):  # after compleating water drop
        tx = -50
        t = np.array([[1, 0, tx],
                      [0, 1, 0],
                      [0, 0, 1]])

        v1 = np.array([[x],
                       [y],
                       [1]])

        v11 = np.matmul(t, v1)
        return v11[0][0]


def rain_movement():
    global d_x0,count
    if d_x0 == None:
        d_x0 = fireAt
        glColor3f(1, 0, 0)

        count = count + 1
        #print(count)
        if (count<10) and (inp==1):   # untill 27 itterration rain drop

            for i in range(50):
                draw_points(fireAt, (random.randint(75, 500)), 3)
                draw_points(fireAt - 10, (random.randint(75, 500)), 3)
                draw_points(fireAt + 10, (random.randint(75, 500)), 3)
            for i in range(50):
                x = random.randint(10, 40)
                y = random.randint(70, 500)

                draw_line(fireAt - x, y, fireAt - x, y + 10)

                draw_line(fireAt + x, y, fireAt + x + 5, y - 5)
                draw_line(fireAt - x, y, fireAt - x + 5, y - 5)

        elif (count>=10) and (inp==1):   # when 27 or avob itterration i done my dropwater
            d_x0 = drone_movement(d_x0, d_y0)



        if (count<27) and (inp==2):   # untill 27 itterration rain drop

            for i in range(50):
                draw_points(fireAt, (random.randint(75, 500)), 3)
                draw_points(fireAt - 10, (random.randint(75, 500)), 3)
                draw_points(fireAt + 10, (random.randint(75, 500)), 3)
            for i in range(50):
                x = random.randint(10, 40)
                y = random.randint(70, 500)

                draw_line(fireAt - x, y, fireAt - x, y + 10)

                draw_line(fireAt + x, y, fireAt + x + 5, y - 5)
                draw_line(fireAt - x, y, fireAt - x + 5, y - 5)

        elif (count>=27) and (inp==2):   # when 27 or avob itterration i done my dropwater
            d_x0 = drone_movement(d_x0, d_y0)



        if (count<45) and (inp==3 ):   # untill 27 itterration rain drop

            for i in range(50):
                draw_points(fireAt, (random.randint(75, 500)), 3)
                draw_points(fireAt - 10, (random.randint(75, 500)), 3)
                draw_points(fireAt + 10, (random.randint(75, 500)), 3)
            for i in range(50):
                x = random.randint(10, 40)
                y = random.randint(70, 500)

                draw_line(fireAt - x, y, fireAt - x, y + 10)

                draw_line(fireAt + x, y, fireAt + x + 5, y - 5)
                draw_line(fireAt - x, y, fireAt - x + 5, y - 5)

        elif (count>=45) and (inp==3):   # when 27 or avob itterration i done my dropwater
            d_x0 = drone_movement(d_x0, d_y0)


###################################################################


def road_striping(center, width):
    left = center - width
    right = center + width
    glColor3f(255 / 255, 255 / 255, 255 / 255)
    for i in range(-123, -127, -1):
        draw_line(left, i, right, i)

def draw_road():
    # Footpath GREEN COLOR
    glColor3f(50 / 255, 205 / 255, 50 / 255)
    for Y in range(0, -40, -1):
        draw_line(-1000, Y, 1000, Y)
    # White line for distinguish the road from footpath
    glColor3f(255 / 255, 255 / 255, 255 / 255)
    for Y in range(-41, -45, -1):
        draw_line(-1000, Y, 1000, Y)
    # The road sheed color
    glColor3f(0 / 255, 15 / 255, 15 / 255)
    for Y in range(-46, -200, -1):
        draw_line(-1000, Y, 1000, Y)

    # White line for distinguish the road from footpath
    glColor3f(255 / 255, 255 / 255, 255 / 255)
    for Y in range(-201, -205, -1):
        draw_line(-1000, Y, 1000, Y)

    glColor3f(50 / 255, 205 / 255, 50 / 255)
    for Y in range(-206, -246, -1):
        draw_line(-1000, Y, 1000, Y)
    # road Striping
    for j in range(-1000, 1001, 200):
        road_striping(j, 25)



def iterate():
    glViewport(0, 0, 1000, 1000)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1000, 1000, -1000, 1000, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    global inputTaken, inp, fireAt, h_x0, h_y0, h_x1, h_y1 , d_x0, d_y0

    # draw_line(0, -1000, 0, 1000)
    glColor3f(102 / 255, 178 / 255, 255 / 255)
    draw_building(-800, 100, 400)

    glColor3f(102 / 255, 178 / 255, 255 / 255)
    draw_building(0, 100, 600)

    glColor3f(102 / 255, 178 / 255, 255 / 255)
    draw_building(750, 100, 400)

    glColor3f(255 / 255, 255 / 255, 0 / 255)

    if not inputTaken:
        inp = int(input("Fire broke out in building 1/2/3: "))
        inputTaken = True

    if inp == 1:
        draw_circle(100, -800, 0, False)  # r, x, y
        fireAt = -800
    elif inp == 2:
        draw_circle(100, 0, 0, False)  # r, x, y
        fireAt = 0
    elif inp == 3:
        fireAt = 750
        draw_circle(100, 750, 0, False)  # r, x, y

    # Road Draw
    draw_road()

    # Draw human
    draw_human(h_x0, h_y0)
    h_x0 = human_movement(h_x0, h_y0)
    draw_human(h_x1, h_y1)
    h_x1 = human_movement(h_x1, h_y1)


###################################zaima
    draw_drone(d_x0, d_y0)
    d_x0 = drone_movement(d_x0, d_y0)
    rain_movement()
##########################################


    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(showScreen)

glutIdleFunc(showScreen)
glutMainLoop()