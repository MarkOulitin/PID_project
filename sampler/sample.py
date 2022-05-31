import uuid


class Sample:
    def __init__(self, path: str, value: str, id=None):
        self.id = id
        self.path = path
        self.value = value
        self.id = id if id else str(uuid.uuid4())
