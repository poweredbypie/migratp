import logging as log
from argparse import ArgumentParser
from pathlib import Path
from sys import argv

from plist import Plist, Pool


def main():
    parser = ArgumentParser(
        prog='migrate',
        description='Migrate old 2.0 texture pack to 2.1'
    )
    parser.add_argument('pack')
    parser.add_argument('resources')

    args = parser.parse_args()
    old = Path(args.pack)
    new = Path(args.resources)

    # Kid named camel case
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
