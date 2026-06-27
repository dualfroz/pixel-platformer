from .geometry import clamp


class Camera:
    def __init__(self, viewWidth, viewHeight, worldWidth, worldHeight):
        self.viewWidth = viewWidth
        self.viewHeight = viewHeight
        self.worldWidth = worldWidth
        self.worldHeight = worldHeight
        self.x = 0.0
        self.y = 0.0
        self.deadzoneWidth = viewWidth * 0.28
        self.deadzoneHeight = viewHeight * 0.32
        self.lerp = 0.18
        self.shakeFrames = 0
        self.shakeMagnitude = 0.0

    def setBounds(self, worldWidth, worldHeight):
        self.worldWidth = worldWidth
        self.worldHeight = worldHeight

    def focusOn(self, targetX, targetY):
        self.x = targetX - self.viewWidth * 0.5
        self.y = targetY - self.viewHeight * 0.5
        self.clampToWorld()

    def clampToWorld(self):
        maxX = max(0.0, self.worldWidth - self.viewWidth)
        maxY = max(0.0, self.worldHeight - self.viewHeight)
        self.x = clamp(self.x, 0.0, maxX)
        self.y = clamp(self.y, 0.0, maxY)

    def addShake(self, frames, magnitude):
        self.shakeFrames = max(self.shakeFrames, frames)
        self.shakeMagnitude = max(self.shakeMagnitude, magnitude)

    def update(self, targetX, targetY):
        centerX = self.x + self.viewWidth * 0.5
        centerY = self.y + self.viewHeight * 0.5
        halfDeadX = self.deadzoneWidth * 0.5
        halfDeadY = self.deadzoneHeight * 0.5

        desiredX = self.x
        if targetX < centerX - halfDeadX:
            desiredX = self.x + (targetX - (centerX - halfDeadX))
        elif targetX > centerX + halfDeadX:
            desiredX = self.x + (targetX - (centerX + halfDeadX))

        desiredY = self.y
        if targetY < centerY - halfDeadY:
            desiredY = self.y + (targetY - (centerY - halfDeadY))
        elif targetY > centerY + halfDeadY:
            desiredY = self.y + (targetY - (centerY + halfDeadY))

        self.x += (desiredX - self.x) * self.lerp
        self.y += (desiredY - self.y) * self.lerp
        self.clampToWorld()

        if self.shakeFrames > 0:
            self.shakeFrames -= 1
            if self.shakeFrames == 0:
                self.shakeMagnitude = 0.0

    def offset(self):
        offsetX = self.x
        offsetY = self.y
        if self.shakeFrames > 0:
            wobble = self.shakeMagnitude * (1.0 if self.shakeFrames % 2 == 0 else -1.0)
            offsetX += wobble
            offsetY += wobble * 0.5
        return int(offsetX), int(offsetY)

    def worldToScreen(self, worldX, worldY):
        offsetX, offsetY = self.offset()
        return worldX - offsetX, worldY - offsetY
