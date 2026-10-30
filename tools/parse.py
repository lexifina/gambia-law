"""Gambia Constitution (1997, 'reprinted 2002') -> unit dict. Reads the cached PDF only (no network).
Usage: python -X utf8 -I parse.py <constitution.pdf> <out units.json>"""
import json, re, sys
import pymupdf

pdf, out = sys.argv[1:3]
doc = pymupdf.open(pdf)


def norm(s):
    s = s.replace(' ', ' ').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace('﻿', '')
    return re.sub(r'\s{2,}', ' ', s).strip()


def page_lines(pn):
    rows = []
    for b in doc[pn].get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            t = ''.join(s['text'] for s in ln['spans'])
            if t.strip():
                rows.append((ln['bbox'][1], ln['bbox'][0], t))
    return rows


# table of contents (pages 0-10): section headings
toc = {}
for pn in range(0, 11):
    rows = [(y, x, t) for y, x, t in page_lines(pn)]
    for i, (y, x, t) in enumerate(rows):
        m = re.match(r'^\s*(\d{1,3})\s?([A-Z])?\s*\.{1,2}\s*(\S.*)$', t) or re.match(r'^\s*(\d{1,3})()\s+([A-Z][a-z].*)$', t)
        if m and x > 50:
            toc.setdefault(m.group(1) + (m.group(2) or ''), norm(m.group(3)))
            continue
        m = re.match(r'^\s*(\d{1,3})\s?([A-Z])?\s*\.{1,2}\s*$', t)
        if m and x > 50 and i + 1 < len(rows) and rows[i + 1][1] > 100:
            toc.setdefault(m.group(1) + (m.group(2) or ''), norm(rows[i + 1][2]))
toc.setdefault('50', 'Delimitation of Constituencies')

FIRST = 11
pre = [(10, y, x, t) for y, x, t in page_lines(10) if y > 600]
for y, x, t in page_lines(11):
    if re.match(r'^\s*CHAPTER I\s*$', t):
        break
    pre.append((11, y, x, t))
paras, cur, last_y = [], '', None
for pn, y, x, t in pre:
    if last_y is not None and y - last_y > 20 and cur:
        paras.append(cur); cur = ''
    cur = (cur + ' ' + norm(t)).strip(); last_y = y
if cur:
    paras.append(cur)
preamble = '# Preamble\n' + '\n'.join(paras) + '\n'

SEC_END = re.compile(r'^(.*?)(?<![\d])(\d{1,3})\s?([A-Z])?\s*\.{1,2}\s*(.*)$')
SEC_NOPT = re.compile(r'^(.*?)(?<![\d])(\d{1,3})\s*(\(1\).*)$')
NUMONLY = re.compile(r'^\s*(\d{1,3})\s?([A-Z])?\s*\.{1,2}\s*$')
HEAD = re.compile(r'^\s*(CHAPTER\s?[IVXL]+\b|PART\s?\d|SCHEDULE\s?\d)', re.I)
expected = 1
# sections whose number is missing from the printed margin (typos in the reprint): matched by their heading instead
FUZZY = {82, 154, 179, 181, 193, 195, 226}


def is_upper(t):
    return len(t.strip()) > 3 and not re.search(r'[a-z]', t)


def try_start(t, x):
    s = re.sub(r'\b\d+ of \d{4}\b', ' ', t)
    m = NUMONLY.match(s)
    if m and x < 200:
        n, suf = int(m.group(1)), m.group(2) or ''
        if n == expected or (suf and n == expected - 1) or (expected < n <= expected + 6 and str(n) in toc):
            return (n, suf, '')
        return None
    if x >= 150:
        return None
    cands = [expected] + [k for k in range(expected + 1, expected + 7) if str(k) in toc]
    for n in cands:
        m = re.search(r'(?<![\d.])' + str(n) + r'(?:\s?([A-Z])\b)?\s*\.{0,2}(?!\d)\s*(.*)$', s)
        if m and not re.search(r'\d', s[:m.start()]):
            return (n, m.group(1) or '', m.group(2))
    import difflib
    for n in [expected] if expected in FUZZY else []:
        ttl = toc.get(str(n))
        if ttl and len(ttl) > 5 and not re.search(r'\d', s[:len(ttl)]):
            if difflib.SequenceMatcher(None, s.strip()[:len(ttl)].lower(), ttl.lower()).ratio() >= 0.7:
                return (n, '', s.strip()[len(ttl):])
    if expected > 1:
        m = re.search(r'(?<![\d.])' + str(expected - 1) + r'\s?([A-Z])\b\s*\.{0,2}\s*(.*)$', s)
        if m and not re.search(r'\d', s[:m.start()]):
            return (expected - 1, m.group(1), m.group(2))
    return None


secs, sched = [], {}
cur = None
curs = None
in_sched = False
for pn in range(FIRST, len(doc)):
    for y, x, t in page_lines(pn):
        if in_sched:
            m = re.match(r'^\s*SCHEDULE\s?(\d)', t, re.I)
            if m:
                curs = m.group(1); sched[curs] = []
            elif curs:
                sched[curs].append((pn, y, x, t))
            continue
        if re.match(r'^\s*SCHEDULE\s?1\s*$', t) and expected > 232:
            in_sched = True; curs = '1'; sched['1'] = []
            continue
        if re.fullmatch(r'\s*\d{1,3}\s*', t) and x > 250:
            continue
        c = None if HEAD.match(t) else try_start(t, x)
        if c:
            n, suf, rest = c
            if suf == '':
                expected = n + 1
            cur = {'n': n, 's': suf, 'lines': []}
            secs.append(cur)
            mr = re.match(r'\s*TO\s+(\d+)', rest or '')
            if mr:
                expected = int(mr.group(1)) + 1
                cur['range'] = int(mr.group(1))
                cur['lines'].append((pn, y, 999, 'Deleted by No. 6 of 2001.'))
                cur = None
                continue
            if rest and norm(rest):
                cur['lines'].append((pn, y, 999, rest))
            continue
        if cur is None:
            continue
        if HEAD.match(t) or (is_upper(t) and x > 100):
            continue
        if x < 150 and not t.startswith(' '):
            continue
        cur['lines'].append((pn, y, x, t))

MARK = re.compile(r'^(\(\s*(?:[0-9]+|[a-z]{1,4}|[ivxl]+|[A-Z])\s*\))\s*(.*)$')


def paragraphs(lines):
    out, curp = [], ''
    for pn, y, x, t in lines:
        n = norm(t)
        if not n:
            continue
        m = MARK.match(n)
        if m:
            if curp:
                out.append(curp)
            curp = re.sub(r'\(\s*(.+?)\s*\)', r'(\1)', m.group(1)) + ((' ' + m.group(2)) if m.group(2) else '')
            continue
        curp = (curp + ' ' + n).strip()
    if curp:
        out.append(curp)
    return out


units = {}
for s in secs:
    key = f"{s['n']}{s['s']}"
    ukey = f"sec-{s['n']:03d}" + (f"-{s['s'].lower()}" if s['s'] else '')
    title = toc.get(key) or toc.get(str(s['n']))
    ps = paragraphs(s['lines'])
    num = f"{s['n']}{(' ' + s['s']) if s['s'] else ''}"
    if s.get('range'):
        num = f"{s['n']} to {s['range']}"
        toc[key] = 'Deleted sections'
    head = f"# {num}. {title}" if title else f"# {num}."
    units[ukey] = {'label': (f"Sections {num}" if s.get('range') else f"Section {num}"), 'kind': 'section', 'text': head + '\n' + ''.join(p + '\n' for p in ps)}
for k, nm in (('1', 'Schedule 1: Dimensions of the national flag'), ('2', 'Schedule 2: Transitional and consequential provisions')):
    ls = [r for r in sched.get(k, []) if not re.fullmatch(r'\s*\d{1,3}\s*', r[3])]
    units[f'schedule-{k}'] = {'label': f'Schedule {k}', 'kind': 'schedule', 'text': f'# {nm}\n' + ''.join(p + '\n' for p in paragraphs(ls))}
units = {'preamble': {'label': 'Preamble', 'kind': 'preamble', 'text': preamble}, **dict(sorted(units.items()))}

def ukey_of(k):
    m = re.match(r'(\d+)([A-Z]?)$', k)
    return f"sec-{int(m.group(1)):03d}" + ('-' + m.group(2).lower() if m.group(2) else '')

missing = [k for k in toc if ukey_of(k) not in units]
print('units', len(units), 'toc', len(toc), 'missing from parse', missing)
json.dump(units, open(out, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
