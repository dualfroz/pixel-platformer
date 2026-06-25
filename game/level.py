from .constants import tileSize

tileChars = {
    "X": "ground",
    "#": "brick",
    "=": "platform",
    "L": "pipeTL",
    "R": "pipeTR",
    "l": "pipeBL",
    "r": "pipeBR",
}

entityChars = {"p", "g", "o"}

mainMap = [
    "                                                                ",
    "                                                                ",
    "                        o   o   o                               ",
    "                                              o  o  o            ",
    "        o   o                                                   ",
    "     o  o  o        o o        L R                    o  o       ",
    "     ####          ===         l r          =====               ",
    "                   ===                                          ",
    "  p        #####               l r      g           g          ",
    "                    L R        l r                              ",
    "        g           l r                          g             ",
    "                    l r                                        ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXX    XXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXX    XXXXXXXXXXXXXXXXXXXXX",
]


class Level:
    def __init__(self, tiles, playerSpawn, enemySpawns, coinSpawns):
        self.tiles = tiles
        self.rows = len(tiles)
        self.cols = len(tiles[0])
        self.playerSpawn = playerSpawn
        self.enemySpawns = enemySpawns
        self.coinSpawns = coinSpawns

    def pixelWidth(self):
        return self.cols * tileSize

    def pixelHeight(self):
        return self.rows * tileSize


def parseAscii(rows):
    width = max(len(row) for row in rows)
    padded = [row.ljust(width) for row in rows]
    tiles = [["air"] * width for _ in padded]
    playerSpawn = None
    enemySpawns = []
    coinSpawns = []
    for y, row in enumerate(padded):
        for x, char in enumerate(row):
            if char in tileChars:
                tiles[y][x] = tileChars[char]
            elif char == "p":
                playerSpawn = (x * tileSize, y * tileSize)
            elif char == "g":
                enemySpawns.append((x * tileSize, y * tileSize))
            elif char == "o":
                coinSpawns.append((x * tileSize, y * tileSize))
    return Level(tiles, playerSpawn, enemySpawns, coinSpawns)


def buildLevel():
    return parseAscii(mainMap)


testMap = [
    "          ",
    "          ",
    "     X    ",
    "  p  X    ",
    "     X    ",
    "XXXXXXXXXX",
]


def buildTestLevel():
    return parseAscii(testMap)
