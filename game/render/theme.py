from ..constants import viewWidth, viewHeight

bufferWidth = viewWidth
bufferHeight = viewHeight
renderScale = 3

skyTop = (58, 122, 210)
skyBottom = (150, 205, 255)
caveTop = (24, 20, 40)
caveBottom = (48, 40, 74)

hillFar = (0, 150, 96)
hillNear = (0, 190, 120)
cloudColor = (255, 255, 255)

hudTextColor = (255, 255, 255)
hudShadowColor = (0, 0, 0)
heartFull = (224, 48, 64)
heartEmpty = (70, 30, 34)

tileFallback = {
    "ground": (198, 100, 29),
    "brick": (181, 94, 41),
    "stone": (110, 110, 128),
    "dirt": (120, 72, 40),
    "platform": (217, 164, 65),
    "woodOneWay": (168, 120, 68),
    "spike": (200, 200, 210),
    "lava": (224, 90, 30),
    "ladder": (150, 100, 50),
    "ladderTop": (170, 120, 60),
    "slopeRight": (150, 74, 18),
    "slopeLeft": (150, 74, 18),
}
