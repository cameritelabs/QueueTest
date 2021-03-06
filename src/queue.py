from typing import Any


class Empty(Exception):
    def __init__(self) -> None:
        super().__init__("Queue is empty")


class Full(Exception):
    def __init__(self) -> None:
        super().__init__("Queue is full")


class RepeatedMessage(Exception):
    def __init__(self) -> None:
        super().__init__("The message is already registered on queue")


class DeleteAttemptToUnknownMessage(Exception):
    def __init__(self) -> None:
        super().__init__(
            "The message you tried to delete was already deleted or don't exists"
        )


class QueueMessage:
    def __init__(self, id: str, content: Any):
        self.id = id
        self.content = content


class Queue(object):
    pass