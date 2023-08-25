from plist.deps import *
from plist.frame import Frame
from plist.plist import Plist


@dataclass
class Pool:
    name: str
    frames: dict[str, Frame]
    owners: dict[str, Plist]
    plists: list[Plist]

    def __init__(self, name: str, plists: list[Plist]):
        self.name = name
        self.frames = {}
        self.owners = {}
        self.plists = plists
        for plist in plists:
            self.add(plist)

    def add(self, plist: Plist):
        self.plists.append(plist)
        for (name, frame) in plist.frames.items():
            if name in self.frames.keys():
                log.warn(f'Frame {name} already exists in frames')
            else:
                self.frames[name] = frame
                self.owners[name] = plist

    def __str__(self):
        print([name for name in self.frames])

    def dump(self):
        folder = Path(f'{self.name}_dump')
        folder.mkdir(exist_ok=True)
        for frame in self.frames.values():
            log.info(f'Saving image under name {frame.name}')
            frame.dump(folder)

    def replace(self, name: str, new: Frame):
        owner = self.owners[name]
        owner.replace(name, new)

    def find(self, name: str) -> Frame | None:
        if name in self.frames.keys():
            return self.frames[name]
        else:
            return None

    def owner(self, frame: Frame) -> Plist | None:
        if frame.name in self.owners.keys():
            return self.owners[frame.name]
        else:
            return None

    def save(self, path: Path):
        path.mkdir(exist_ok=True)
        for plist in self.plists:
            plist.save(path)
