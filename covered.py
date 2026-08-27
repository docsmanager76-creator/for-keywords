"""Print every keyword already used in a previous batch.

The daily routine must run this BEFORE researching and treat everything it
prints as off-limits, so batches stop repeating each other. Works across both
CSV schemas used so far -- each one has a "Keyword" column.

    python3 covered.py           # normalized core products, one per line
    python3 covered.py --raw     # full original keyword phrases with dates
"""
import csv, glob, os, re, sys

# Modifier tails the routine bolts on ("... under $100", "... for professionals").
# Stripping them means "palm nailer under $100" blocks a later "palm nailer for
# framing" -- the product is what's spent, not the phrasing.
TAIL = re.compile(r"\s+(?:for|under|with|w/)\s+.*$", re.I)
LEAD = re.compile(r"^(?:the\s+)?(?:\d+\s+)?best\s+", re.I)
FILLER = re.compile(r"\b(?:top|review(?:ed|s)?|\d{4})\b", re.I)


def normalize(kw):
    s = kw.strip().lower()
    s = LEAD.sub("", s)
    s = TAIL.sub("", s)
    s = FILLER.sub("", s)
    s = re.sub(r"[^a-z0-9$ ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    # crude singularization so "push blocks" == "push block", while leaving
    # words that merely end in s alone ("trellis", "status", "bias")
    return " ".join(w[:-1] if len(w) > 3 and w.endswith("s")
                    and not w.endswith(("ss", "is", "us", "as")) else w
                    for w in s.split())


def load(root):
    rows = []
    for path in sorted(glob.glob(os.path.join(root, "keywords-*.csv"))):
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                kw = (row.get("Keyword") or "").strip()
                if kw:
                    rows.append((row.get("Date", "").strip() or "?", kw, os.path.basename(path)))
    return rows


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    rows = load(root)
    if "--raw" in sys.argv:
        for date, kw, src in rows:
            print(f"{date}\t{kw}\t{src}")
        return
    for core in sorted({normalize(kw) for _, kw, _ in rows}):
        print(core)


if __name__ == "__main__":
    main()
