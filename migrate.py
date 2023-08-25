from plist import Pool, Plist
from pathlib import Path
from sys import argv

import logging as log

def main():
    old = Path(argv[1])
    new = Path(argv[2])

    log.basicConfig(level=log.INFO)

    old_pool = Pool('old', [])
    new_pool = Pool('new', [])

    glob = 'GJ_*-hd.plist'

    for name in old.glob(glob):
        print(f'Adding old plist {name}')
        old_pool.add(Plist(name, False))

    for name in new.glob(glob):
        print(f'Adding new plist {name}')
        new_pool.add(Plist(name, True))
    
    found: dict[str, set[str]] = {}
    missing: dict[str, set[str]] = {}

    for frame in old_pool.frames.values():
        plist = old_pool.owner(frame)
        if new_pool.find(frame.name) is not None:
            if not plist.name in found:
                found[plist.name] = set()
            found[plist.name].add(frame.name)
        else:
            if not plist.name in missing:
                missing[plist.name] = set()
            missing[plist.name].add(frame.name)

    # old_pool.dump()
    
    print("Missing:", missing)
    print("Found:", found)

    all_found: set[str] = set()
    for value in found.values():
        all_found = all_found.union(value)

    for frame in all_found:
        new_pool.replace(frame, old_pool.find(frame))

    new_pool.save(Path('new'))

if __name__ == '__main__':
    main()
