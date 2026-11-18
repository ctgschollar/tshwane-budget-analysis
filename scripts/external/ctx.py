import sys, re, glob, os
# usage: ctx.py '<keyword regex>' [verbregex] [window]
kw = re.compile(sys.argv[1], re.I)
verb = re.compile(sys.argv[2] if len(sys.argv)>2 and sys.argv[2] else r'serv|suppl|benefi|feed|address|provid|cater|capacity for|for the (residents|communit)|to (meet|accommodat)|communit|demand|households|area', re.I)
w = int(sys.argv[3]) if len(sys.argv)>3 else 2
for f in sorted(glob.glob(os.path.join(os.environ.get('TSHWANE_WORKDIR', '.'), 'txt', '*.txt'))):
    pages = open(f, encoding='utf-8', errors='replace').read().split('\f')
    short = os.path.basename(f)[:30]
    for i, p in enumerate(pages, 1):
        L = p.splitlines()
        for j, line in enumerate(L):
            if kw.search(line):
                win = L[max(0,j-w):j+w+1]
                txt = ' | '.join(re.sub(r'\s+',' ',x).strip() for x in win if x.strip())
                if verb.search(txt):
                    print(f"[{short} p{i}] {txt[:600]}")
