#!/usr/bin/env python3
"""Keyword history ledger for ToolScope Pro.

Every product ever suggested, excluded, or rejected lives in keywords-history.csv.
Run `check` before proposing a batch so the same product never ships twice.

    python3 history.py check "conduit bender" "best palm nailer 2026"
    python3 history.py add 2026-07-25 used "best drawer slide jig 2026"
    python3 history.py list [used|rejected|excluded]
    python3 history.py stats

Matching is product-level, not string-level: "palm nailer under $100" and
"best palm nailer 2026" both reduce to "palm nailer" and collide.
"""
import csv, sys, os, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "keywords-history.csv")

# Marketing scaffolding that carries no product meaning.
NOISE = re.compile(
    r"\b(the|a|an|best|top|review|reviews|reviewed|buying|guide|"
    r"20\d\d|\d+)\b"
)
# Qualifiers that describe a variant, not a different video topic.
QUALIFIERS = {
    "cordless", "corded", "electric", "battery", "battery-powered", "powered",
    "heavy", "duty", "professional", "professionals", "beginners", "hobbyists",
    "compact", "portable", "budget", "cheap", "premium", "brushless",
    "variable", "speed", "adjustable", "precision", "digital", "automatic",
    "manual", "set", "sets", "kit", "kits", "tool", "tools", "system",
    "systems", "machine", "gauge",
}
# Everything after these words is a use-case tail, not the product.
TAIL = re.compile(r"\b(for|under|with|without|in)\b.*$")


def normalize(text):
    """Reduce a keyword or title to its core product tokens."""
    t = text.lower().strip()
    t = re.sub(r"[|,:].*$", "", t)          # drop title suffixes after punctuation
    t = TAIL.sub("", t)                      # drop "for cabinet making", "under $200"
    t = re.sub(r"[^a-z0-9\s-]", " ", t)      # strip $ and punctuation
    t = NOISE.sub(" ", t)
    tokens = [w for w in t.split() if w and w not in QUALIFIERS]
    tokens = [w[:-1] if len(w) > 3 and w.endswith("s") else w for w in tokens]
    return tokens


def key(text):
    return " ".join(normalize(text))


def load():
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check(candidates):
    rows = load()
    index = []
    for r in rows:
        index.append((set(normalize(r["product_key"])), r))

    verdicts = []
    for cand in candidates:
        toks = set(normalize(cand))
        hit, kind = None, None
        for past_toks, row in index:
            if not toks or not past_toks:
                continue
            if toks == past_toks:
                hit, kind = row, "EXACT"
                break
            # One product contained in the other, e.g. "featherboard" vs
            # "table saw featherboard" -> same video topic.
            if toks <= past_toks or past_toks <= toks:
                if hit is None:
                    hit, kind = row, "OVERLAP"
        verdicts.append((cand, kind, hit))
    return verdicts


def cmd_check(args):
    if not args:
        print("usage: history.py check <keyword> [keyword ...]")
        return 2
    verdicts = check(args)
    blocked = 0
    for cand, kind, hit in verdicts:
        if kind is None:
            print(f"  OK       {cand}")
        else:
            blocked += 1
            print(f"  {kind:8} {cand}")
            print(f"           -> {hit['status']} {hit['date']}: "
                  f"{hit['product_key']} ({hit['notes']})")
    print(f"\n{len(verdicts) - blocked}/{len(verdicts)} clear, {blocked} blocked.")
    return 1 if blocked else 0


def cmd_add(args):
    if len(args) < 3:
        print("usage: history.py add <date> <used|rejected|excluded> "
              "<keyword> [notes]")
        return 2
    date, status, keyword = args[0], args[1], args[2]
    notes = args[3] if len(args) > 3 else f"Batch {date}"
    if status not in ("used", "rejected", "excluded"):
        print(f"bad status: {status}")
        return 2
    exists = os.path.exists(LEDGER)
    with open(LEDGER, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["date", "product_key", "status", "keyword", "notes"])
        w.writerow([date, key(keyword), status, keyword, notes])
    print(f"added [{status}] {key(keyword)}")
    return 0


def cmd_list(args):
    rows = load()
    if args:
        rows = [r for r in rows if r["status"] == args[0]]
    for r in rows:
        print(f"{r['date']}  {r['status']:9} {r['product_key']}")
    print(f"\n{len(rows)} entries.")
    return 0


def cmd_stats(_):
    rows = load()
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"ledger: {LEDGER}")
    for k in sorted(counts):
        print(f"  {k:9} {counts[k]}")
    print(f"  {'TOTAL':9} {len(rows)}")
    return 0


COMMANDS = {"check": cmd_check, "add": cmd_add, "list": cmd_list,
            "stats": cmd_stats}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(2)
    sys.exit(COMMANDS[sys.argv[1]](sys.argv[2:]))
