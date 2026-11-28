# Print plan: party night (Sat 28 Nov)

One command builds everything into `print_pack/` (one PDF per paper type, so each paper is one printer job):

```
scripts/make_print_pack.sh          # quest cards 61x90
scripts/make_print_pack.sh 57x88    # quest cards for 57x88 card stock
```

**Always print at 100% / actual size, never "fit to page".** Mono laser `HL-2150N_series` is fastest; everything is designed black & white.

## Order (longest-lead first)

| # | File | Paper | Sheets | Then |
|---|---|---|---|---|
| 1 | `1_STICKER_quest_fronts*.pdf` + `1_STICKER_quest_backs*.pdf` | A4 sticker sheets | 14 + 14 | cut, stick (slowest step: start first) |
| 2 | `3_CARD_riddles.pdf` | 160-200 g card (manual feed) | see pack | cut, put one per data centre |
| 3 | `2_PLAIN_targets.pdf` | 120 g plain | see pack | A4 into frames as-is; small sizes cut |
| 4 | `4_PLAIN_customs.pdf` | 80 g plain | see pack | guide double-sided; A5 cards cut in half, laminate/tape |

## Cutting fast
- Cards sit edge to edge in a 3 x 3 grid with crop marks outside: stack 5-10 sheets, guillotine **4 cuts down + 4 across = 9 cards per stack**. No trimming between cards.
- Line the first cut up with the crop marks, not the paper edge (printers shift 1-2 mm).

## Sticking quest cards (246 stickers)
- Any back fits any front, so no matching: one person peels fronts, one peels backs, a third sticks. About 10 s per card, ~20 min for 123 cards with 3 people.
- Stick fronts on the card face, backs on the pattern side. Quest ID at the bottom of both helps sort afterwards.
- Faster fallback (no poker cards): print fronts on card stock, backs on the reverse page by page (same order), cut. Check the printer's max paper weight first.

## Before the doors open
- [ ] Count: 123 quest cards, 12 riddle cards, targets framed, 2 customs script cards at the gate.
- [ ] Riddle answer key stays with the crew (never on display).
- [ ] Filled passports and ministry lists come from `passport_v2/out/` (local only, not in git).
