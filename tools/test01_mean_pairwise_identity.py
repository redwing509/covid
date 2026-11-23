import itertools, pathlib, sys

def read_fa(path):
    seqs, name, buf = [], None, []
    for line in pathlib.Path(path).read_text().splitlines():
        if line.startswith(">"):
            if name is not None:
                seqs.append((name, "".join(buf).upper()))
            name, buf = line[1:].split()[0], []
        else:
            buf.append(line.strip())
    if name is not None:
        seqs.append((name, "".join(buf).upper()))
    return seqs

seqs = read_fa(sys.argv[1])
L = {len(s) for _, s in seqs}
if len(L) != 1:
    raise SystemExit("alignment sequences have different lengths")
pairs = []
for a, b in itertools.combinations([s for _, s in seqs], 2):
    m = n = 0
    for x, y in zip(a, b):
        if x in "-N" or y in "-N":
            continue
        n += 1
        if x == y:
            m += 1
    if n:
        pairs.append(m / n)
if not pairs:
    print("MEAN_PAIRWISE_IDENTITY=NA PAIRS=0")
    raise SystemExit(2)
print(f"MEAN_PAIRWISE_IDENTITY={sum(pairs)/len(pairs):.6f} PAIRS={len(pairs)}")
