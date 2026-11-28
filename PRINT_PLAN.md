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
| 2 | `3_CARD_riddles.pdf` | 160-200 g card (manual feed) | 1 | cut; 12 cards over 7 data centres: DC1-5 two cards each, DC6 one, DC7 the ring-order card |
| 3 | `2_PLAIN_targets.pdf` | 120 g plain | see pack | A4 into frames as-is; small sizes cut |
| 3b | `2c_PLAIN_gate_kit.pdf` | 120 g plain | 13 | scoreboard 2 sheets on the wall; tray + data centre labels cut on crop marks; range brief + run of show to crew |
| 4 | `4_PLAIN_customs.pdf` | 80 g plain | see pack | guide double-sided; A5 cards cut in half, laminate/tape |

## Cutting fast
- Cards sit edge to edge in a 3 x 3 grid with crop marks outside: stack 5-10 sheets, guillotine **4 cuts down + 4 across = 9 cards per stack**. No trimming between cards.
- Line the first cut up with the crop marks, not the paper edge (printers shift 1-2 mm).

## Sticking quest cards (246 stickers)
- **Backs belong to one front.** Each back names the issuing ministry, the verb and the quest ID. Keep front sheet N with back sheet N and stick position by position; check the quest ID at the bottom matches.
- One person peels fronts, one peels backs (same sheet number, same position), a third sticks. About 10 s per card, ~20 min for 123 cards with 3 people.
- Do **not** print fronts and backs duplex: the backs are not mirrored, so columns 1 and 3 would swap.

## Enough starter cards
- Customs gives every citizen one starter card (a Personal I-card or a chain step 1): about **150 + walk-ins**.
- One run holds only 50 I-cards + H1/D1/S1. **Print sheets 1-6 of fronts AND backs two extra times** (+12 sticker sheets each side = +108 cards).
- That needs ~108 more poker cards than the ~156 you have. No more poker cards? Stick front and back sticker onto each other (or on 160 g card) instead.

## Before the doors open
- [ ] Count: 123 quest cards + 108 extra starter I-cards, 12 riddle cards, targets framed, 2 customs script cards at the gate.
- [ ] Riddle answer key `5_CREW_answer_key.pdf` (1 sheet, 2 copies) stays with the crew.
- [ ] Fill in safety lead + medical names and phone numbers by pen on every customs guide and cheat card.
- [ ] Brief crew on closing time: passport says "Dance until 03:00", CANON says 04:00.
- [ ] Targets: "DO NOT SHOOT" red prints grey on the mono laser; still readable. Print only the frame sizes you have (pages 2-11 = A4).
- [ ] Filled passports and ministry lists come from `passport_v2/out/` (local only, not in git).
