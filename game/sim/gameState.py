from .world import World

MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAMEOVER = "gameover"
COMPLETE = "complete"
VICTORY = "victory"


class Game:
    def __init__(self, levels, rng=None):
        self.levels = list(levels)
        self.levelIndex = 0
        self.mode = MENU
        self.world = None
        self.rng = rng
        self.frame = 0
        self.transitions = []

    def startLevel(self, index):
        self.levelIndex = index
        self.world = World(self.levels[index], rng=self.rng)
        self.setMode(PLAYING)

    def start(self):
        self.startLevel(0)

    def setMode(self, mode):
        if mode != self.mode:
            self.transitions.append((self.mode, mode, self.frame))
        self.mode = mode

    def update(self, command):
        self.frame += 1
        handler = {
            MENU: self.updateMenu,
            PLAYING: self.updatePlaying,
            PAUSED: self.updatePaused,
            GAMEOVER: self.updateGameover,
            COMPLETE: self.updateComplete,
            VICTORY: self.updateVictory,
        }[self.mode]
        handler(command)

    def updateMenu(self, command):
        if command.confirm or command.jump:
            self.start()

    def updatePlaying(self, command):
        if command.pause:
            self.setMode(PAUSED)
            return
        self.world.step(command)
        if self.world.gameOver:
            self.setMode(GAMEOVER)
        elif self.world.completed:
            if self.levelIndex + 1 < len(self.levels):
                self.setMode(COMPLETE)
            else:
                self.setMode(VICTORY)

    def updatePaused(self, command):
        if command.pause:
            self.setMode(PLAYING)

    def updateGameover(self, command):
        if command.confirm:
            self.setMode(MENU)

    def updateComplete(self, command):
        if command.confirm:
            self.startLevel(self.levelIndex + 1)

    def updateVictory(self, command):
        if command.confirm:
            self.levelIndex = 0
            self.setMode(MENU)
