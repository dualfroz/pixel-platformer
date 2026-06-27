class State:
    name = "state"

    def onEnter(self, owner, world):
        pass

    def onExit(self, owner, world):
        pass

    def update(self, owner, world):
        return None


class StateMachine:
    def __init__(self, owner):
        self.owner = owner
        self.states = {}
        self.current = None
        self.previous = None
        self.timeInState = 0

    def addState(self, state):
        self.states[state.name] = state
        return self

    def setInitial(self, name, world=None):
        self.current = self.states[name]
        self.timeInState = 0
        if world is not None:
            self.current.onEnter(self.owner, world)
        return self

    def transition(self, name, world):
        if name == self.current.name:
            return
        self.previous = self.current
        self.current.onExit(self.owner, world)
        self.current = self.states[name]
        self.timeInState = 0
        self.current.onEnter(self.owner, world)

    def update(self, world):
        self.timeInState += 1
        nextState = self.current.update(self.owner, world)
        if nextState is not None and nextState != self.current.name:
            self.transition(nextState, world)

    @property
    def stateName(self):
        return self.current.name if self.current else None
