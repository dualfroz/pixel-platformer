# Pixel Platformer

A 2D platformer written in Python with pygame. The game logic lives in a headless simulation package (`game/sim`) that never imports pygame: it takes one input command per frame and advances the world by one fixed step. A separate package (`game/render`) draws that world, plays its sound events and reads the keyboard. Movement borrows the forgiving feel of precision platformers: coyote time, jump buffering, a dash, wall slides and wall jumps, a double jump, slopes and one-way platforms. You play a fox explorer across three built-in levels set in a mossy forest at dusk: grass-lipped stone over dark soil layers, carved rune blocks, mossy log ledges, glowing berries to gather and a moonlit sky over misty ridges and pine forests.

## Features

Movement (all values in `game/constants.py`, tuned for 60 steps per second):

- Acceleration-based running with separate ground and air control, friction and a faster run speed.
- Variable jump height: releasing jump while rising cuts the upward speed.
- Coyote time: a jump still works for 6 frames after walking off a ledge.
- Jump buffer: a jump pressed up to 6 frames before landing fires on touchdown.
- One air jump, refilled on landing and on stomping an enemy.
- Dash in the facing or held direction, 10 frames long with a 32 frame cooldown; the player cannot be hurt while dashing.
- Wall slide with a capped fall speed while pushing into a wall, and a wall jump that kicks away from it.
- Fast fall by holding down in the air.
- 45 degree slopes in both directions, with snapping so the player stays on the surface when walking down.
- One-way platforms you can jump up through and drop down through (down + jump).
- Ladders with a one-way ladder top, climbing in both axes and jumping off.
- Moving platforms, solid or one-way, that carry the player horizontally and vertically. They are drawn as floating rune slabs with a dotted track between their endpoints.
- A claw swipe in the facing direction: 9 active frames, a 26 frame cooldown, a reach of 14 pixels to the side. It defeats beetles and chasers in one hit; flyers and shooters shrug it off.

Game:

- Health in hearts, knockback and invulnerability frames after a hit, three lives, checkpoints that move the respawn point, and a level exit.
- Checkpoints are stone lanterns that light up once touched; the exit is a glowing stone arch.
- Locked doors: walking into a door while carrying a key spends the key and opens the door for good. Doors block the player and enemies until opened. The cavern exit sits in a room behind one.
- Hazard tiles: thorns and embers, each with its own damage.
- Four enemy types driven by small state machines, all of which can be stomped:
  - beetle: patrols and turns around at walls and ledges;
  - chaser: patrols, then runs at the player once they come close, and gives up when they get away;
  - flyer: hovers on a sine wave inside a patrol range and homes in on a nearby player;
  - shooter: stands still, aims for a moment and fires a projectile at the player.
- Collectibles: glowing berries, gems, keys (stored in the inventory and spent on doors) and hearts that restore health.
- Game flow: menu, playing, paused, level clear, game over and victory screens.
- Camera with a dead zone, smoothing, clamping to the level and screen shake on hits and stomps.
- Particle bursts for jumps, dashes, stomps, pickups, opened doors and damage.
- Layered parallax backdrop: a dusk gradient with stars and a moon, drifting cloud streaks, misty ridges and two rows of pine forest.
- Sound: the simulation emits named sound events; the renderer turns them into synthesized square-wave tones and stays silent when no audio device is available.
- Levels written as ASCII maps or JSON files, plus a JSON snapshot of a running world (`game/sim/saveLoad.py`).
- The simulation is deterministic: every random source is a seeded `random.Random`.

## Requirements

- Python 3.8 or newer
- pygame 2.1 or newer (tested with pygame 2.6.1 on Python 3.12)

## Install and run

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m game
```

The game renders at 320x180 and scales the window by 3 (960x540).

Render a single frame to a PNG without opening a window. The menu is skipped and a short scripted run is played first:

```sh
python -m game --screenshot frame.png --frames 60
```

## Controls

| Action | Keys |
|---|---|
| Move | Arrow keys or A / D |
| Climb a ladder | Up / Down or W / S |
| Jump (hold for a higher jump) | Space or Z |
| Drop through a one-way platform | Down + Jump |
| Fast fall | Down while in the air |
| Dash | X or Left Shift |
| Run | Hold Left Shift |
| Attack (claw swipe to the side) | C |
| Open a door | Walk into it while carrying a key |
| Pause | Esc or P |
| Confirm on menus | Enter or Space |

## Level format

A level is a list of equal-width strings, one character per 16x16 tile (`game/sim/builtinLevels.py` has three examples). Shorter rows are padded with air.

Tiles:

| Char | Tile | Behaviour |
|---|---|---|
| `X` | ground: mossy stone, with a grass lip when nothing solid is above | solid |
| `D` | dirt: dark soil layers | solid |
| `S` | stone: slate | solid |
| `#` | brick: carved rune block | solid |
| `=` | platform: mossy log | one-way |
| `-` | wood: rope plank | one-way |
| `^` | spike: thorns | hazard, 2 damage |
| `~` | lava: embers | hazard, 3 damage |
| `H` | ladder: vine ladder | climbable |
| `T` | ladder top | climbable, one-way |
| `/` | slope | rises to the right |
| `\` | slope | rises to the left |

Entities:

| Char | Entity |
|---|---|
| `p` | player spawn |
| `b` | beetle |
| `c` | chaser |
| `f` | flyer |
| `s` | shooter |
| `o` | berry |
| `G` | gem |
| `k` | key |
| `v` | heart |
| `@` | checkpoint |
| `E` | exit (when missing, the last checkpoint is the exit) |
| `\|` | locked door; vertically stacked cells form one door |

```python
from game.sim import World, loadLevel, saveLevelJson

level = loadLevel([
    "                    ",
    "  p    o o o     E  ",
    "XXXXXX   ====  XXXXX",
])
saveLevelJson(level, "level.json")
world = World("level.json")
```

`loadLevel` accepts a list of strings, a JSON file path, an already parsed dict or a `Level`. The JSON form stores the collision layer as tile names (`layers.collision`), entity spawns in pixels (`playerSpawn`, `enemies`, `items`, `checkpoints`, `exit`), doors (`doors`, each with `x`, `y`, `w` and `h`) and moving platforms (`platforms`, each with `x`, `y`, `w`, `h`, `toX`, `toY`, `speed` and `oneWay`). Moving platforms have no ASCII character; add them in JSON or in code, as the `skyway` level does.

## Tests

```sh
pip install pytest
python -m pytest
```

59 tests cover geometry, gravity and collisions, slopes, one-way platforms, ladders, hazards, moving platforms, the player's movement rules (coyote time, jump buffer, double jump, dash, wall slide, wall jump, variable jump height), the attack (reach, facing, cooldown, which enemies it defeats) and doors (blocking, opening with a key, one key per door, JSON and ASCII round trips, snapshots). They drive the simulation directly and do not need a display.

There is also a smoke run that plays 640 frames of scripted input on the first level, checks invariants every frame (finite position, health in range, no tile penetration, no falling through the floor) and walks the menu and pause screens:

```sh
python -m game.smoke
```

## Project layout

```
game/
  __main__.py        entry point: play, or --screenshot
  constants.py       movement and gameplay tuning
  smoke.py           scripted smoke run
  sim/               headless simulation, no pygame
    world.py         one world step: platforms, player, doors, attack, enemies, collisions
    player.py        player movement, attack and damage
    door.py          locked doors and their spawns
    physics.py       tile, slope, one-way and platform collision
    enemies.py       enemy types and their states
    stateMachine.py  small state machine used by enemies
    level.py         Level model, ASCII and JSON loading and saving
    tiles.py         tile registry and ASCII legend
    builtinLevels.py meadow, cavern and skyway
    gameState.py     menu, playing, paused, clear, game over, victory
    camera.py, particles.py, audio.py, items.py, inventory.py,
    movingPlatform.py, projectile.py, saveLoad.py, geometry.py, entity.py
  render/            pygame side
    app.py           window, input mapping, main loop, screenshot mode
    renderer.py      tiles, props, sprites, particles, attack swipe
    backdrop.py      sky, moon, clouds, ridges and pine parallax
    art.py           characters and collectibles built in code
    terrainArt.py    forest tileset
    propArt.py       lanterns, exit arch, doors, floating slabs, glows
    hud.py           score, berries, lives, keys, hearts, overlays
    audioBackend.py  synthesized sound effects
    theme.py         render scale and the dusk forest palette
tests/               pytest suite
```

## Limitations

- World snapshots (`saveLoad.py`) are available as an API only; there is no save or load key in the game.
- Levels can carry `background` and `foreground` layers in JSON, but only the collision layer is drawn.
- There is no level editor and no music.
