import sys, re
path, pat = sys.argv[1], sys.argv[2]
pages = open(path, encoding='utf-8', errors='replace').read().split('\f')
rx = re.compile(pat, re.I)
for i, p in enumerate(pages, 1):
    for line in p.splitlines():
        if rx.search(line):
            print(f"p{i}: {line.strip()[:160]}")
