# 3D Rubik's Cube Simulator

An interactive 3x3x3 Rubik's cube you can rotate, scramble, and turn face by face.

## The problem

I wanted to understand 3D rotation math by building something with it instead of reading about it. A Rubik's cube is a clean target: 27 sub-cubes, six face rotations, and every move has to update both geometry (where each cubie sits in space) and state (which colored sticker is now facing which direction). It is a learning project, not a solver and not a speedcubing trainer. The goal was a working simulator with honest, hand-rolled rotation logic.

## The approach

Python with Pygame for the window and input loop, PyOpenGL for the 3D rendering, NumPy for vector math. The cube is 27 `Cubie` objects, each storing a position and a 6-tuple of face colors. Drawing iterates over cubies and emits `GL_QUADS` per visible face, with black `GL_LINE_LOOP` borders for the sticker gaps.

Face rotations are the interesting part. A move like `R` picks the slice of 9 cubies at `x=1`, then applies a 2D rotation matrix (sin/cos around the relevant axis) to each cubie's position. The color tuple gets permuted in the same step so the sticker that was on top ends up facing back, and so on. Each face (`F/B/R/L/U/D`) has its own clockwise and counter-clockwise permutation table, written by hand and checked against a physical cube.

View rotation is decoupled: mouse drag updates two Euler angles applied via `glRotatef` before drawing.

## Controls

- `F / B / R / L / U / D`: rotate that face clockwise. Hold `SHIFT` for counter-clockwise.
- `SPACE`: scramble (20 random moves).
- Mouse drag: orbit the camera.
- `ESC`: quit.

## What it does

- Renders a full 3x3x3 cube with the standard color scheme (white/yellow, red/orange, green/blue).
- All six face rotations in both directions, with correct position and sticker updates.
- 20-move random scramble.
- Mouse-drag view rotation, basic OpenGL lighting, depth testing.

Not implemented: smooth animated rotations, move history, solver, other cube sizes. The `CHECKLIST.md` lists where this could go.

## Run locally

```
pip install -r requirements.txt
python rubiks_cube.py
```

Requires a display (OpenGL context). Tested on Python 3.11 with Pygame 2.5.2, PyOpenGL 3.1.7, NumPy 1.24.3.

## What I learned

- 3D rotation matrices around the principal axes, and why you rotate position and orientation state separately.
- OpenGL fixed-function pipeline basics: matrix stacks, `glPushMatrix` / `glPopMatrix`, normals for lighting, depth test ordering.
- The bookkeeping cost of representing the same object two ways (geometric position plus discrete sticker state) and keeping them consistent across every move.
- Float comparison in geometric code: cubies were getting missed by integer equality after several rotations, so face-selection uses a small epsilon.
- Where Pygame ends and OpenGL begins: Pygame owns the window and events, OpenGL owns everything you see inside it.
