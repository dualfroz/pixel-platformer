from .level import parseAscii, PlatformSpawn

meadowMap = [
    "                                                                ",
    "          o o o o                                               ",
    "                      = = =            o o o                    ",
    "     f                                                          ",
    "                                                    = =         ",
    "        = =        o o o          G           v                 ",
    "   o o                    = =                        o o o      ",
    "  p     b      b     c    @   s        b        f         E     ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
]

cavernMap = [
    "                                        ",
    "              o o o                     ",
    "        TTT       k  @        o o   SSSSS",
    "        HHH      #####              S    ",
    "        HHH        X     ^ ^        |    ",
    "   p    HHH    b   /X    S S  f     |  E ",
    "XXXXXXXXXXXXXXXX~~~~XXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXX~~~~XXXXXXXXXXXXXXXXXXXXX",
    "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
]

skywayMap = [
    "                                                    ",
    "        o o o                     o o o             ",
    "                 = = =                              ",
    "    p                       G                       ",
    "  XXXXXX                              c    @   E    ",
    "  XXXXXX          ^^^^^^          XXXXXXXXXXXXXX     ",
    "  DDDDDD                          DDDDDDDDDDDDDD     ",
    "                                                    ",
]


def buildMeadow():
    level = parseAscii("meadow", meadowMap)
    return level


def buildCavern():
    level = parseAscii("cavern", cavernMap)
    return level


def buildSkyway():
    level = parseAscii("skyway", skywayMap)
    level.platforms.append(PlatformSpawn(9 * 16, 5 * 16, 48, 12, 26 * 16, 5 * 16, 1.1))
    level.platforms.append(PlatformSpawn(20 * 16, 3 * 16, 32, 12, 20 * 16, 1 * 16, 0.9))
    return level


def buildAll():
    return [buildMeadow(), buildCavern(), buildSkyway()]


levelBuilders = {
    "meadow": buildMeadow,
    "cavern": buildCavern,
    "skyway": buildSkyway,
}
