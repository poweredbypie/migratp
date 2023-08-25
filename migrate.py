import logging as log
from argparse import ArgumentParser
from pathlib import Path

from plist import Plist, Pool


def main():
    parser = ArgumentParser(
        prog='migrate',
        description='Migrate old 2.0 texture pack to 2.1'
    )
    parser.add_argument('pack', type=str)
    parser.add_argument('resources', type=str)
    parser.add_argument('output', type=str)
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()
    log.basicConfig(level=log.DEBUG if args.verbose else log.INFO)
    old = Path(args.pack)
    new = Path(args.resources)

    old_pool = Pool('old', [])
    new_pool = Pool('new', [])

    glob = 'GJ_*-hd.plist'

    for name in old.glob(glob):
        log.info(f'Adding old plist {name}')
        old_pool.add(Plist.from_plist(name))

    for name in new.glob(glob):
        log.info(f'Adding new plist {name}')
        new_pool.add(Plist.from_plist(name))

    found: dict[str, set[str]] = {}
    missing: dict[str, set[str]] = {}

    for frame in old_pool.frames.values():
        plist = old_pool.owner(frame)
        if plist is None:
            log.fatal(f'Could not find owner for frame {frame.name}')
            exit(1)

        if new_pool.find(frame.name) is not None:
            if not plist.name in found:
                found[plist.name] = set()
            found[plist.name].add(frame.name)
        else:
            if not plist.name in missing:
                missing[plist.name] = set()
            missing[plist.name].add(frame.name)

    # old_pool.dump()

    log.info(f"Missing: {missing}")
    log.info(f"Found: {found}")

    all_found: set[str] = set()
    for value in found.values():
        all_found = all_found.union(value)

    for name in all_found:
        frame = old_pool.find(name)
        if frame is None:
            log.fatal(f'Could not find frame from name {name}')
            exit(1)
        new_pool.replace(name, frame)

    new_pool.save(Path(args.output))


if __name__ == '__main__':
    main()
