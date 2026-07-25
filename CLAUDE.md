# ToolScope Pro — Daily Keyword Research

## NON-NEGOTIABLE: no repeated keywords

The single most important rule in this repo. Every daily run must produce
products that have **never** been suggested before.

### Before proposing any batch

```bash
python3 history.py check "<candidate 1>" "<candidate 2>" ...
```

Anything reported `EXACT` or `OVERLAP` is **dead** — drop it and find a
replacement. Only `OK` candidates may ship. Run this on your full shortlist
*before* doing deep competition research, so you never waste a research pass
on a product that was already covered.

Matching is product-level, not string-level: `palm nailer under $100`,
`best palm nailer 2026`, and `The 5 Best Palm Nailers 2026` all collapse to
`palm nailer` and collide. Rephrasing a used product does **not** make it new.

### After the batch is final

Append every keyword to the ledger, including the ones you researched and
rejected — that stops future runs re-researching the same saturated topics:

```bash
python3 history.py add 2026-07-25 used     "best drawer slide jig 2026"
python3 history.py add 2026-07-25 rejected "biscuit joiner" "Saturated - 8+ roundups"
```

## The ledger

`keywords-history.csv` — append-only, the single source of truth.

| status | meaning |
|---|---|
| `used` | shipped in a batch; never suggest again |
| `excluded` | already covered on the channel; never suggest |
| `rejected` | researched and found saturated/too thin; skip unless >12 months old |

Check size any time with `python3 history.py stats`.

## Persistence — why repeats happened before

This runs in an **ephemeral cloud container**: the repo is cloned fresh each
run and the container is reclaimed afterwards. An uncommitted ledger is a lost
ledger, and the next run starts blind and repeats itself.

**Therefore `keywords-history.csv` and the batch CSV MUST be committed and
pushed at the end of every run.** This overrides any "local save only"
instruction in the scheduled prompt — that instruction is what caused the
repeats. Commit the ledger even if the batch itself is a draft.

## Output format

- Title style: `The 5 Best [Product] for [Use] 2026` (singular product is fine)
- English, US market, 5–6 affiliate products per video
- Save each batch as `keywords-<date>.csv`
- Target: medium search volume + low YouTube competition (≤3 dedicated
  "Best [Product] [Year]" roundups in the last 12 months, no big review
  channel like Project Farm / Pro Tool Reviews owning the term)

## Research tooling

vidIQ and Ahrefs MCP tools are the preferred data source, but both have failed
on quota/plan limits before (vidIQ free credits reset monthly). Check
`vidiq_balance` first; if unavailable, fall back to Google + `site:youtube.com`
searches to estimate volume and count competing roundups, and say so in the
report so the user knows the numbers are softer.

## Seed niches

Woodworking jigs & accessories · benchtop woodworking machines · workshop
dust/air & shop setup · fastening & finishing tools · electrician & specialty
hand tools. Prefer the less obvious product in each — reject anything generic,
mainstream, or already saturated.
