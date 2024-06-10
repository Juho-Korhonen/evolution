import uuid


class Creature:
    def __init__(self, energy) -> None:
        self.energy = energy
        self.identifier = uuid.uuid4()
        self.location = []