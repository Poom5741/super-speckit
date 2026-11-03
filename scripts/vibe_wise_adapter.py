#!/usr/bin/env python3
"""Inspect pinned VibeWise skills without installing global skills."""
import argparse
import json
import sys
from pathlib import Path
import discipline_contract as discipline


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kit', type=Path, default=discipline.KIT)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('inventory')
    commands.add_parser('catalog')
    read = commands.add_parser('read')
    read.add_argument('name')
    args = parser.parse_args()
    try:
        catalog = discipline.vibe_catalog(args.kit)
        if args.command == 'read':
            result = discipline.read_vibe_skill(args.name, args.kit)
        elif args.command == 'catalog':
            result = catalog
        else:
            result = {'status': 'pass', 'revision': catalog['source_revision'],
                      'skills': len(catalog['skills']), 'runtime_certified': False}
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print('error: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
