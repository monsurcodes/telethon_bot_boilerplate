from abc import ABC, abstractmethod

class BasePlugin(ABC):

    def __init__(self, bot):
        self.bot = bot

    @abstractmethod
    def register(self):
        pass
