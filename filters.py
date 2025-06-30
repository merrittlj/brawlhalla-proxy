from enum import Enum

DIR_C2S = 0
DIR_S2C = 1

class Filters:
    class Mode(Enum):
        REGEX = 0
        STARTSWITH = 1
        EXACT = 2
        BYTES = 3

    _filters = {
        DIR_C2S: [],
        DIR_S2C: []
    }

    @classmethod
    def register(cls, direction: int, pattern: bytes, mode: int, callback):
        entry = (pattern, mode, callback)
        cls._filters[direction].append(entry)
        return entry  # Return handle for unregistering

    @classmethod
    def unregister(cls, direction: int, handle):
        if handle in cls._filters[direction]:
            cls._filters[direction].remove(handle)

    @classmethod
    def apply(cls, direction: int, data: bytes) -> bytes:
        for pattern, mode, callback in cls._filters[direction]:
            if mode == cls.Mode.REGEX:
                if re.match(pattern, data):
                    data = callback(data)
            elif mode == cls.Mode.STARTSWITH:
                if data.startswith(pattern):
                    data = callback(data)
            elif mode == cls.Mode.EXACT:
                if data == pattern:
                    data = callback(data)
            elif mode == cls.Mode.BYTES:
                if pattern in data:
                    callback(data)
        return data
