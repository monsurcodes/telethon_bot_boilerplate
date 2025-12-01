from telethon import events

class Dispatcher:

    def __init__(self, client):
        self.client = client

    def register_handler(self, handler, event_type=events.NewMessage):
        self.client.add_event_handler(handler, event_type)
