class SoundEvent:
    __slots__ = ("name", "x", "frame")

    def __init__(self, name, x, frame):
        self.name = name
        self.x = x
        self.frame = frame


class AudioBus:
    def __init__(self, sink=None, historyCap=64):
        self.sink = sink
        self.events = []
        self.historyCap = historyCap
        self.frame = 0
        self.totalEmitted = 0

    def setSink(self, sink):
        self.sink = sink

    def tick(self):
        self.frame += 1

    def play(self, name, x=None):
        event = SoundEvent(name, x, self.frame)
        self.events.append(event)
        if len(self.events) > self.historyCap:
            self.events.pop(0)
        self.totalEmitted += 1
        if self.sink is not None:
            self.sink(event)

    def drain(self):
        drained = self.events
        self.events = []
        return drained
