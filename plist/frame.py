from plist.coord import Coord
from plist.deps import *

coord_regex = re.compile('{({.*}),({.*})}')


def coord_pair(coords: str) -> tuple[Coord, Coord] | None:
    log.debug(f'Creating coordinate pair from string {coords}')
    matched = coord_regex.match(coords)
    if matched is None:
        return None

    first = Coord.from_str(matched.group(1))
    second = Coord.from_str(matched.group(2))
    if first is None or second is None:
        return None
    else:
        return (first, second)


class NewFrameDict(types.TypedDict):
    aliases: list[str]
    textureRect: str
    spriteOffset: str
    spriteSize: str
    spriteSourceSize: str
    textureRotated: bool


class OldFrameDict(types.TypedDict):
    frame: str
    offset: str
    rotated: bool


@dataclass
class Frame:
    name: str
    image: Image
    frame: tuple[Coord, Coord]
    offset: Coord
    rotated: bool
    size: Coord

    @staticmethod
    def from_values(name: str, image: Image, frame: str, offset: str, rotated: bool) -> types.Union['Frame', None]:
        log.debug(f'Creating frame {name} from values')
        frame_pair = coord_pair(frame)
        if frame_pair is None:
            return None

        offset_coord = Coord.from_str(offset)
        if offset_coord is None:
            return None

        left = frame_pair[0].x
        top = frame_pair[0].y
        over = frame_pair[1].x
        down = frame_pair[1].y
        if not rotated:
            bottom = top + down
            right = left + over
        else:
            bottom = top + over
            right = left + down
        image = image.crop((left, top, right, bottom))
        if rotated:
            image = image.transpose(Transpose.ROTATE_90)

        return Frame(
            name=name,
            image=image,
            frame=frame_pair,
            offset=offset_coord,
            rotated=rotated,
            size=frame_pair[1]
        )

    @staticmethod
    def from_dict(name: str, attrs: NewFrameDict | OldFrameDict, image: Image) -> types.Union['Frame', None]:
        if 'textureRect' in attrs:
            return Frame.from_values(name, image, attrs['textureRect'], attrs['spriteOffset'], attrs['textureRotated'])
        else:
            return Frame.from_values(name, image, attrs['frame'], attrs['offset'], attrs['rotated'])

    def dump(self, folder: Path):
        self.image.save(folder / self.name)

    def as_new_dict(self) -> NewFrameDict:
        return {
            'aliases': [],
            'spriteOffset': str(self.offset),
            'spriteSize': str(self.size),
            'spriteSourceSize': str(self.size),
            'textureRect': f'{{{self.frame[0]},{self.size}}}',
            'textureRotated': self.rotated
        }
