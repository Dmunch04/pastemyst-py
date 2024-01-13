from trio import Lock, Event


class HoldableLock:
    __slots__ = ("lock", "unlock")

    def __init__(self, lock: Lock):
        self.lock = lock
        self.unlock = True

    def hold(self) -> None:
        self.unlock = False

    async def __aenter__(self) -> "HoldableLock":
        await self.lock.acquire()
        return self

    async def __aexit__(self, *args) -> "HoldableLock":
        if self.unlock:
            self.lock.release()


class GlobalLock:
    __slots__ = ("global_event", "is_global")

    def __init__(self, global_event: Event, is_global: bool):
        self.global_event = global_event
        self.is_global = is_global

    def __enter__(self):
        if self.is_global:
            self.global_event.clear()

    def __exit__(self, *args):
        if self.is_global:
            self.global_event.set()
