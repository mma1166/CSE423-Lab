from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Game state variables
player_pos = [0, 0, 0]  # Player position
player_angle = 0  # Player rotation angle
player_life = 5
game_score = 0
bullets_missed = 0
game_over = False

# Cheat modes
cheat_mode = False
cheat_vision = False

# Camera settings
camera_mode = "third_person" 
camera_pos = (0, 500, 500)
camera_angle = 0
camera_height = 500

# Enemy settings
enemies = []
for _ in range(5):
    enemies.append({
        'pos': [random.randint(-400, 400), random.randint(-400, 400), 0],
        'size': random.uniform(30, 50),
        'growing': True,
        'speed': random.uniform(0.02, 0.06)
    })

# Bullet settings
bullets = []
bullet_speed = 80

# Gun settings
gun_angle = 0
gun_length = 100

# Grid settings
GRID_LENGTH = 600
fovY = 120

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])

    if game_over:
        glRotatef(90, 1, 0, 0)  # Lay down on game over

    glRotatef(player_angle, 0, 0, 1)

    # Head - Sphere
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)  # Black
    glTranslatef(0, 0, 90)
    gluSphere(gluNewQuadric(), 20, 20, 20)
    glPopMatrix()

    # Torso - Cuboid
    glPushMatrix()
    glColor3f(0.4, 0.6, 0.4)  # Olive green
    glTranslatef(0, 0, 50)
    glScalef(40, 20, 60)
    glutSolidCube(1)
    glPopMatrix()

    # Arms - Cylinders (horizontal)
    for side in [-1, 1]:
        glPushMatrix()
        glColor3f(1.0, 0.8, 0.6)  # Skin color
        glTranslatef(side * 30, 0, 80)  # Move to shoulder height
        glRotatef(90, 0, 1, 0)  # Rotate to horizontal
        gluCylinder(gluNewQuadric(), 5, 5, 20, 10, 10)
        glPopMatrix()

        # Shoulder Joint Sphere
        glPushMatrix()
        glColor3f(1.0, 0.8, 0.6)
        glTranslatef(side * 30, 0, 80)
        gluSphere(gluNewQuadric(), 6, 10, 10)
        glPopMatrix()

    # Gun - Tapered Cylinder forward
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.9)
    glTranslatef(0, 20, 70)
    glRotatef(gun_angle, 0, 0, 1)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 3, 1, 60, 10, 10)
    glPopMatrix()

    # Legs - Blue Cuboids
    for side in [-15, 15]:
        glPushMatrix()
        glColor3f(0.0, 0.0, 1.0)  # Blue
        glTranslatef(side, 0, 10)
        glScalef(10, 10, 40)
        glutSolidCube(1)
        glPopMatrix()

    glPopMatrix()

def draw_enemies():
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy['pos'][0], enemy['pos'][1], enemy['pos'][2])

        # Lower Sphere (Body)
        glColor3f(1.0, 0.0, 0.0)  # Red
        gluSphere(gluNewQuadric(), enemy['size'], 20, 20)

        # Upper Sphere (Head)
        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)  # Black
        glTranslatef(0, 0, enemy['size'] * 1.2)
        gluSphere(gluNewQuadric(), enemy['size'] * 0.4, 10, 10)
        glPopMatrix()

        glPopMatrix()

def draw_bullets():
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet['pos'][0], bullet['pos'][1], bullet['pos'][2])
        glColor3f(1.0, 1.0, 0.0)  # Bright yellow

        # Make bullet a  cube 
        glScalef(1.5, 1.5, 1.5)
        glutSolidCube(15)  # size 

        glPopMatrix()


def draw_grid():
    # Draw checkered floor (purple and white)
    square_size = 50
    glPushMatrix()
    for x in range(-GRID_LENGTH, GRID_LENGTH, square_size):
        for y in range(-GRID_LENGTH, GRID_LENGTH, square_size):
            if (x + y) // square_size % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)  # White
            else:
                glColor3f(0.6, 0.4, 1.0)  # Purple
            glBegin(GL_QUADS)
            glVertex3f(x, y, 0)
            glVertex3f(x + square_size, y, 0)
            glVertex3f(x + square_size, y + square_size, 0)
            glVertex3f(x, y + square_size, 0)
            glEnd()
    glPopMatrix()

    # Boundaries (walls)
    wall_height = 100
    glBegin(GL_QUADS)
    
    # Left wall - Green
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)

    # Right wall - Lime
    glColor3f(0.5, 1.0, 0.5)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)

    # Back wall - Blue
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)

    # Front wall - Cyan
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    
    glEnd()

def keyboardListener(key, x, y):
    global player_pos, player_angle, gun_angle, cheat_mode, cheat_vision, game_over
    
    if game_over and key == b'r':
        reset_game()
        return
    
    # Player movement
    if key == b'w':  # Move forward
        player_pos[0] -= 5 * math.sin(math.radians(player_angle))
        player_pos[1] -= 5 * math.cos(math.radians(player_angle))
    if key == b's':  # Move backward
        player_pos[0] += 5 * math.sin(math.radians(player_angle))
        player_pos[1] += 5 * math.cos(math.radians(player_angle))
    
    # Gun rotation
    if key == b'a':  # Rotate left
        player_angle = (player_angle - 5) % 360
    if key == b'd':  # Rotate right
        player_angle = (player_angle + 5) % 360
    
    # Cheat modes
    if key == b'c':
        cheat_mode = not cheat_mode
    if key == b'v':
        cheat_vision = not cheat_vision

def specialKeyListener(key, x, y):
    global camera_angle, camera_height
    
    # Camera height adjustment
    if key == GLUT_KEY_UP:
        camera_height += 10
    if key == GLUT_KEY_DOWN:
        camera_height -= 10
    
    # Camera rotation
    if key == GLUT_KEY_LEFT:
        camera_angle = (camera_angle + 5) % 360
    if key == GLUT_KEY_RIGHT:
        camera_angle = (camera_angle - 5) % 360

def mouseListener(button, state, x, y):
    global bullets, gun_angle

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        bullet_angle = player_angle + gun_angle
        rad_angle = math.radians(bullet_angle)

    # Calculate gun tip position
        bullet_x = player_pos[0] + gun_length * math.sin(rad_angle)
        bullet_y = player_pos[1] + gun_length * math.cos(rad_angle)
        bullet_z = player_pos[2] + 70  # approximate gun height on player

        bullets.append({
        'pos': [bullet_x, bullet_y, bullet_z],
        'dir': [math.sin(rad_angle), math.cos(rad_angle), 0],
        'distance': 0
        })

        print("Player Bullet Fired")

    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        global camera_mode
        if camera_mode == "third_person":
            camera_mode = "first_person"
        else:
            camera_mode = "third_person"

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera_mode == "third_person":
        # Third-person camera
        cam_x = player_pos[0] + 500 * math.sin(math.radians(camera_angle))
        cam_y = player_pos[1] + 500 * math.cos(math.radians(camera_angle))
        gluLookAt(cam_x, cam_y, camera_height,
                  player_pos[0], player_pos[1], 30,
                  0, 0, 1)
    else:
        if game_over:
            # Game over: top-down view
            gluLookAt(player_pos[0], player_pos[1] - 100, player_pos[2] + 150,
                      player_pos[0], player_pos[1], player_pos[2],
                      0, 0, 1)
        else:
            # Gameplay: First-person view - "from gun"
            angle = player_angle + gun_angle
            if cheat_mode and cheat_vision:
                angle += 30

            # Position camera a bit in front of gun (at muzzle height)
            cam_x = player_pos[0] + 40 * math.sin(math.radians(angle))
            cam_y = player_pos[1] + 40 * math.cos(math.radians(angle))
            cam_z = player_pos[2] + 70  # Above torso, near gun height

            look_x = cam_x + 100 * math.sin(math.radians(angle))
            look_y = cam_y + 100 * math.cos(math.radians(angle))

            gluLookAt(cam_x, cam_y, cam_z,
                      look_x, look_y, cam_z,
                      0, 0, 1)

def update_game():
    global bullets, enemies, player_life, game_score, bullets_missed, game_over, gun_angle
    
    if game_over:
        return
    
    # Update bullets
    for bullet in bullets[:]:
        bullet['pos'][0] += bullet['dir'][0] * bullet_speed
        bullet['pos'][1] += bullet['dir'][1] * bullet_speed
        bullet['distance'] += bullet_speed
        

        # Remove bullets that go too far OR exit the floor boundary
        x, y = bullet['pos'][0], bullet['pos'][1]
        if (bullet['distance'] > 1000 or 
            abs(x) > GRID_LENGTH or abs(y) > GRID_LENGTH):
            
            bullets.remove(bullet)
            bullets_missed += 1
            print(f"Bullet Missed {bullets_missed}")

    
    # Update enemies
    for enemy in enemies:
        # Move enemies toward player
        dx = player_pos[0] - enemy['pos'][0]
        dy = player_pos[1] - enemy['pos'][1]
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            enemy['pos'][0] += (dx/dist) * enemy['speed']
            enemy['pos'][1] += (dy/dist) * enemy['speed']
        
        # Update enemy size (pulsing effect)
        if enemy['growing']:
            enemy['size'] += 0.2
            if enemy['size'] > 50:
                enemy['growing'] = False
        else:
            enemy['size'] -= 0.2
            if enemy['size'] < 30:
                enemy['growing'] = True
        
        # Check collision with player
        player_dist = math.sqrt((player_pos[0]-enemy['pos'][0])**2 + 
                       (player_pos[1]-enemy['pos'][1])**2)
        if player_dist < 30 + enemy['size'] and player_life > 0:
            player_life -= 1
            enemy['pos'] = [random.randint(-400, 400), random.randint(-400, 400), 0]
            print(f"Remaining Player Life: {player_life}")

    
    # Check bullet-enemy collisions
    for bullet in bullets[:]:
        for enemy in enemies:
            bullet_dist = math.sqrt((bullet['pos'][0]-enemy['pos'][0])**2 + 
                          (bullet['pos'][1]-enemy['pos'][1])**2)
            if bullet_dist < enemy['size']:
                game_score += 10
                print(f"Enemy Hit! Score: {game_score}")

                enemy['pos'] = [random.randint(-400, 400), random.randint(-400, 400), 0]
                if bullet in bullets:
                    bullets.remove(bullet)
                break
    if cheat_mode:
        gun_angle = (gun_angle + 5) % 360
        if random.random() < 0.02:  # fire rate
            print("Player Bullet Fired (Cheat Mode)")
            bullet_angle = player_angle + gun_angle
            bullets.append({
                'pos': [player_pos[0], player_pos[1], 30],
                'dir': [math.sin(math.radians(bullet_angle)),
                       math.cos(math.radians(bullet_angle)),
                        0],
                'distance': 0
        })

    # Check game over conditions
    if player_life <= 0 or bullets_missed >= 10:
        game_over = True
        print("GAME OVER! Press 'R' to restart.")


def reset_game():
    global player_pos, player_angle, gun_angle, player_life, game_score, bullets_missed
    global bullets, enemies, game_over, cheat_mode, cheat_vision
    
    player_pos = [0, 0, 0]
    player_angle = 0
    gun_angle = 0
    player_life = 5
    game_score = 0
    bullets_missed = 0
    bullets = []
    game_over = False
    cheat_mode = False
    cheat_vision = False
    
    enemies = []
    for _ in range(5):
        enemies.append({
            'pos': [random.randint(-400, 400), random.randint(-400, 400), 0],
            'size': random.uniform(30, 50),
            'growing': True,
            'speed': random.uniform(0.02, 0.06)
        })

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    setupCamera()
    
    # Draw game elements
    draw_grid()
    draw_player()
    draw_enemies()
    draw_bullets()
    
    # Display game info
    draw_text(10, 770, f"Player Life Remaining: {player_life}")
    draw_text(10, 740, f"Game Score: {game_score}")
    draw_text(10, 710, f"Player Bullet Missed: {bullets_missed}")
    
    if cheat_mode:
        draw_text(10, 680, "CHEAT MODE: ON", GLUT_BITMAP_HELVETICA_12)
    if cheat_vision:
        draw_text(10, 660, "CHEAT VISION: ON", GLUT_BITMAP_HELVETICA_12)
    if game_over:
        draw_text(400, 400, "GAME OVER! Press R to restart", GLUT_BITMAP_TIMES_ROMAN_24)
    
    glutSwapBuffers()

def idle():
    update_game()
    glutPostRedisplay()
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Bullet Frenzy")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()
if __name__ == "__main__":
    main()