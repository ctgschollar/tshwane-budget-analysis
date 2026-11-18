import sys
path=sys.argv[1]; pages=open(path,encoding='utf-8',errors='replace').read().split('\f')
for a in sys.argv[2:]:
    n=int(a); print(f"######## PAGE {n}"); print(pages[n-1])
