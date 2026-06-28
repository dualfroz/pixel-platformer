import pygame

from .theme import hudTextColor, hudShadowColor, heartFull, heartEmpty


class Hud:
    def __init__(self):
        self.font = pygame.font.Font(None, 22)
        self.bigFont = pygame.font.Font(None, 48)

    def drawText(self, surf, text, pos, color=hudTextColor):
        shadow = self.font.render(text, True, hudShadowColor)
        label = self.font.render(text, True, color)
        surf.blit(shadow, (pos[0] + 1, pos[1] + 1))
        surf.blit(label, pos)

    def drawCentered(self, surf, text, y, color=hudTextColor):
        label = self.bigFont.render(text, True, color)
        shadow = self.bigFont.render(text, True, hudShadowColor)
        x = (surf.get_width() - label.get_width()) // 2
        surf.blit(shadow, (x + 2, y + 2))
        surf.blit(label, (x, y))

    def drawHearts(self, surf, hp, maxHp):
        for index in range(maxHp):
            color = heartFull if index < hp else heartEmpty
            x = 10 + index * 16
            y = 30
            pygame.draw.circle(surf, color, (x + 3, y + 3), 3)
            pygame.draw.circle(surf, color, (x + 8, y + 3), 3)
            pygame.draw.polygon(surf, color, [(x, y + 4), (x + 11, y + 4), (x + 5, y + 11)])

    def draw(self, surf, world):
        self.drawText(surf, "SCORE %06d" % world.score, (10, 8))
        self.drawText(surf, "COINS x%02d" % world.coins, (surf.get_width() - 130, 8))
        self.drawText(surf, "LIVES %d" % world.lives, (surf.get_width() - 130, 30))
        self.drawHearts(surf, world.player.hp, world.player.maxHp)

    def drawOverlay(self, surf, mode):
        veil = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 140))
        surf.blit(veil, (0, 0))
        messages = {
            "menu": "PIXEL PLATFORMER",
            "paused": "PAUSED",
            "gameover": "GAME OVER",
            "complete": "LEVEL CLEAR",
            "victory": "YOU WIN",
        }
        self.drawCentered(surf, messages.get(mode, ""), surf.get_height() // 2 - 40)
        self.drawCentered(surf, "PRESS ENTER", surf.get_height() // 2 + 12)
