AIR = "air"


class TileDef:
    __slots__ = ("name", "solid", "oneWay", "hazard", "ladder", "slope", "damage")

    def __init__(self, name, solid=False, oneWay=False, hazard=False, ladder=False, slope=None, damage=0):
        self.name = name
        self.solid = solid
        self.oneWay = oneWay
        self.hazard = hazard
        self.ladder = ladder
        self.slope = slope
        self.damage = damage


tileRegistry = {
    AIR: TileDef(AIR),
    "ground": TileDef("ground", solid=True),
    "brick": TileDef("brick", solid=True),
    "stone": TileDef("stone", solid=True),
    "dirt": TileDef("dirt", solid=True),
    "platform": TileDef("platform", oneWay=True),
    "woodOneWay": TileDef("woodOneWay", oneWay=True),
    "spike": TileDef("spike", hazard=True, damage=2),
    "lava": TileDef("lava", hazard=True, damage=3),
    "ladder": TileDef("ladder", ladder=True),
    "ladderTop": TileDef("ladderTop", ladder=True, oneWay=True),
    "slopeRight": TileDef("slopeRight", slope="ascendRight"),
    "slopeLeft": TileDef("slopeLeft", slope="ascendLeft"),
}


asciiToTile = {
    "X": "ground",
    "#": "brick",
    "S": "stone",
    "D": "dirt",
    "=": "platform",
    "-": "woodOneWay",
    "^": "spike",
    "~": "lava",
    "H": "ladder",
    "T": "ladderTop",
    "/": "slopeRight",
    "\\": "slopeLeft",
}

tileToAscii = {value: key for key, value in asciiToTile.items()}


asciiEntities = {
    "p": "playerSpawn",
    "b": "beetle",
    "c": "chaser",
    "f": "flyer",
    "s": "shooter",
    "o": "berry",
    "G": "gem",
    "k": "key",
    "v": "heart",
    "@": "checkpoint",
    "E": "exit",
    "|": "door",
}


def tileDef(name):
    return tileRegistry.get(name, tileRegistry[AIR])


def isSolidName(name):
    return tileRegistry[name].solid if name in tileRegistry else False


def isOneWayName(name):
    return tileRegistry[name].oneWay if name in tileRegistry else False


def isHazardName(name):
    return tileRegistry[name].hazard if name in tileRegistry else False


def isLadderName(name):
    return tileRegistry[name].ladder if name in tileRegistry else False


def slopeKind(name):
    definition = tileRegistry.get(name)
    return definition.slope if definition else None
