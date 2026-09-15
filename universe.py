import random

from world_time import Time
from events import EventManager

class Universe:
    def __init__(self):
        self.seed = random.randint(1, 999999)
        self.random = random.Random(self.seed)
        self.event_manager = EventManager(self.random)
        self.time = Time()
