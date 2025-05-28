from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys
import time

width, height = 800, 600
catcher_w= 100
catcher_h = 20
catcher_y = 50
catcher_white = (1.0, 1.0, 1.0)

diamond_size = 20
diamond_color = (1.0, 0.0, 0.0)
diamond_x = random.randint(100, width - 100)
diamond_y = height - diamond_size

score = 0
speed = 2
is_gameOver = False
is_paused = False

def draw_point(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))  
    glEnd()

def draw_midpoint_line(x1, y1, x2, y2):
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1

    if dx > dy:
        d = 2 * dy - dx
        for _ in range(dx):
            draw_point(x, y)
            x += sx
            if d >= 0:
                y += sy
                d -= 2 * dx
            d += 2 * dy
    else:
        d = 2 * dx - dy
        for _ in range(dy):
            draw_point(x, y)
            y += sy
            if d >= 0:
                x += sx
                d -= 2 * dy
            d += 2 * dx

def draw_diamond(x, y):
    half = diamond_size // 2
    glColor3f(*diamond_color)
    draw_midpoint_line(x, y + half, x + half, y)
    draw_midpoint_line(x + half, y, x, y - half)
    draw_midpoint_line(x, y - half, x - half, y)
    draw_midpoint_line(x - half, y, x, y + half)

def draw_catcher():
    half = catcher_w// 2
    h = catcher_h
    glColor3f(*catcher_white)
    draw_midpoint_line(catcher_x - half + 20, catcher_y, catcher_x + half - 20, catcher_y)            # Top horizontal line
    draw_midpoint_line(catcher_x - half, catcher_y + h, catcher_x - half + 20, catcher_y)             # Left diagonal
    draw_midpoint_line(catcher_x + half, catcher_y + h, catcher_x + half - 20, catcher_y)             # Right diagonal
    draw_midpoint_line(catcher_x - half, catcher_y + h, catcher_x + half, catcher_y + h)              # Bottom horizontal line

def draw_buttons():
    # Left Arrow (Bright teal color - Restart)
    glColor3f(0.0, 0.8, 0.8)
    x = 60  # Tip of arrow
    y = height - 40

    # Shaft
    draw_midpoint_line(x, y, x + 20, y)

    # Arrowhead
    draw_midpoint_line(x, y, x + 10, y + 10)
    draw_midpoint_line(x, y, x + 10, y - 10)

    # Pause/Play Icon (Yellow)
    glColor3f(1.0, 1.0, 0.0)
    if is_paused:
        # Draw Play Icon (Right-pointing Triangle)
        x = width // 2 - 10
        y = height - 50
        draw_midpoint_line(x, y, x, y + 20)               # Left edge of triangle
        draw_midpoint_line(x, y, x + 15, y + 10)          # Bottom to tip
        draw_midpoint_line(x, y + 20, x + 15, y + 10)     # Top to tip
    else:
        # Draw Pause Icon (Two vertical lines)
        draw_midpoint_line(width // 2 - 5, height - 50, width // 2 - 5, height - 30)
        draw_midpoint_line(width // 2 + 5, height - 50, width // 2 + 5, height - 30)

    # Exit Icon (Red 'X')
    glColor3f(1.0, 0.0, 0.0)
    draw_midpoint_line(width - 50, height - 50, width - 30, height - 30)
    draw_midpoint_line(width - 50, height - 30, width - 30, height - 50)


def display():
    global diamond_y, diamond_x, score, speed, catcher_white, is_gameOver
    glClear(GL_COLOR_BUFFER_BIT)
    draw_buttons()
    if not is_gameOver and not is_paused:
        diamond_y -= speed

        if abs(diamond_y - catcher_y) < 10 and abs(diamond_x - catcher_x) < catcher_w// 2:
            score += 1
            print("Score:", score)
            reset_diamond()
            speed += 0.2

        elif diamond_y <= 0:
            print("Game Over! Score:", score)
            catcher_white = (1.0, 0.0, 0.0)
            is_gameOver = True

    draw_diamond(diamond_x, diamond_y)
    draw_catcher()
    glutSwapBuffers()

def reset_diamond():
    global diamond_x, diamond_y, diamond_color
    diamond_x = random.randint(100, width - 100)
    diamond_y = height - diamond_size
    diamond_color = (random.random(), random.random(), random.random())

def keyboard(key, x, y):
    global catcher_x
    if is_gameOver or is_paused:
        return
    if key == GLUT_KEY_LEFT and catcher_x - catcher_w// 2 > 0:
        catcher_x -= 20
    elif key == GLUT_KEY_RIGHT and catcher_x + catcher_w// 2 < width:
        catcher_x += 20

def mouse_click(button, state, x, y):
    global is_paused, is_gameOver, catcher_white, score, speed
    if state == GLUT_DOWN:
        if x < 80 and y < 80:
            restart_game()
        elif width // 2 - 20 < x < width // 2 + 20 and y < 80:
            if not is_gameOver:
                is_paused = not is_paused
        elif width - 60 < x < width - 20 and y < 80:
            print("Game over! Score:", score)
            os._exit(0) 


def restart_game():
    global score, speed, is_gameOver, catcher_white, is_paused
    score = 0
    speed = 2
    catcher_white = (1.0, 1.0, 1.0)
    is_gameOver = False
    is_paused = False
    reset_diamond()
    print("Starting Over")

def timer(v):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, width, 0, height)

catcher_x = width // 2

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutCreateWindow("Catch the Diamonds!".encode("ascii"))
init()
glutDisplayFunc(display)
glutSpecialFunc(keyboard)
glutMouseFunc(mouse_click)
glutTimerFunc(0, timer, 0)
glutMainLoop()