import json


def captureState(world):
    player = world.player
    return {
        "level": world.level.name,
        "frame": world.frame,
        "score": world.score,
        "berries": world.berries,
        "lives": world.lives,
        "gameOver": world.gameOver,
        "completed": world.completed,
        "active": world.active,
        "activatedCheckpoints": sorted(world.activatedCheckpoints),
        "player": {
            "x": player.x,
            "y": player.y,
            "vx": player.vx,
            "vy": player.vy,
            "hp": player.hp,
            "maxHp": player.maxHp,
            "facing": player.facing,
            "score": player.score,
            "berries": player.berries,
            "iframes": player.iframes,
            "airJumps": player.airJumps,
            "spawnX": player.spawnX,
            "spawnY": player.spawnY,
            "inventory": player.inventory.asDict(),
        },
        "items": [item.collected for item in world.items],
        "doors": [door.open for door in world.doors],
        "enemies": [
            {
                "kind": enemy.kind,
                "x": enemy.x,
                "y": enemy.y,
                "vx": enemy.vx,
                "vy": enemy.vy,
                "direction": enemy.direction,
                "alive": enemy.alive,
                "hp": enemy.hp,
                "state": enemy.machine.stateName,
            }
            for enemy in world.enemies
        ],
        "platforms": [
            {
                "progress": platform.progress,
                "direction": platform.direction,
                "x": platform.x,
                "y": platform.y,
            }
            for platform in world.platforms
        ],
    }


def applyState(world, state):
    world.frame = state["frame"]
    world.score = state["score"]
    world.berries = state["berries"]
    world.lives = state["lives"]
    world.gameOver = state["gameOver"]
    world.completed = state["completed"]
    world.active = state.get("active", True)
    world.activatedCheckpoints = set(state["activatedCheckpoints"])

    player = world.player
    saved = state["player"]
    player.x = saved["x"]
    player.y = saved["y"]
    player.vx = saved["vx"]
    player.vy = saved["vy"]
    player.hp = saved["hp"]
    player.maxHp = saved["maxHp"]
    player.facing = saved["facing"]
    player.score = saved["score"]
    player.berries = saved["berries"]
    player.iframes = saved["iframes"]
    player.airJumps = saved["airJumps"]
    player.spawnX = saved["spawnX"]
    player.spawnY = saved["spawnY"]
    player.inventory.loadDict(saved["inventory"])

    for item, collected in zip(world.items, state["items"]):
        item.collected = collected

    for door, opened in zip(world.doors, state.get("doors", [])):
        door.open = opened
    world.refreshColliders()

    for enemy, record in zip(world.enemies, state["enemies"]):
        enemy.x = record["x"]
        enemy.y = record["y"]
        enemy.vx = record["vx"]
        enemy.vy = record["vy"]
        enemy.direction = record["direction"]
        enemy.alive = record["alive"]
        enemy.hp = record["hp"]
        stateName = record["state"]
        if stateName is not None and stateName in enemy.machine.states:
            enemy.machine.current = enemy.machine.states[stateName]

    for platform, record in zip(world.platforms, state["platforms"]):
        platform.progress = record["progress"]
        platform.direction = record["direction"]
        platform.x = record["x"]
        platform.y = record["y"]

    return world


def saveGame(world, path):
    with open(path, "w", encoding="ascii") as handle:
        json.dump(captureState(world), handle, indent=2)


def loadGameInto(world, path):
    with open(path, "r", encoding="ascii") as handle:
        state = json.load(handle)
    return applyState(world, state)
