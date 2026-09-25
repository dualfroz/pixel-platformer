import array
import math

import pygame

toneTable = {
    "jump": (660, 90),
    "doubleJump": (820, 90),
    "dash": (300, 80),
    "stomp": (200, 120),
    "pickup": (900, 70),
    "hurt": (160, 160),
    "die": (110, 300),
    "shoot": (420, 70),
    "checkpoint": (1040, 120),
    "levelComplete": (760, 260),
    "spark": (520, 40),
    "slash": (1240, 45),
    "doorOpen": (240, 180),
}


def synthTone(frequency, milliseconds, volume=0.25):
    mixerInfo = pygame.mixer.get_init()
    if mixerInfo is None:
        return None
    sampleRate, _, channels = mixerInfo
    frames = int(sampleRate * milliseconds / 1000.0)
    amplitude = int(32767 * volume)
    samples = array.array("h")
    for index in range(frames):
        envelope = 1.0 - index / frames
        value = int(amplitude * envelope * (1.0 if math.sin(2.0 * math.pi * frequency * index / sampleRate) >= 0 else -1.0))
        for _ in range(max(1, channels)):
            samples.append(value)
    return pygame.mixer.Sound(buffer=samples.tobytes())


class PygameAudio:
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            for name, (frequency, duration) in toneTable.items():
                sound = synthTone(frequency, duration)
                if sound is not None:
                    self.sounds[name] = sound
            self.enabled = bool(self.sounds)
        except pygame.error:
            self.enabled = False

    def sink(self, event):
        if not self.enabled:
            return
        sound = self.sounds.get(event.name)
        if sound is not None:
            sound.play()


class NullAudio:
    enabled = False

    def sink(self, event):
        pass


def buildAudioSink():
    backend = PygameAudio()
    if backend.enabled:
        return backend.sink
    return NullAudio().sink
