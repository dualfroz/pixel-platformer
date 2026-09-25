from ..constants import viewWidth, viewHeight

bufferWidth = viewWidth
bufferHeight = viewHeight
renderScale = 3

skyTop = (28, 36, 68)
skyMiddle = (86, 78, 128)
skyBottom = (196, 146, 150)
caveTop = (24, 20, 40)
caveBottom = (48, 40, 74)

moonColor = (240, 228, 196)
moonShade = (214, 196, 170)
moonGlow = (240, 228, 196, 36)
starColor = (226, 222, 255)

ridgeFar = (78, 74, 118)
ridgeFarLight = (98, 90, 138)
forestMid = (44, 66, 86)
forestNear = (26, 46, 56)
mistColor = (208, 170, 184, 70)
cloudColor = (236, 186, 190)
cloudShade = (178, 132, 156)

hudTextColor = (246, 238, 226)
hudShadowColor = (20, 14, 30)
heartFull = (232, 70, 96)
heartEmpty = (70, 34, 50)

grassLight = (176, 220, 102)
grassMid = (112, 176, 74)
grassDark = (58, 116, 60)
mossLight = (128, 168, 84)
mossDark = (74, 112, 66)
stoneLight = (118, 128, 122)
stoneMid = (88, 98, 96)
stoneDark = (60, 68, 72)
stoneCrack = (42, 48, 56)
soilLight = (92, 64, 64)
soilMid = (66, 46, 52)
soilDark = (46, 32, 42)
soilPebble = (120, 104, 98)
rootColor = (104, 72, 52)
slateLight = (128, 138, 162)
slateMid = (96, 104, 128)
slateDark = (64, 70, 94)
runeBase = (58, 84, 104)
runeLight = (104, 144, 160)
runeDark = (36, 54, 72)
runeGlow = (130, 236, 214)
barkLight = (138, 100, 78)
barkMid = (106, 74, 60)
barkDark = (70, 48, 44)
plankLight = (176, 136, 96)
plankDark = (118, 84, 62)
ropeColor = (206, 184, 140)
thornLight = (214, 196, 214)
thornDark = (110, 70, 104)
emberLight = (255, 200, 120)
emberMid = (236, 98, 52)
emberDark = (150, 40, 52)

berryBody = (212, 58, 132)
berryLight = (255, 168, 212)
berryShade = (140, 30, 96)
berryGlow = (255, 120, 196, 60)
leafColor = (96, 178, 86)

lanternStone = (110, 116, 128)
lanternStoneDark = (70, 74, 88)
lanternOff = (44, 50, 66)
lanternOn = (255, 206, 112)
lanternCore = (255, 244, 204)
lanternGlow = (255, 196, 96, 54)

portalStone = (124, 130, 150)
portalStoneDark = (74, 78, 100)
portalInner = (40, 92, 110)
portalLight = (150, 240, 222)

doorWood = (128, 86, 58)
doorWoodDark = (86, 56, 42)
doorBand = (66, 70, 86)
doorBandLight = (124, 130, 146)
doorLock = (240, 200, 90)
doorwayShadow = (18, 22, 30)

slashColor = (250, 244, 226)
slashTrail = (150, 236, 220)
trackColor = (130, 236, 214)

tileFallback = {
    "ground": stoneMid,
    "brick": runeBase,
    "stone": slateMid,
    "dirt": soilMid,
    "platform": barkMid,
    "woodOneWay": plankLight,
    "spike": thornDark,
    "lava": emberMid,
    "ladder": barkMid,
    "ladderTop": barkLight,
    "slopeRight": stoneMid,
    "slopeLeft": stoneMid,
}
