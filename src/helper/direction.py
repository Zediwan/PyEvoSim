from __future__ import annotations

import enum


class ExtendedEnum(enum.Enum):
    @classmethod
    def get_options(cls):
        return list(map(lambda c: c.value, cls))


class Direction(ExtendedEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @staticmethod
    def is_valid_direction(direction: Direction) -> bool:
        return direction in Direction.get_options()

    @staticmethod
    def get_neighboring_directions(direction: Direction) -> list[Direction]:
        if direction == Direction.NORTH:
            return [Direction.WEST, Direction.EAST]
        elif direction == Direction.EAST:
            return [Direction.NORTH, Direction.SOUTH]
        elif direction == Direction.SOUTH:
            return [Direction.WEST, Direction.EAST]
        elif direction == Direction.WEST:
            return [Direction.NORTH, Direction.SOUTH]
        else:
            raise ValueError("Invalid direction provided")
