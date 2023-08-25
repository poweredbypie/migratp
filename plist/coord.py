from __future__ import annotations

import logging as log
import re
from dataclasses import dataclass

coord_regex = re.compile('{([0-9-.]+),([0-9-.]+)}')


@dataclass
class Coord:
    x: int
    y: int

    @staticmethod
    def from_str(coord: str) -> Coord | None:
        log.debug(f'Initializing coord from string {coord}')
        matched = coord_regex.match(coord)
        if matched is None:
            return None

        x = matched.group(1)
        y = matched.group(2)
        return Coord(
            x=int(float(x)),
            y=int(float(y))
        )

    def __str__(self):
        return f'{{{self.x},{self.y}}}'
