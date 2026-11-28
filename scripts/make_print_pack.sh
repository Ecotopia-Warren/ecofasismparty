#!/usr/bin/env bash
# Build one print-ready PDF per paper type, so each printer run is a single job.
# Usage: scripts/make_print_pack.sh [61x90|57x88]   (quest card size, default 61x90)
# Output: print_pack/*.pdf  (gitignored; regenerate any time)
set -euo pipefail
cd "$(dirname "$0")/.."
SIZE="${1:-61x90}"
SUF=""; [ "$SIZE" != "61x90" ] && SUF="_$SIZE"
OUT=print_pack; mkdir -p "$OUT"

have() { for f in "$@"; do [ -f "$f" ] || { echo "missing: $f" >&2; return 1; }; done; }
join() { local out="$1"; shift; local ok=(); for f in "$@"; do [ -f "$f" ] && ok+=("$f") || echo "  skip (not made yet): $f" >&2; done
         [ ${#ok[@]} -gt 0 ] || return 0
         pdfunite "${ok[@]}" "$OUT/$out"; echo "$OUT/$out: $(pdfinfo "$OUT/$out" | awk '/Pages/{print $2}') sheets"; }

# 1. STICKER PAPER (A4 sticker sheets, laser): quest card fronts + backs
join 1_STICKER_quest_fronts$SUF.pdf passport_v2/quest_cards$SUF.pdf
join 1_STICKER_quest_backs$SUF.pdf  passport_v2/quest_cards_backs$SUF.pdf
# 2. PLAIN PAPER 120 g (laser, B&W): shooting range targets + station sign
join 2_PLAIN_targets.pdf props/shooting_range/PRINT_ALL_targets.pdf
# 3. CARD 160-200 g (laser): riddle cards
join 3_CARD_riddles.pdf props/cryptex/riddle_cards.pdf
# 4. PLAIN PAPER 80 g (laser, B&W): customs crew guide + script cards
join 4_PLAIN_customs.pdf customs/CUSTOMS_CREW_GUIDE.pdf customs/CUSTOMS_CHEAT_CARD_2UP.pdf
# 5. CREW ONLY (plain 80 g): riddle answer key, 2 copies per A4
join 5_CREW_answer_key.pdf props/cryptex/ANSWER_KEY.pdf
echo
echo "Print (mono laser, fastest):  lp -d HL-2150N_series -o media=A4 -o fit-to-page=false print_pack/<file>.pdf"
echo "Print at 100% / actual size, never 'fit to page', or cards come out the wrong size."
