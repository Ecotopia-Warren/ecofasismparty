"""Writes ../QUEST_SYSTEM.md from the card data (run from passport_v2)."""
import re
from collections import Counter

import make_quest_cards as C
from chains import CHAINS, ROLES

qs = C.load(C.SRC) + [(r[0], r[2], r[3]) for r in ROLES] + [(c[0], c[6], c[7]) for c in CHAINS]


def mode(q):
    return "-" if q in C.ROLE else "TOGETHER" if q in C.TOGETHER else "REPORT" if q in C.DELIVER else "WITNESS"


def kind(q):
    return "Secret role" if q in C.ROLE else "Chain" if q in C.CHAIN else C.KINDS.get(re.match(r"[A-Z]*", q).group(), "Quest")


rows = []
for q, text, st in qs:
    t = text if len(text) < 70 else text[:67] + "..."
    rows.append(f"| {q} | {kind(q)} | {C.issuer_of(q).title()} | {mode(q)} | {st.replace('.0', '')} | {t.replace('|', '/')} |")
cnt = Counter(C.issuer_of(q).title() for q, _, _ in qs if q not in C.ROLE)

doc = f"""# Ecotopia quest system

Decided on 2026-11-26 (Chris), for the party on Sat 28 Nov. Reference for the gate crew and the stations.
Cards: `passport_v2/quest_cards.pdf` (fronts) + `quest_cards_backs.pdf` (backs), 61 x 90 mm stickers for poker cards.
Regenerate: `python3 passport_v2/make_quest_cards.py`, then `cd passport_v2 && python3 make_quest_doc.py` for this file.

## Scoring

- Every credit stamp is worth **100 CC**. A quest gives **1, 2 or 3 stamps**: 1 = easy (alone or with one or two people, a few minutes), 2 = real effort (find something hidden, strangers from several ministries, stealth), 3 = the really hard ones. Not generous on easy quests (decided 2026-11-28; overrides in `passport_v2/quest_rewards.py`).
- **Chains pay off:** stamps escalate per step and the **FINALE** step pays **5 stamps**. Whoever completes a chain has their **reg. no. read out at the Grand Assembly** (the gate keeps a list of finale cards for the announcer). A full chain is worth 10-11 stamps, against 1 for an easy quest.
- Stamps go in the credit boxes on passport pages 6 and 7. Final balance (page 8) = carbon debt + stamps x 100.
- Every credit above 0 counts for your ministry. At the **Grand Assembly (23:30)** only the **top 3 ministries** may compete for **Ascension** (a privilege, not a right) with a song, a chant, a formation, or more.
- Scoreboard at the gate (Chris makes it).
- **Secret victory, Most supportive ministry:** the ministry whose quests were completed most. Count the handed-in cards per issuing ministry. Not printed anywhere.

## Anatomy of a card

**Front**
- Icon + kind (Personal / Ministry / Rival / Collaboration / Rebel / Chain quest / Secret role) + **issuing ministry**.
- Chain and role cards: a black bar, e.g. `THE HACKER · STEP 2 OF 4`.
- The quest: starts with what to do, then **"Done when ..."** (how many / how long) and any special proof. Complex quests get an **extra instruction** (i, small italic).
- **Mode line** in plain words: `DO IT WITH:` / `BRING IT TO:` / `SHOW IT TO:` a citizen of the issuing ministry (TOGETHER / REPORT / WITNESS, below).
- **How to play** strip: `1 Do it -> 2 get their reg. no. -> 3 hand in at the gate`.
- Reward: number of stamps (+CC).
- **SEAL circle, "this quest scores for":** stamped at the gate with the seal of the ministry that scores the quest.

**Back** (sticker on the other side of the poker card)
- Icon + "A QUEST OF THE MINISTRY OF X" (the issuing ministry), or "RESISTANCE".
- `Completed by: your reg. no. ___`
- `DONE WITH / BROUGHT TO / SHOWN TO a X citizen:` + `Write their reg. no. here ___`: must be a citizen of the **issuing ministry**.
- Registration **numbers only, no names**. Quest ID at the bottom to match back and front when sticking.

## Three ways to involve the issuing ministry

| Mode | Front says | Back says | Example |
|---|---|---|---|
| **TOGETHER** | DO IT WITH: a X citizen (ministry / collaboration quests: the Ministry of X) | DONE WITH a X citizen: their reg. no. | slow dance with a Breath citizen; "another ministry" in a quest = the issuing ministry |
| **REPORT** | BRING IT TO: a X citizen | BROUGHT TO a X citizen: their reg. no. | bring a rebel or hacker to Vigilance; a data centre label to Humus |
| **WITNESS** | SHOW IT TO: a X citizen (they watch you do it) | SHOWN TO a X citizen: their reg. no. | ask an official the same question three times (Service watches) |

Data: `passport_v2/quest_ministries.py`: `ISSUER` (chosen by mandate), modes in `TOGETHER` and `DELIVER`, extra instructions in `NOTES`.
Card texts: `passport_v2/quest_texts.py` (`TEXT`) overrides the xlsx "quests to print" column; chain and role texts live in `chains.py`. Change log: `passport_v2/QUEST_CARD_CHANGES.md`.
Rebel quests (RB) are issued by the **Resistance**; the witness is a fellow rebel.

## Flow on the night

1. **Gate, at the start:** each citizen gets quest cards. The gate stamps the **ministry seal** on the front (the ministry that will score it).
2. The citizen does the quest with the issuing ministry (together / report / witness) and fills in both **registration numbers** on the back.
3. **Hand in the card** at the gate or a station. The official checks the numbers (ministry tick-lists, `ministry_lists.pdf`), stamps the passport (1-3 x 100 CC) and **keeps the card**. Kept cards go in a tray per issuing ministry (secret victory) and can be handed out again.
4. **Chain quest?** The gate hands out the next step.

## Chains and secret roles (card game + role play)

We are expanding the quests with chains. Only step 1 of a chain is handed out at the start; hand in a step at the gate to get the next one. Each step is issued by a **different ministry**, so ministries depend on each other.
A **secret role** card goes to a volunteer at the gate, who plays that character all night. **Captives can always say no**: being caught means playing along, never being dragged around.

| Chain | Role card | Steps |
|---|---|---|
| **The Hacker** | H0 The Hacker: deny twice, confess the third time. Still free at 23:00 = 3 stamps | H1 Vigilance (REPORT: catch the hacker) -> H2 Service (TOGETHER: Interrogation station) -> H3 Radiance (REPORT: Carbon Confessions) -> H4 Humus (WITNESS: recycling plant) |
| **The Data Centre** | none | D1 Humus (REPORT: memorise a data centre message) -> D2 Vigilance (TOGETHER: decode it) -> D3 Service (REPORT: make it an announcement) |
| **The Smuggler** | S0 The Smuggler: hides a forbidden item. Never found = 2 stamps | S1 Light (REPORT: find the item) -> S2 Humus (TOGETHER: process it at recycling) -> S3 Joy (WITNESS: return it with a celebration) |

The captured hacker also collects the Interrogation, Carbon Confessions and Recycling stamps on passport page 3.
Add a chain: edit `passport_v2/chains.py` (`ROLES`, `CHAINS`, `NOTES`) and regenerate.

## Anti-cheat

- The official **keeps the card** when stamping: no reuse.
- **Registration numbers** of the completer and the witness/participant on the back; check them against the ministry tick-lists.
- Only officials hold the credit stamps. One ink colour.
- **Officials count** the final balance ("Counted by" on page 8).
- Police spot checks; caught cheating = no credits are taken away (decided 2026-11-27), the citizen is corrected instead: Interrogation / Carbon Confessions, stamped on passport page 3 (CITIZENSHIP STATUS).

## Materials

- Poker cards: about **3 packs** available (3 x 52 = 156 cards, plus jokers). {len(qs)} cards designed now, so about {156 - len(qs)} left for duplicates of popular quests or more chains.

## Open

- Rebel cards show "The Resistance" on both sides: OK, or disguise them as a ministry quest?
- Which seal goes on a card at the gate: always the citizen's own ministry?
- How many copies of each card, and how many role cards (how many hackers and smugglers)?
- Rival quests (R): rival pairings to confirm (proposal: Purity-Flow, Vigilance-Joy, Industry-Humus, Light-Breath, Radiance-Service).
- Who counts at the end, when, and who updates the scoreboard?

## All cards ({len(qs)})

Per issuing ministry: {", ".join(f"{k} {v}" for k, v in sorted(cnt.items()))}.

| ID | Kind | Issued by | Mode | Stamps | Quest |
|---|---|---|---|---|---|
""" + "\n".join(rows) + "\n"

open("../QUEST_SYSTEM.md", "w").write(doc)
print(len(rows), "cards documented")
