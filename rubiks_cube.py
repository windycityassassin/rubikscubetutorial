import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
from typing import List, Tuple
import math
import sys
import os

os.environ['PYOPENGL_DEBUG'] = 'debug'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

print("Starting program...")

def init_pygame_and_gl():
    """Initialize Pygame and OpenGL with error checking"""
    print("Initializing Pygame...")
    pygame.init()
    print("Pygame initialized!")
    
    print("Setting up display...")
    display = (800, 600)
    try:
        screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        if not screen:
            print("Failed to create display surface!")
            sys.exit(1)
        pygame.display.set_caption("Rubik's Cube")
        print("Display setup successful!")
    except pygame.error as e:
        print(f"Failed to create display: {e}")
        sys.exit(1)
    
    print("Setting up OpenGL...")
    try:
        # Clear to black
        glClearColor(0.0, 0.0, 0.0, 1.0)
        print("Set clear color")
        
        # Basic setup
        glViewport(0, 0, display[0], display[1])
        print("Set viewport")
        
        # Enable features
        print("Enabling OpenGL features...")
        glEnable(GL_DEPTH_TEST)
        print("Enabled depth test")
        glEnable(GL_LIGHTING)
        print("Enabled lighting")
        glEnable(GL_LIGHT0)
        print("Enabled light 0")
        glEnable(GL_COLOR_MATERIAL)
        print("Enabled color material")
        glShadeModel(GL_SMOOTH)
        print("Set shade model")
        
        # Set up material properties
        print("Setting up materials...")
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Set up lighting with error checking
        print("Setting up lighting...")
        light_ambient = [0.6, 0.6, 0.6, 1.0]
        light_diffuse = [0.8, 0.8, 0.8, 1.0]
        light_position = [2.0, 4.0, 5.0, 0.0]
        
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        print("Set light ambient")
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        print("Set light diffuse")
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        print("Set light position")
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.4, 0.4, 0.4, 1.0])
        print("Set light model")
        
        # Set up perspective
        print("Setting up perspective...")
        glMatrixMode(GL_PROJECTION)
        print("Set matrix mode to projection")
        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
        print("Set perspective")
        glMatrixMode(GL_MODELVIEW)
        print("Set matrix mode to modelview")
        
        # Test if everything is working
        error = glGetError()
        if error != GL_NO_ERROR:
            print(f"OpenGL error during initialization: {error}")
            sys.exit(1)
            
        print("OpenGL initialization successful!")
        
        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        pygame.display.flip()
        print("Initial screen clear done")
        
    except Exception as e:
        print(f"Failed to initialize OpenGL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Define colors with alpha
COLORS = {
    'red': (1, 0, 0, 1),
    'green': (0, 1, 0, 1),
    'blue': (0, 0, 1, 1),
    'yellow': (1, 1, 0.1, 1),  # Even brighter yellow with slight warmth
    'orange': (1, 0.3, 0, 1),  # Darker and more reddish orange
    'white': (1, 1, 1, 1),
    'black': (0, 0, 0, 1)
}

class Cubie:
    def __init__(self, position: Tuple[float, float, float], colors: List[Tuple[float, float, float, float]]):
        self.position = list(position)
        self.colors = colors  # [right, left, top, bottom, front, back]
        self.size = 0.95  # Slightly smaller than 1 to create gaps
    
    def draw(self):
        """Draw a single cubie"""
        try:
            glPushMatrix()
            
            # Move to cubie position
            glTranslatef(self.position[0], self.position[1], self.position[2])
            
            # Draw each face
            self.draw_face('right', self.colors[0])   # Right face
            self.draw_face('left', self.colors[1])    # Left face
            self.draw_face('top', self.colors[2])     # Top face
            self.draw_face('bottom', self.colors[3])  # Bottom face
            self.draw_face('front', self.colors[4])   # Front face
            self.draw_face('back', self.colors[5])    # Back face
            
            glPopMatrix()
        except Exception as e:
            print(f"Error drawing cubie at position {self.position}: {e}")
            import traceback
            traceback.print_exc()
    
    def draw_face(self, face_type: str, color: Tuple[float, float, float, float]):
        """Draw a single face of the cubie"""
        try:
            s = self.size / 2  # Half size for vertices
            
            glBegin(GL_QUADS)
            glColor4fv(color)  # Set the face color
            
            if face_type == 'right':  # Right face (x = 1)
                glNormal3f(1.0, 0.0, 0.0)
                glVertex3f(s, -s, -s)
                glVertex3f(s, s, -s)
                glVertex3f(s, s, s)
                glVertex3f(s, -s, s)
            elif face_type == 'left':  # Left face (x = -1)
                glNormal3f(-1.0, 0.0, 0.0)
                glVertex3f(-s, -s, -s)
                glVertex3f(-s, -s, s)
                glVertex3f(-s, s, s)
                glVertex3f(-s, s, -s)
            elif face_type == 'top':  # Top face (y = 1)
                glNormal3f(0.0, 1.0, 0.0)
                glVertex3f(-s, s, -s)
                glVertex3f(-s, s, s)
                glVertex3f(s, s, s)
                glVertex3f(s, s, -s)
            elif face_type == 'bottom':  # Bottom face (y = -1)
                glNormal3f(0.0, -1.0, 0.0)
                glVertex3f(-s, -s, -s)
                glVertex3f(s, -s, -s)
                glVertex3f(s, -s, s)
                glVertex3f(-s, -s, s)
            elif face_type == 'front':  # Front face (z = 1)
                glNormal3f(0.0, 0.0, 1.0)
                glVertex3f(-s, -s, s)
                glVertex3f(s, -s, s)
                glVertex3f(s, s, s)
                glVertex3f(-s, s, s)
            else:  # Back face (z = -1)
                glNormal3f(0.0, 0.0, -1.0)
                glVertex3f(-s, -s, -s)
                glVertex3f(-s, s, -s)
                glVertex3f(s, s, -s)
                glVertex3f(s, -s, -s)
            
            glEnd()
            
            # Draw black edges
            glColor4fv(COLORS['black'])
            glBegin(GL_LINE_LOOP)
            glVertex3f(-s, -s, -s)
            glVertex3f(s, -s, -s)
            glVertex3f(s, s, -s)
            glVertex3f(-s, s, -s)
            glEnd()
            
        except Exception as e:
            print(f"Error drawing face {face_type}: {e}")
            import traceback
            traceback.print_exc()

class RubiksCube:
    def __init__(self):
        """Initialize the Rubik's Cube with all cubies in solved state"""
        self.cubies = []
        self.moves = ['F', 'B', 'R', 'L', 'U', 'D']
        
        # Create all 27 cubies (3x3x3)
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    # Initialize all faces as black
                    colors = [COLORS['black']] * 6  # [right, left, top, bottom, front, back]
                    
                    # Set colors for visible faces
                    if x == 1:  # Right face
                        colors[0] = COLORS['green']
                    if x == -1:  # Left face
                        colors[1] = COLORS['blue']
                    if y == 1:   # Top face
                        colors[2] = COLORS['white']
                    if y == -1:  # Bottom face
                        colors[3] = COLORS['yellow']
                    if z == 1:   # Front face
                        colors[4] = COLORS['red']
                    if z == -1:  # Back face
                        colors[5] = COLORS['orange']
                    
                    # Create cubie with position and colors
                    self.cubies.append(Cubie((x, y, z), colors))
        print("Cube initialized with all cubies")
    
    def draw(self):
        """Draw the entire cube"""
        try:
            glPushMatrix()
            # Scale the entire cube to fit the view
            glScalef(0.5, 0.5, 0.5)
            
            # Draw each cubie
            for cubie in self.cubies:
                cubie.draw()
            
            glPopMatrix()
        except Exception as e:
            print(f"Error drawing cube: {e}")
            import traceback
            traceback.print_exc()
            
    def scramble(self, num_moves: int = 20):
        """Scramble the cube with random moves"""
        print("\nStarting scramble...")
        for i in range(num_moves):
            # Choose a random face and direction
            face = random.choice(self.moves)
            clockwise = random.choice([True, False])
            
            # Print debug info
            print(f"\nMove {i+1}/{num_moves}:")
            print(f"Selected face: {face}, {'clockwise' if clockwise else 'counterclockwise'}")
            
            # Print colors before rotation
            print("Colors before rotation:")
            for j, cubie in enumerate(self.cubies):
                if any(c != COLORS['black'] for c in cubie.colors):
                    print(f"Cubie {j} at {cubie.position}: {[c == COLORS['black'] for c in cubie.colors]}")
            
            # Perform the rotation
            self.rotate_face(face, clockwise)
            
            # Print colors after rotation
            print("Colors after rotation:")
            for j, cubie in enumerate(self.cubies):
                if any(c != COLORS['black'] for c in cubie.colors):
                    print(f"Cubie {j} at {cubie.position}: {[c == COLORS['black'] for c in cubie.colors]}")
            
            # Verify no colors were lost
            for cubie in self.cubies:
                visible_faces = sum(1 for c in cubie.colors if c != COLORS['black'])
                if visible_faces == 0 and any(abs(p) == 1 for p in cubie.position):
                    print(f"WARNING: Cubie at {cubie.position} lost all colors!")
                elif visible_faces > 3:
                    print(f"WARNING: Cubie at {cubie.position} has too many colors: {visible_faces}")
        
        print("\nScramble complete!")

    def rotate_face(self, face: str, clockwise: bool = True):
        """Rotate a face of the cube"""
        try:
            print(f"Rotating face {face} {'clockwise' if clockwise else 'counterclockwise'}")
            
            # Get the axis and coordinate for the face
            if face == 'F':  # Front face (z = 1)
                axis = 2  # z-axis
                coord = 1
            elif face == 'B':  # Back face (z = -1)
                axis = 2  # z-axis
                coord = -1
            elif face == 'R':  # Right face (x = 1)
                axis = 0  # x-axis
                coord = 1
            elif face == 'L':  # Left face (x = -1)
                axis = 0  # x-axis
                coord = -1
            elif face == 'U':  # Up face (y = 1)
                axis = 1  # y-axis
                coord = 1
            elif face == 'D':  # Down face (y = -1)
                axis = 1  # y-axis
                coord = -1
            else:
                print(f"Invalid face: {face}")
                return

            # Find cubies on this face
            face_cubies = []
            for cubie in self.cubies:
                if abs(cubie.position[axis] - coord) < 0.1:  # Use small threshold for float comparison
                    face_cubies.append(cubie)

            if not face_cubies:
                print(f"No cubies found for face {face}")
                return

            print(f"Found {len(face_cubies)} cubies to rotate")

            # Rotate the cubies
            angle = -90 if clockwise else 90  # Angle in degrees
            angle_rad = math.radians(angle)
            
            # Store original states
            original_states = [(cubie.position.copy(), cubie.colors.copy()) for cubie in face_cubies]
            
            # Perform rotations
            for cubie, (orig_pos, orig_colors) in zip(face_cubies, original_states):
                x, y, z = orig_pos
                
                # Rotate position based on axis
                if axis == 0:  # x-axis rotation (R/L faces)
                    new_y = y * math.cos(angle_rad) - z * math.sin(angle_rad)
                    new_z = y * math.sin(angle_rad) + z * math.cos(angle_rad)
                    cubie.position = [x, new_y, new_z]
                    
                    if clockwise:
                        cubie.colors = [
                            orig_colors[0],  # Right stays
                            orig_colors[1],  # Left stays
                            orig_colors[4],  # Front becomes top
                            orig_colors[5],  # Back becomes bottom
                            orig_colors[3],  # Bottom becomes front
                            orig_colors[2]   # Top becomes back
                        ]
                    else:
                        cubie.colors = [
                            orig_colors[0],  # Right stays
                            orig_colors[1],  # Left stays
                            orig_colors[5],  # Back becomes top
                            orig_colors[4],  # Front becomes bottom
                            orig_colors[2],  # Top becomes front
                            orig_colors[3]   # Bottom becomes back
                        ]
                        
                elif axis == 1:  # y-axis rotation (U/D faces)
                    new_x = x * math.cos(angle_rad) + z * math.sin(angle_rad)
                    new_z = -x * math.sin(angle_rad) + z * math.cos(angle_rad)
                    cubie.position = [new_x, y, new_z]
                    
                    if clockwise:
                        cubie.colors = [
                            orig_colors[4],  # Front becomes right
                            orig_colors[5],  # Back becomes left
                            orig_colors[2],  # Top stays
                            orig_colors[3],  # Bottom stays
                            orig_colors[1],  # Left becomes front
                            orig_colors[0]   # Right becomes back
                        ]
                    else:
                        cubie.colors = [
                            orig_colors[5],  # Back becomes right
                            orig_colors[4],  # Front becomes left
                            orig_colors[2],  # Top stays
                            orig_colors[3],  # Bottom stays
                            orig_colors[0],  # Right becomes front
                            orig_colors[1]   # Left becomes back
                        ]
                        
                else:  # z-axis rotation (F/B faces)
                    new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
                    new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
                    cubie.position = [new_x, new_y, z]
                    
                    if clockwise:
                        cubie.colors = [
                            orig_colors[3],  # Bottom becomes right
                            orig_colors[2],  # Top becomes left
                            orig_colors[0],  # Right becomes top
                            orig_colors[1],  # Left becomes bottom
                            orig_colors[4],  # Front stays
                            orig_colors[5]   # Back stays
                        ]
                    else:
                        cubie.colors = [
                            orig_colors[2],  # Top becomes right
                            orig_colors[3],  # Bottom becomes left
                            orig_colors[1],  # Left becomes top
                            orig_colors[0],  # Right becomes bottom
                            orig_colors[4],  # Front stays
                            orig_colors[5]   # Back stays
                        ]

            print(f"Rotation complete for face {face}")

        except Exception as e:
            print(f"Error rotating face {face}: {e}")
            import traceback
            traceback.print_exc()    

def main():
    try:
        init_pygame_and_gl()
        print("Starting Rubik's Cube...")
        
        # Create the Rubik's cube
        cube = RubiksCube()
        
        # Initialize rotation variables
        rotation_x = 20  # Initial rotation
        rotation_y = -45  # Initial rotation
        last_mouse = None
        mouse_button_down = False
        
        # Game loop
        clock = pygame.time.Clock()
        running = True
        while running:
            try:
                for event in pygame.event.get():
                    try:
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            print(f"Key pressed: {event.key}")  # Debug print
                            if event.key == pygame.K_ESCAPE:
                                running = False
                            elif event.key == pygame.K_SPACE:
                                print("Scrambling cube...")  # Debug print
                                cube.scramble()
                            # Handle face rotation keys
                            elif event.key == pygame.K_f:
                                print("Rotating front face")
                                cube.rotate_face('F', not pygame.key.get_mods() & pygame.KMOD_SHIFT)
                            elif event.key == pygame.K_b:
                                print("Rotating back face")
                                cube.rotate_face('B', not pygame.key.get_mods() & pygame.KMOD_SHIFT)
                            elif event.key == pygame.K_r:
                                print("Rotating right face")
                                cube.rotate_face('R', not pygame.key.get_mods() & pygame.KMOD_SHIFT)
                            elif event.key == pygame.K_l:
                                print("Rotating left face")
                                cube.rotate_face('L', not pygame.key.get_mods() & pygame.KMOD_SHIFT)
                            elif event.key == pygame.K_u:
                                print("Rotating up face")
                                cube.rotate_face('U', not pygame.key.get_mods() & pygame.KMOD_SHIFT)
                            elif event.key == pygame.K_d:
                                print("Rotating down face")
                                cube.rotate_face('D', not pygame.key.get_mods() & pygame.KMOD_SHIFT)
                        # Mouse controls
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:  # Left click
                                last_mouse = pygame.mouse.get_pos()
                                mouse_button_down = True
                                print("Mouse button down")  # Debug print
                        elif event.type == pygame.MOUSEBUTTONUP:
                            if event.button == 1:  # Left click release
                                mouse_button_down = False
                                print("Mouse button up")  # Debug print
                        elif event.type == pygame.MOUSEMOTION and mouse_button_down:
                            current_mouse = pygame.mouse.get_pos()
                            if last_mouse:
                                diff_x = current_mouse[0] - last_mouse[0]
                                diff_y = current_mouse[1] - last_mouse[1]
                                rotation_y += diff_x * 0.5
                                rotation_x += diff_y * 0.5
                                print(f"Rotating view: dx={diff_x}, dy={diff_y}")  # Debug print
                            last_mouse = current_mouse
                            
                    except Exception as e:
                        print(f"Error handling event: {e}")
                        import traceback
                        traceback.print_exc()
                        continue
                
                # Clear the screen and depth buffer
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glLoadIdentity()
                
                # Set up camera and lighting
                glTranslatef(0.0, 0.0, -9.0)
                glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 4.0, 5.0, 0.0])
                
                # Apply rotations
                glRotatef(rotation_x, 1, 0, 0)
                glRotatef(rotation_y, 0, 1, 0)
                
                # Draw the cube
                cube.draw()
                
                # Update the display
                pygame.display.flip()
                
                # Cap the frame rate
                clock.tick(60)
                
            except Exception as e:
                print(f"Error in game loop: {e}")
                import traceback
                traceback.print_exc()
                continue
                
    except Exception as e:
        print(f"Fatal error in main: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        print("Game closed")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)
