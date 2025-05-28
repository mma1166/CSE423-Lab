#Task1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

rain_drop_arr = []
rain_speed = 0.001
rain_angle = 0
indicator = (0.0, 0.0, 0.0, 0.0)

def Housedesign():
     glPointSize(6)
     glLineWidth(6)
     glColor3f(0.0, 1.0, 0.0)

     # Roof
     glColor3f(0.1, 1.2, 0.3)
     glBegin(GL_TRIANGLES)
     glVertex2f(-150, 40)
     glVertex2f(0, 150)
     glVertex2f(150, 40)
     glEnd()

     #body Design
     glColor3f(1.0,1.0,0.0)
     glBegin(GL_LINES)
     glVertex2f(-150, -200)  # Bottom-left to Bottom-right
     glVertex2f(150, -200)

     glVertex2f(150, -200)   # Bottom-right to Top-right
     glVertex2f(150, 40)

     glVertex2f(150, 40)     # Top-right to Top-left
     glVertex2f(-150, 40)

     glVertex2f(-150, 40)    # Top-left to Bottom-left
     glVertex2f(-150, -200)
     glEnd()

     # door Design
     glPointSize(3)
     glLineWidth(3)
     glColor3f(0.0, 0.0, 1.1)
     glBegin(GL_LINES)

     glVertex2f(-80, -120)  # Bottom-left to Bottom-right
     glVertex2f(-120, -120)

     glVertex2f(-80, -200)   # Bottom-right to Top-right
     glVertex2f(-80, -120)

     glVertex2f(-80, -120)    # Top-right to Top-left
     glVertex2f(-120, -120)

     glVertex2f(-120, -120)   # Top-left to Bottom-left
     glVertex2f(-120, -200)
     glEnd()

     #window Design
     glColor3f(0.0,1.0,1.0)
     glBegin(GL_LINES)
     glVertex2f(70, -45)   # Bottom-left to Bottom-right
     glVertex2f(110, -45)

     glVertex2f(70, -45)   # Bottom-right to Top-right
     glVertex2f(70, -15)

     glVertex2f(70, -15)  # Top-right to Top-left
     glVertex2f(110, -15)

     glVertex2f(110, -15)  # Top-left to Bottom-left (closing the loop)
     glVertex2f(110, -45)

     glColor3f(1.0, 0.0, 1.0)
     glVertex2f(90, -45)
     glVertex2f(90, -15)
     glVertex2f(70, -30)
     glVertex2f(110, -30)
     glEnd()

     # door lock
     glPointSize(6)
     glBegin(GL_POINTS)
     glVertex2f(-90, -150)
     glEnd()

def Rain_Drops_Drawing():
    glColor3f(0.8, 0.5, 0.0)
    glBegin(GL_LINES)
    for (x, y) in rain_drop_arr:
        glVertex2f(x, y)
        glVertex2f(x + rain_angle * 5, y - 5)
    glEnd()

def Rain_speed_controller():
    global rain_drop_arr
    for i, (x, y) in enumerate(rain_drop_arr):
        y -= rain_speed * 40
        x += rain_angle
        if y < -250:
            y = random.uniform(100, 250)
            x = random.uniform(-250, 250)
        rain_drop_arr[i] = (x, y)

def DayNight_Controller(key, x, y):
    global indicator

    if key == b'n' or key == b'N':  # Shift to night mode
        indicator = (0.0, 0.0, 0.0, 0.0)
        print("It's night")
    elif key == b'd' or key == b'D':  # Shift to day mode
        indicator = (1.0, 1.0, 1.0, 1.0)
        print("It's morning")

    glutPostRedisplay()

def RainFlowAngle ( key, x, y ):
    global rain_angle
    if key == GLUT_KEY_RIGHT:
        rain_angle += 0.004
        print("Rain Tilt Right")
    if key == GLUT_KEY_LEFT:
        rain_angle -= 0.004
        print("Rain Tilt Left")

    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*indicator)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glViewport(0, 0, 600, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    Housedesign()
    Rain_Drops_Drawing()
    glutSwapBuffers()

def animation_mood():
    Rain_speed_controller()
    glutPostRedisplay()

def init_rain():
    global rain_drop_arr
    rain_drop_arr = [(random.uniform(-250, 250), random.uniform(-250, 250)) for r in range(100)]


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(600, 600)
glutInitWindowPosition(100, 100)

wind = glutCreateWindow(b"RainFall House")
init_rain()

glutDisplayFunc(display)
glutIdleFunc(animation_mood)
glutKeyboardFunc(DayNight_Controller)
glutSpecialFunc(RainFlowAngle)

glutMainLoop()




# # TASK-2
# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random
# import time
# points = []
# speed = 0.003
# freeze = False
# blink = False
# blink_time = time.time()

# class MovablePoint:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.direct_x = random.choice([-1, 1])
#         self.direct_y = random.choice([-1, 1])
#         self.color = [random.random(), random.random(), random.random()]
#         self.original_color = self.color.copy()

#     def update_position(self):
#         if not freeze:
#             self.x += self.direct_x * speed
#             self.y += self.direct_y * speed
#             self.check_boundary()

#     def check_boundary(self):
#         if self.x >= 250 or self.x <= -250:
#             self.direct_x *= -1
#         if self.y >= 250 or self.y <= -250:
#             self.direct_y *= -1

#     def blinking(self):
#         if blink:
#             if self.color == self.original_color:
#                 self.color = [0, 0, 0]
#             else:
#                 self.color = self.original_color
#         elif not blink and self.color != self.original_color:
#             self.color = self.original_color

# def init():
#     glClearColor(0, 0, 0, 0)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glEnable(GL_POINT_SMOOTH)
#     gluOrtho2D(-250, 250, -250, 250)

# def display():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glClearColor(0, 0, 0, 0)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()

#     BoundaryDraw()
#     PingPongDraw()

#     glutSwapBuffers()

# def animation():
#     global blink_time
#     if time.time() - blink_time > 0.05:  # Toggle blink every 0.05 seconds
#         for point in points:
#             point.blinking()
#         blink_time = time.time()

#     for point in points:
#         point.update_position()
#     glutPostRedisplay()

# def BoundaryDraw():
#     glColor3f(0, 1, 0)
#     glBegin(GL_LINE_LOOP)
#     glVertex2f(-250, -250)
#     glVertex2f(250, -250)
#     glVertex2f(250, 250)
#     glVertex2f(-250, 250)
#     glEnd()

# def PingPongDraw():
#     glPointSize(10)
#     for point in points:
#         glColor3f(*point.color)
#         glBegin(GL_POINTS)
#         glVertex2f(point.x, point.y)
#         glEnd()

# def control_in_Mouse(button, state, x, y):
#     global blink
#     if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
#         cx, cy = conv_cord(x, y)
#         if -250 < cx < 250 and -250 < cy < 250:
#             points.append(MovablePoint(cx, cy))

#     elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
#         blink = not blink

# def Control_in_Key(key, x, y):
#     global speed
#     if key == GLUT_KEY_UP:
#         speed += 0.009
#     elif key == GLUT_KEY_DOWN and speed > 0.001:
#         speed -= 0.009

# def Control_in_Keyboard(key, x, y):
#     global freeze
#     if key == b' ':
#         freeze = not freeze

# def conv_cord(x, y):
#     return x - (500 / 2), (500 / 2) - y

# glutInit()
# glutInitDisplayMode(GLUT_RGBA)
# glutInitWindowSize(600, 600)
# glutInitWindowPosition(100, 100)

# wind = glutCreateWindow(b"PingPong Box")
# init()

# glutDisplayFunc(display)
# glutIdleFunc(animation)
# glutKeyboardFunc(Control_in_Keyboard)
# glutSpecialFunc(Control_in_Key)
# glutMouseFunc(control_in_Mouse)
# glutMainLoop()