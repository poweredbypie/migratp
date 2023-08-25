from plist.deps import *
from plist.coord import Coord

def coord_pair(str: str) -> tuple[Coord, Coord]:
    log.debug(f'Creating coordinate pair from string {str}')
    matched = re.match('{({.*}),({.*})}', str)
    first = matched.group(1)
    second = matched.group(2)
    return (Coord(first), Coord(second))

@dataclass
class Frame:
    name: str
    image: Image
    frame: tuple[Coord, Coord]
    offset: Coord
    rotated: bool
    size: Coord

    def __init__(self, name: str, attrs: dict, image: Image, new: bool):
        log.debug(f'Creating frame with name {name}')
        self.name = name
        self.frame = coord_pair(attrs['textureRect' if new else 'frame'])
        self.offset = Coord(attrs['spriteOffset' if new else 'offset'])
        self.rotated = attrs['textureRotated' if new else 'rotated']
        self.size = self.frame[1]

        left = self.frame[0].x
        top = self.frame[0].y
        over = self.frame[1].x
        down = self.frame[1].y
        if not self.rotated:
            bottom = top + down
            right = left + over
        else:
            bottom = top + over
            right = left + down
        self.image = image.crop((left, top, right, bottom))

        if self.rotated:
            self.image = self.image.transpose(Transpose.ROTATE_90)
    
    def dump(self, folder: Path):
        self.image.save(folder / self.name)

    def as_new_dict(self) -> dict:
        return {
            'aliases': [],
            'spriteOffset': str(self.offset),
            'spriteSize': str(self.size),
            'spriteSourceSize': str(self.size),
            'textureRect': f'{{{self.frame[0]},{self.size}}}',
            'textureRotated': self.rotated
        }