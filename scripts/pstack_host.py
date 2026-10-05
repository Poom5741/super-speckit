#!/usr/bin/env python3
"""Explicit host capabilities and argv dispatch; no invented host flags."""
import argparse
import json
import hashlib
import fnmatch
import uuid
import os
from pathlib import Path
import shutil
import signal
import re
import subprocess

HOSTS = ('zcode', 'codex', 'pi', 'omp', 'cursor')
PROVIDER_PATH_ENV = {'ZCODE_BUILTIN_PROVIDER_CONFIG_FILE', 'ZCODE_PERSONAL_PROVIDER_CONFIG_FILE'}

def environment_paths(value):
    if not isinstance(value, dict) or set(value)-PROVIDER_PATH_ENV: raise ValueError('Only reviewed provider config path environment overrides are supported')
    for key, path in value.items():
        if not isinstance(path, str) or not Path(path).is_file(): raise ValueError('Provider config path must be an existing file')
    return dict(value)

def discovery(scopes, skill='ask-super-speckit'):
    matches = []; seen = set()
    for scope in scopes:
        directory = Path(scope['path']).expanduser().resolve()
        paths = sorted(p for p in directory.rglob('SKILL.md') if all(not part.startswith('.') or part == '.system' for part in p.relative_to(directory).parts[:-1])) if directory.is_dir() else []
        for path in paths:
            if path in seen: continue
            seen.add(path)
            # Read only YAML frontmatter, never unrelated skill bodies.
            with path.open() as stream:
                if stream.readline().strip() != '---': continue
                for line in stream:
                    if line.strip() == '---': break
                    match = re.match(r"^name:\s*[\"']?([^\"']+?)[\"']?\s*$", line)
                    if match and match.group(1).strip() == skill:
                        matches.append(dict(path=str(path), scope=scope.get('kind', 'unspecified'))); break
    winner = matches[0] if matches else None
    return dict(precedence='configured-first-match', winner=winner, matches=matches, warning='user-scope-shadowing' if winner and winner['scope']=='user' and any(m['scope']=='project' for m in matches[1:]) else None)


def doctor(config, project=None):
    results = {}
    for host in HOSTS:
        entry = config.get(host, {})
        argv = entry.get('argv')
        binary = argv[0] if isinstance(argv, list) and argv else host
        located = shutil.which(binary)
        results[host] = dict(primary=host == 'zcode', executable=located, dispatch='configured' if located and argv else 'unavailable', isolation=entry.get('isolation', 'unavailable'), certification='unverified')
        if host == 'zcode':
            workspace = Path(project or config.get('_project') or Path.cwd()).resolve()
            parents = [workspace, *workspace.parents]
            defaults = [dict(path=p,kind='configured') for p in entry.get('configured_skill_roots', [])]
            defaults += [dict(path=str(Path.home()/'.zcode/skills'),kind='user'),dict(path=str(Path.home()/'.agents/skills'),kind='user')]
            defaults += [dict(path=str(parent/directory/'skills'),kind='project') for directory in ('.zcode','.agents') for parent in parents]
            defaults += [dict(path=p,kind='plugin') for p in entry.get('plugin_skill_roots', [])]
            results[host]['discovery'] = discovery(entry.get('skill_scopes', defaults))
    return results


def plan(config, host, brief, worktree, model=None, role="worker", allowed_writes=None, stop_condition="return-evidence", attempt=None):
    if host not in HOSTS: raise ValueError('Unsupported host')
    entry = config.get(host, {})
    env = environment_paths(entry.get('env', {}))
    argv = entry.get('argv')
    if not isinstance(argv, list) or not argv or not shutil.which(argv[0]): raise ValueError('No configured executable dispatch')
    if entry.get('isolation') != 'git-worktree': raise ValueError('Dispatch requires declared git-worktree isolation')
    worktree = Path(worktree).resolve()
    head = subprocess.run(['git', '-C', str(worktree), 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    if subprocess.run(['git', '-C', str(worktree), 'status', '--porcelain'], capture_output=True, text=True, check=True).stdout:
        raise ValueError('Worker worktree must start clean')
    brief = Path(brief).resolve()
    if not brief.is_file() or not brief.stat().st_size: raise ValueError('Immutable brief must be a nonempty file')
    if not (worktree/'.git').is_file(): raise ValueError('Use an isolated linked git worktree')
    fields = dict(brief=str(brief), worktree=str(worktree), model=model or entry.get('model', ''))
    if model and '{model}' not in ' '.join(argv): raise ValueError('Configured host does not expose model selection')
    command = []
    for arg in argv:
        for key, value in fields.items(): arg = arg.replace('{'+key+'}', value)
        command.append(arg)
    return dict(host=host, argv=command, cwd=str(worktree), base=head, brief=str(brief), brief_sha256=hashlib.sha256(brief.read_bytes()).hexdigest(), role=role, allowed_writes=allowed_writes or [], attempt=attempt or uuid.uuid4().hex, stop_condition=stop_condition, env=env, certification='unverified')



def changed_paths(request):
    cwd = request['cwd']
    changes = subprocess.run(['git', '-C', cwd, 'diff', '--name-only', '-z', request['base']], capture_output=True, check=True).stdout.decode().split('\0')
    changes += subprocess.run(['git', '-C', cwd, 'ls-files', '--others', '--exclude-standard', '-z'], capture_output=True, check=True).stdout.decode().split('\0')
    changes = sorted(set(p for p in changes if p))
    allowed = request['allowed_writes'] if request['role'] not in ('reviewer', 'checker', 'read-only') else []
    return changes, [p for p in changes if not any(fnmatch.fnmatchcase(p, pattern) for pattern in allowed)]


def dispatch(request, timeout=60):
    cwd = Path(request['cwd']).resolve()
    if not (cwd/'.git').is_file(): raise ValueError('Dispatch requires a linked git worktree')
    brief = Path(request['brief'])
    if hashlib.sha256(brief.read_bytes()).hexdigest() != request['brief_sha256']: raise ValueError('Brief changed after planning')
    head = subprocess.run(['git', '-C', request['cwd'], 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    if head != request['base']: raise ValueError('Base changed after planning')
    if subprocess.run(['git', '-C', request['cwd'], 'status', '--porcelain'], capture_output=True, text=True, check=True).stdout: raise ValueError('Worktree changed after planning')
    env = environment_paths(request.get('env', {}))
    process = subprocess.Popen(request['argv'], cwd=request['cwd'], env={**os.environ, **env}, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        changes, violations = changed_paths(request)
        return dict(status='write-violation' if violations else ('completed' if process.returncode == 0 else 'failed'), returncode=process.returncode, stdout=stdout, stderr=stderr, base=request['base'], changed_paths=changes, write_violations=violations, attempt=request['attempt'])
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try: stdout, stderr = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL); stdout, stderr = process.communicate()
        changes, violations = changed_paths(request)
        return dict(status='cancelled', returncode=process.returncode, stdout=stdout, stderr=stderr, base=request['base'], changed_paths=changes, write_violations=violations, attempt=request['attempt'])


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('operation', choices=['doctor', 'plan', 'dispatch']); p.add_argument('--input', required=True)
    args = p.parse_args(); data = json.loads(Path(args.input).read_text())
    try: print(json.dumps({'doctor': lambda: doctor(data), 'plan': lambda: plan(**data), 'dispatch': lambda: dispatch(**data)}[args.operation](), indent=2))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc: p.exit(1, str(exc)+'\n')

if __name__ == '__main__': main()
