from plist.deps import *
from plist.frame import Frame


@dataclass
class Plist:
    name: str
    image: Image
    frames: dict[str, Frame]

    def __init__(self, path: Path, new: bool):
        self.image = open_image(path.with_suffix('.png'))
        data: dict = {}
        with open(path, 'rb') as file:
            data = plist.load(file)

        self.frames = {name: Frame(name, attrs, self.image, new)
                       for (name, attrs) in data['frames'].items()}
        self.name = path.name

    # Replace a frame with a new one.
    def replace(self, name: str, new: Frame):
        old = self.frames[name]
        old.image = new.image
        old.size = new.size

        if not old.size == new.size:
            log.warning(
                f'Replacing image {old.name} ({old.size} vs. {new.size})')

        assert old.size.x >= new.size.x and old.size.y >= new.size.y

        if old.rotated:
            image = new.image.transpose(Transpose.ROTATE_270)
        else:
            image = new.image

        self.image.paste(image, (old.frame[0].x, old.frame[0].y))

    def save(self, path: Path):
        path = path / self.name
        sheet_path = path.with_suffix('.png')
        self.image.save(sheet_path)

        data: dict = {
            'frames': {},
            'metadata': {
                'format': 3,
                'pixelFormat': 'RGBA4444',
                'premultiplyAlpha': False,
                'realTextureFileName': sheet_path.name,
                'size': f'{{{self.image.size[0]},{self.image.size[1]}}}',
                'smartupdate': '',
                'textureFileName': sheet_path.name
            }
        }

        for frame in self.frames.values():
            data['frames'][frame.name] = frame.as_new_dict()

        with open(path, 'wb') as file:
            plist.dump(data, file)
