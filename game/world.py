import pygame

from .constants import (
    tileSize,
    bufferWidth,
    bufferHeight,
    renderScale,
    skyColor,
    stompBounce,
)
from .art import buildSprites
from .entities import Player, Enemy, Coin


class MoveInput:
    def __init__(self, left=False, right=False, jump=False):
        self.left = left
        self.right = right
        self.jump = jump


class World:
    def __init__(self, level, sprites=None):
        self.level = level
        self.tiles = level.tiles
        self.cols = level.cols
        self.rows = level.rows
        self.sprites = sprites if sprites is not None else buildSprites()
        self.player = Player(*level.playerSpawn)
        self.enemies = [Enemy(x, y) for (x, y) in level.enemySpawns]
        self.coins = [Coin(x, y) for (x, y) in level.coinSpawns]
        self.score = 0
        self.coinCount = 0

    def solidAt(self, col, row):
        if col < 0 or col >= self.cols:
            return True
        if row < 0 or row >= self.rows:
            return False
        return self.tiles[row][col] != "air"

    def solidCellsOverlapping(self, box):
        leftCol = box.left // tileSize
        rightCol = box.right // tileSize
        topRow = box.top // tileSize
        bottomRow = box.bottom // tileSize
        cells = []
        for row in range(topRow, bottomRow + 1):
            for col in range(leftCol, rightCol + 1):
                if self.solidAt(col, row):
                    cells.append(pygame.Rect(col * tileSize, row * tileSize, tileSize, tileSize))
        return cells

    def step(self, moveInput):
        self.player.update(self, moveInput)
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(self)
        self.resolveEnemies()
        self.resolveCoins()

    def resolveEnemies(self):
        playerBox = self.player.rect()
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            enemyBox = enemy.rect()
            if not playerBox.colliderect(enemyBox):
                continue
            stomping = self.player.vy > 0 and (playerBox.bottom - enemyBox.top) < 10
            if stomping:
                enemy.alive = False
                self.player.vy = stompBounce
                self.score += 100
            else:
                self.player.alive = False

    def resolveCoins(self):
        playerBox = self.player.rect()
        for coin in self.coins:
            if coin.collected:
                continue
            if playerBox.colliderect(coin.rect()):
                coin.collected = True
                self.coinCount += 1
                self.score += 200

    def cameraOffset(self):
        camX = int(self.player.x + self.player.width / 2 - bufferWidth / 2)
        camY = int(self.player.y + self.player.height / 2 - bufferHeight / 2)
        camX = max(0, min(camX, self.level.pixelWidth() - bufferWidth))
        camY = max(0, min(camY, self.level.pixelHeight() - bufferHeight))
        return camX, camY

    def drawBackground(self, buffer, camX):
        buffer.fill(skyColor)
        for hillX in (40, 220, 430, 620):
            screenX = hillX - camX // 2
            pygame.draw.ellipse(buffer, (0, 168, 68), (screenX, bufferHeight - 46, 120, 70))
            pygame.draw.ellipse(buffer, (0, 200, 84), (screenX + 18, bufferHeight - 40, 84, 60))
        for cloudX in (90, 260, 470, 640):
            screenX = cloudX - camX // 3
            pygame.draw.ellipse(buffer, (255, 255, 255), (screenX, 26, 46, 20))
            pygame.draw.ellipse(buffer, (255, 255, 255), (screenX + 18, 18, 40, 24))
            pygame.draw.ellipse(buffer, (255, 255, 255), (screenX + 34, 28, 34, 18))

    def render(self):
        buffer = pygame.Surface((bufferWidth, bufferHeight))
        camX, camY = self.cameraOffset()
        self.drawBackground(buffer, camX)

        firstCol = max(0, camX // tileSize)
        lastCol = min(self.cols, (camX + bufferWidth) // tileSize + 1)
        firstRow = max(0, camY // tileSize)
        lastRow = min(self.rows, (camY + bufferHeight) // tileSize + 1)
        for row in range(firstRow, lastRow):
            for col in range(firstCol, lastCol):
                tile = self.tiles[row][col]
                if tile == "air":
                    continue
                buffer.blit(self.sprites[tile], (col * tileSize - camX, row * tileSize - camY))

        for coin in self.coins:
            if not coin.collected:
                buffer.blit(self.sprites["coin"], (coin.x - camX, coin.y - camY))

        for enemy in self.enemies:
            if not enemy.alive:
                continue
            sprite = self.sprites["goomba"]
            if enemy.direction > 0:
                sprite = pygame.transform.flip(sprite, True, False)
            buffer.blit(sprite, (int(enemy.x) - camX, int(enemy.y) - camY))

        playerSprite = self.sprites["player"]
        if self.player.facing < 0:
            playerSprite = pygame.transform.flip(playerSprite, True, False)
        buffer.blit(playerSprite, (int(self.player.x) - 2 - camX, int(self.player.y) - camY))

        scaled = pygame.transform.scale(
            buffer, (bufferWidth * renderScale, bufferHeight * renderScale)
        )
        self.drawHud(scaled)
        return scaled

    def drawHud(self, surf):
        font = pygame.font.Font(None, 24)
        scoreText = "SCORE %06d" % self.score
        coinText = "COINS x%02d" % self.coinCount
        for label, pos in ((scoreText, (10, 8)), (coinText, (surf.get_width() - 132, 8))):
            shadow = font.render(label, True, (0, 0, 0))
            text = font.render(label, True, (255, 255, 255))
            surf.blit(shadow, (pos[0] + 1, pos[1] + 1))
            surf.blit(text, pos)
