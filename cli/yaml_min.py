"""Minimal YAML subset parser — stdlib only (no PyYAML dependency).

Supports what an SSK manifest.yml needs:
  - nested mappings by indentation
  - lists of scalars and lists of mappings ("- key: value" with continuation keys)
  - scalars: plain / "quoted" / 'quoted' strings
Not a general YAML implementation: no anchors, no multi-line scalars, no flow
collections. Enough for the manifest contract; error loudly on anything else.
"""
import sys


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return parse(f.read())


def parse(text):
    lines = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, stripped))
    if not lines:
        return {}
    value, idx = _block(lines, 0, lines[0][0])
    if idx != len(lines):
        raise ValueError("yaml_min: unparsed content at line block %r" % (lines[idx],))
    return value


def _scalar(tok):
    tok = tok.strip()
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in "\"'":
        return tok[1:-1]
    if tok in ("null", "~", ""):
        return None
    if tok == "true":
        return True
    if tok == "false":
        return False
    return tok


def _block(lines, i, indent):
    if lines[i][1].startswith("- ") or lines[i][1] == "-":
        return _list(lines, i, indent)
    return _mapping(lines, i, indent)


def _list(lines, i, indent):
    items = []
    while i < len(lines) and lines[i][0] == indent and (lines[i][1].startswith("- ") or lines[i][1] == "-"):
        first = lines[i][1][2:].strip() if lines[i][1] != "-" else ""
        i += 1
        if not first:
            # scalar item on following lines is unsupported; empty item
            items.append(None)
            continue
        if ":" in first and not _looks_like_scalar(first):
            # mapping item: first key inline, remaining keys on deeper lines
            sub = [(indent + 2, first)]
            while i < len(lines) and lines[i][0] > indent:
                sub.append(lines[i])
                i += 1
            value, _ = _mapping(sub, 0, indent + 2)
            items.append(value)
        else:
            items.append(_scalar(first))
    return items, i


def _mapping(lines, i, indent):
    result = {}
    while i < len(lines):
        line_indent, content = lines[i]
        if line_indent < indent:
            break
        if line_indent > indent:
            raise ValueError("yaml_min: unexpected indent %r" % (content,))
        if content.startswith("- "):
            break
        key, sep, rest = content.partition(":")
        if not sep:
            raise ValueError("yaml_min: expected 'key: value', got %r" % (content,))
        key = _scalar(key.strip())
        rest = rest.strip()
        i += 1
        if rest:
            result[key] = _scalar(rest)
        elif i < len(lines) and lines[i][0] > indent:
            result[key], i = _block(lines, i, lines[i][0])
        elif i < len(lines) and lines[i][0] == indent and (lines[i][1].startswith("- ") or lines[i][1] == "-"):
            result[key], i = _list(lines, i, indent)
        else:
            result[key] = None
    return result, i


def _looks_like_scalar(tok):
    # "a: b" where the part before ':' is a bare word -> mapping key.
    head = tok.split(":", 1)[0].strip()
    return not head or " " in head or head[0] in "\"'"


if __name__ == "__main__":
    data = load(sys.argv[1])
    import json

    print(json.dumps(data, indent=2, ensure_ascii=False))
