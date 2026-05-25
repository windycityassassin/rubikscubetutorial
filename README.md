# 3D Rubik's Cube Simulator

An interactive 3x3x3 Rubik's cube you can rotate, scramble, and turn face by face.

**Live demo (browser):** https://windycityassassin.github.io/rubikscubetutorial/

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

Not implemented in the Python: smooth animated rotations, move history, solver, other cube sizes. The browser version below adds animated turns and a solver; `CHECKLIST.md` lists what else could go in.

## Run locally

```
pip install -r requirements.txt
python rubiks_cube.py
```

Requires a display (OpenGL context). Tested on Python 3.11 with Pygame 2.5.2, PyOpenGL 3.1.7, NumPy 1.24.3.

## Browser version

The desktop app needs OpenGL, which makes it awkward to share. `docs/index.html` is a single-file JavaScript port using Three.js, served from GitHub Pages at the URL above. Same controls (`F/B/R/L/U/D`, hold `Shift` for inverse, `Space` to scramble, drag to orbit), same color scheme, no install.

The JS version drops the hand-rolled color-permutation tables. It reparents the 9 face cubies into a temporary `THREE.Group` pivot, animates the pivot's rotation over 180&nbsp;ms, then bakes the world transform back onto each cubie and re-rounds positions to the integer lattice. Three.js's matrix math handles sticker orientation for free. A `snapQuaternion` step rounds each cubie's orientation to the nearest 90-degree multiple after every turn so float drift can't accumulate over a long scramble.

## Solver and tutorial

Hit **Solve** (or press `Enter`) to watch the cube solve itself. The solver is [cubejs](https://github.com/ldez/cubejs), a JS port of Kociemba's two-phase algorithm. State extraction walks each cubie, asks "which of my six local face normals currently points along the world `+y` axis?" using the cubie's snapped quaternion, then reads the color letter stored in `material.userData.faceLetter` at that index. The 54-character facelet string goes to `Cube.fromString(s).solve()`, which returns a near-optimal solution in ~20 moves. The solution is parsed (`R'` → inverse, `U2` → two quarter-turns) and queued through the same animation pipeline as a manual scramble. A horizontal move strip highlights the current step.

The **how to solve** link in the header opens an inline tutorial covering notation (`F`/`F'`/`F2`) and the four phases of the Beginner's Method (white cross, white corners, middle layer edges, last layer) with the trigger algorithms. Kociemba's solution is shorter; Beginner's is what a human can actually understand and execute.

## What I learned

- 3D rotation matrices around the principal axes, and why you rotate position and orientation state separately.
- OpenGL fixed-function pipeline basics: matrix stacks, `glPushMatrix` / `glPopMatrix`, normals for lighting, depth test ordering.
- The bookkeeping cost of representing the same object two ways (geometric position plus discrete sticker state) and keeping them consistent across every move.
- Float comparison in geometric code: cubies were getting missed by integer equality after several rotations, so face-selection uses a small epsilon.
- Where Pygame ends and OpenGL begins: Pygame owns the window and events, OpenGL owns everything you see inside it.
