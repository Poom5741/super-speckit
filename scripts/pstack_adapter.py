#!/usr/bin/env python3
"""Pinned-source inventory and progressive routing; never a second coordinator."""
from __future__ import annotations
import argparse
import hashlib
import json
import stat
from pathlib import Path
import sys

KIT = Path(__file__).resolve().parents[1]
GROUPS = ('skills', 'principles', 'playbooks', 'agents', 'automations')

def read_json(path):
    return json.loads(path.read_text())

def verify_source(kit=KIT):
    manifest = read_json(kit / 'vendor/pstack-manifest.json')
    vendor = kit / manifest['root']
    expected = {row['path']: row for row in manifest['files']}
    actual = {p.relative_to(vendor).as_posix() for p in vendor.rglob('*') if p.is_file()}
    failures = [f'missing: {p}' for p in sorted(set(expected) - actual)]
    failures += [f'unexpected: {p}' for p in sorted(actual - set(expected))]
    for name in sorted(actual & set(expected)):
        p = vendor / name
        if p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest() != expected[name]['sha256']:
            failures.append(f'modified: {name}')
        if bool(p.stat().st_mode & stat.S_IXUSR) != (expected[name].get('mode') == '100755'):
            failures.append(f'executable mode changed: {name}')
    if len(expected) != manifest['counts']['files']:
        failures.append('manifest count mismatch')
    return {'status': 'pass' if not failures else 'fail', 'revision': manifest['revision'], 'files': len(expected), 'failures': failures}

def catalog(kit=KIT):
    return read_json(kit / 'adapters/pstack/routes.json')

def inventory(kit=KIT):
    source = verify_source(kit)
    routes = catalog(kit)
    failures = list(source['failures'])
    expected = {'skills':27, 'principles':24, 'playbooks':23, 'agents':2, 'automations':12}
    for group, count in expected.items():
        entries = routes.get(group, [])
        if len(entries) != count or len({e['id'] for e in entries}) != count:
            failures.append(f'{group}: expected {count} unique routes')
        for entry in entries:
            path = kit / 'vendor/pstack' / entry['source']
            if not path.is_file() or not path.resolve().is_relative_to((kit / 'vendor/pstack').resolve()):
                failures.append(f'{group}/{entry["id"]}: invalid source')
            for required in ('triggers', 'native_stage', 'outputs', 'required_primitives', 'overrides', 'status'):
                if required not in entry:
                    failures.append(f'{group}/{entry["id"]}: missing {required}')
    for group, pattern in [('skills','skills/*/SKILL.md'), ('principles','skills/principle-*/SKILL.md'), ('playbooks','skills/poteto-mode/playbooks/*.md'), ('agents','agents/*.md'), ('automations','automations/benny/**/*')]:
        found = {p.relative_to(kit/'vendor/pstack').as_posix() for p in (kit/'vendor/pstack').glob(pattern) if p.is_file()}
        if group == 'skills': found = {p for p in found if '/principle-' not in p}
        mapped = {e['source'] for e in routes.get(group, [])}
        if mapped != found: failures.append(f'{group}: source coverage mismatch')
    return {'status': 'pass' if not failures else 'fail', 'source':source, 'counts':expected, 'failures':failures, 'execution_coverage':'see docs/pstack-certification.md; adapter-defined is not live-certified'}

def route(name, group='playbooks', kit=KIT):
    entries = catalog(kit)[group]
    matches = [e for e in entries if e['id'] == name]
    if len(matches) != 1: raise ValueError(f'unknown {group} route: {name}')
    entry = matches[0]
    return {'entry_command':'ask-super-speckit', 'route':entry, 'read_first':'adapters/pstack/override-contract.md', 'authority':'native feature state; routing metadata is advisory', 'source_revision':catalog(kit)['source_revision']}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--kit', type=Path, default=KIT)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('verify-source'); sub.add_parser('inventory')
    for command in ('route','read'):
        x=sub.add_parser(command); x.add_argument('name'); x.add_argument('--group', choices=GROUPS, default='playbooks')
    sub.add_parser('catalog')
    args=p.parse_args(); kit=args.kit.resolve()
    try:
        if args.command == 'verify-source': result=verify_source(kit)
        elif args.command == 'inventory': result=inventory(kit)
        elif args.command == 'catalog': result=catalog(kit)
        else:
            result=route(args.name,args.group,kit)
            if args.command == 'read':
                if verify_source(kit)['status'] != 'pass': raise ValueError('vendor integrity failed')
                result['adapter_contract']=(kit/'adapters/pstack/override-contract.md').read_text()
                result['upstream_text']=(kit/'vendor/pstack'/result['route']['source']).read_text()
                result['fidelity_overrides']=(kit/'adapters/pstack/override-contract.md').read_text()
                result['application_claim']='source supplied; application requires observed native receipts'
        print(json.dumps(result,indent=2)); return 1 if result.get('status')=='fail' else 0
    except (ValueError,KeyError,OSError) as e:
        print(f'error: {e}',file=sys.stderr); return 2
if __name__=='__main__': raise SystemExit(main())
