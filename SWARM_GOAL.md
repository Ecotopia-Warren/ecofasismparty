# Swarm goal: party-night print pack (Sat 28 Nov 2026)

## Goal
Every guest and crew member knows exactly what to do, with nothing ambiguous on paper.
Done = four print-ready packs, rendered to PDF and visually checked, nothing committed with attendee data.

## Workstreams (one agent each, parallel)

| # | Agent | Deliverable | Done when |
|---|---|---|---|
| 1 | **cards** | Rewritten quest cards (`passport_v2/quest_cards*.pdf`) + `passport_v2/QUEST_CARD_CHANGES.md` | Every card: imperative action, finish condition, proof. Plain mode line ("DO IT WITH / BRING IT TO / SHOW IT TO"). No overflow on 61x90 mm |
| 2 | **targets** | Shooting range picture-frame targets (`props/shooting_range/`) A4 + 13x18 (+10x15) + A5 rules sign | 8-10 portraits with score zones in CC, 1-2 "don't shoot" penalty targets, crop marks |
| 3 | **customs** | `customs/CUSTOMS_CREW_GUIDE.md` + A4 PDF (max 2 pages) + A5 script card | Numbered per-guest flow (~60-90 s), what to check, exact lines, edge cases, out-of-character safety signal |
| 4 | **riddles** | Printable cryptex riddle cards (12) + verification report | Every riddle's answer verified against the actual card/passport text; codes match the cryptex rings |

## Riddle source of truth
`~/Nextcloud/Github/3dprints/number_safe_dials/RIDDLES_*.md`. Three cryptexes, 6 dials each:
- Capsule A "The Hacker" (digits; clues on chain cards H0-H2 and passport p8)
- Capsule B "The Notice" (digits; passport p4 underlined digits)
- Ministry capsule (icons) + ring-order card
- Codes live only in the crew answer key `props/cryptex/ANSWER_KEY.*` (gitignored).

## Dependencies and guards
- **cards -> riddles:** chain cards H0-H4 must keep 23:00, "deny twice", "three questions", H3 Radiance, H4 Humus. Riddles agent verifies against the *regenerated* cards.
- Passport text (p4, p8) is printed and frozen; nothing may change it.
- `Citizens export and quests.xlsx` and `passport_v2/out/` filled passports = personal data, gitignored, never copied.
- No retired ministry names. No commits by agents; the lead reviews and commits.

## Topology
Hierarchical star: lead (main session) dispatches 4 independent workers, merges, verifies PDFs, commits.
