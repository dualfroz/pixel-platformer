class InputCommand:
    __slots__ = (
        "left",
        "right",
        "up",
        "down",
        "jump",
        "jumpHeld",
        "dash",
        "run",
        "attack",
        "pause",
        "confirm",
    )

    def __init__(
        self,
        left=False,
        right=False,
        up=False,
        down=False,
        jump=False,
        jumpHeld=False,
        dash=False,
        run=False,
        attack=False,
        pause=False,
        confirm=False,
    ):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.jump = jump
        self.jumpHeld = jumpHeld
        self.dash = dash
        self.run = run
        self.attack = attack
        self.pause = pause
        self.confirm = confirm

    @property
    def moveAxis(self):
        return (1 if self.right else 0) - (1 if self.left else 0)

    @property
    def verticalAxis(self):
        return (1 if self.down else 0) - (1 if self.up else 0)

    def copy(self):
        return InputCommand(
            self.left,
            self.right,
            self.up,
            self.down,
            self.jump,
            self.jumpHeld,
            self.dash,
            self.run,
            self.attack,
            self.pause,
            self.confirm,
        )
