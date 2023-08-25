from plist.deps import *


@dataclass
class Coord:
    x: int
    y: int

    def __init__(self, str: str):
        log.debug(f'Initializing coord from string {str}')
        matched = re.match('{([0-9-.]+),([0-9-.]+)}', str)
        x = matched.group(1)
        y = matched.group(2)
        self.x = int(float(x))
        self.y = int(float(y))

    def __eq__(self, other: 'Coord'):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'{{{self.x},{self.y}}}'
