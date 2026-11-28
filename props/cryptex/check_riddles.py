"""Check that the cryptex riddles still match the printed material. Re-run after any card or passport change.

    python3 props/cryptex/check_riddles.py

Derives every code from the sources (no answers are written in this public file):
  passport   passport_v2/letters.py + make_passport_batch.py (page 4 underlined digits, page 5 grid, page 8 date)
  cards      passport_v2/chains.py + quest_texts.py, and the RENDERED passport_v2/quest_cards.html
  ring       3dprints/number_safe_dials/make_ministry.py (icon order on the physical ministry ring)
and compares them with the expected codes in ANSWER_KEY.json (crew only, gitignored) if that file exists.
It also scans the guest riddle cards (riddle_cards.html) for leaked answers.
Exit code 0 = all good, 1 = something to fix.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
PV2 = os.path.join(REPO, "passport_v2")
RING = os.path.normpath(os.path.join(REPO, "..", "3dprints", "number_safe_dials", "make_ministry.py"))
sys.path.insert(0, PV2)

FAIL = []
WORD = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "once": 1, "twice": 2, "thrice": 3}


def ok(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        FAIL.append(msg)
    return cond


def text(h):
    h = re.sub(r"<(style|script)\b.*?</\1>", " ", h, flags=re.S)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", h)).split())


def num(word):
    w = word.lower()
    return WORD[w] if w in WORD else int(w)


# ------------------------------------------------------------------ passport
print("PASSPORT (letters.py, make_passport_batch.py)")
import letters  # noqa: E402  (its own asserts: placeholder order, each once)
import make_passport_batch as B  # noqa: E402
import make_passport_options as M  # noqa: E402

notice = set()
for key in [*letters.LETTERS, None]:
    _, body = letters.letter(key or "", "Test", "&minus;9876&nbsp;CC")  # digits in the debt must not count
    notice.add("".join(re.findall(r'<u class="k">(\d)</u>', body)))
ok(len(notice) == 1, f"page 4: every ministry letter + the generic one give the same underlined digits ({len(letters.LETTERS)} letters + generic)")
code_b = notice.pop() if len(notice) == 1 else "?"
ok(len(code_b) == 6, "page 4: exactly six underlined digits (capsule B has six rings)")
ok(B.pages({"name": "", "ministry": "", "debt": ""})[4].count('<u class="k">') == 6, "page 4 as built by the batch: six underlined digits")

pg = B.pages({"name": "", "ministry": "", "debt": ""})
m = re.search(r"returns to nature on (\d{1,2})\.(\d{1,2})", pg[8])
ok(bool(m), 'page 8 (last page): "Every record returns to nature on DD.MM"')
day = m.group(1) if m else "?"
ok(pg[5] is B.NIGHT and "THE TEN MINISTRIES" in pg[5], "page 5 = THE NIGHT with THE TEN MINISTRIES grid")
ok("grid-template-columns:repeat(5,1fr)" in B.EXTRA_CSS and len(M.ORDER) == 10, "page 5 grid: 2 rows of 5")
lower_third = M.ORDER[5 + 2]
ok(f"<span>{lower_third.title()}</span>" in B.MINI_ROW, f"page 5: lower row, third from left is labelled (derived: {lower_third.title()})")

out = os.path.join(PV2, "out")
for f in ("passports.html", "passports_blank.html"):  # printed batch, if present locally (counts only, no names)
    p = os.path.join(out, f)
    if os.path.exists(p):
        h = open(p, encoding="utf-8").read()
        parts = h.split('class="howto"')[1:]
        seqs = {"".join(re.findall(r'<u class="k">(\d)</u>', x.split('class="ozone')[0])) for x in parts}
        ok(seqs == {code_b}, f"printed out/{f}: all {len(parts)} passports carry the same page 4 digits")
        ok(h.count(f"returns to nature on {day}.") == len(parts), f"printed out/{f}: every passport has the page 8 date")

# ------------------------------------------------------------------ cards
print("CARDS (chains.py, quest_texts.py, rendered quest_cards.html)")
import chains  # noqa: E402
try:
    from quest_texts import TEXT as QT
except Exception:
    QT = {}
role = {r[0]: r for r in chains.ROLES}
chain = {c[0]: c for c in chains.CHAINS}
src = {k: QT.get(k, role[k][2] if k in role else chain[k][6]) + " " + chains.NOTES.get(k, "") for k in ("H0", "H1", "H2", "H3", "H4")}

mh = re.search(r"(\d{1,2}):00", role["H0"][3])
ok(bool(mh), 'H0 reward: "Still free at HH:00?"')
hour = mh.group(1) if mh else "?"
md = re.search(r"[Dd]eny it (\w+)", src["H0"]) or re.search(r"deny it (\w+)", src["H1"])
ok(bool(md), "H0/H1: how many times the hacker may deny it")
deny = num(md.group(1)) if md else "?"
mq = re.search(r"\b(\w+) questions\b", src["H2"], re.I)
ok(bool(mq) and "Interrogation" in src["H2"], "H2: ask N questions at the Interrogation station")
quest = num(mq.group(1)) if mq else "?"
ok("Carbon Confessions" in src["H3"] and "Kinderkamer" in src["H3"], "H3: Carbon Confessions, in the Kinderkamer")
ok(chain["H3"][4] == "RADIANCE", "H3 is issued by Radiance")
ok(chain["H4"][4] == "HUMUS" and chain["H4"][5] == "W", "H4 is issued by Humus, mode WITNESS")
ok("recycling" in src["H4"].lower() and "renew" in src["H4"].lower(), "H4: recycling plant, renewal")

qc = os.path.join(PV2, "quest_cards.html")
newest = max(os.path.getmtime(os.path.join(PV2, f)) for f in ("chains.py", "quest_texts.py") if os.path.exists(os.path.join(PV2, f)))
ok(os.path.getmtime(qc) >= newest - 1, "quest_cards.html is newer than chains.py / quest_texts.py (else re-run make_quest_cards.py)")
if os.path.getmtime(qc) < os.path.getmtime(os.path.join(PV2, "make_quest_cards.py")) - 1:
    print("  warn make_quest_cards.py changed after quest_cards.html was built: re-run it, then this check")
cards = {}
for c in open(qc, encoding="utf-8").read().split('<div class="card">')[1:]:
    mm = re.search(r'<span class="id">(H\d)</span>', c)
    if mm and mm.group(1) not in cards:
        cards[mm.group(1)] = text(c)
ok(set(cards) >= {"H0", "H1", "H2", "H3", "H4"}, "rendered: cards H0-H4 present")
r = {k: cards.get(k, "") for k in ("H0", "H1", "H2", "H3", "H4")}
ok(f"{hour}:00" in r["H0"], f"rendered H0 shows the hour ({hour}:00)")
ok(bool(re.search(r"deny it (twice|two times)", r["H0"] + r["H1"], re.I)), "rendered H0/H1: deny it twice")
ok(bool(re.search(r"\b(three|3) questions", r["H2"], re.I)), "rendered H2: three questions")
ok("Ministry of Radiance" in r["H3"] and "Carbon Confessions" in r["H3"] and "Kinderkamer" in r["H3"], "rendered H3: Ministry of Radiance, Carbon Confessions, Kinderkamer")
ok("Radiance citizen" in r["H3"], "rendered H3: they confess to a Radiance citizen")
ok("Ministry of Humus" in r["H4"] and "Humus citizen" in r["H4"] and "watch" in r["H4"], "rendered H4: a Humus citizen watches")

# ------------------------------------------------------------------ ministry ring
print("MINISTRY RING (3dprints make_ministry.py)")
if os.path.exists(RING):
    mo = re.search(r"order\s*=\s*\[([^\]]+)\]", open(RING).read())
    ring = re.findall(r"'(\w+)'", mo.group(1)) if mo else []
    ok(ring == list(M.ORDER), "physical ring carries the same 10 ministries as the passport page 5 grid")
else:
    print("  skip ring file not found:", RING)

# ------------------------------------------------------------------ codes
code_a = f"{hour}{day}{quest}{deny}"
print("DERIVED")
print("  capsule A:", " ".join(code_a), "  capsule B:", " ".join(code_b))
key = os.path.join(HERE, "ANSWER_KEY.json")
if os.path.exists(key):
    K = json.load(open(key))
    ok(code_a == K["capsule_a"], "capsule A matches ANSWER_KEY.json")
    ok(code_b == K["capsule_b"], "capsule B matches ANSWER_KEY.json")
    ok(K["ministry"][1] == lower_third, "ministry ring 2 = page 5 lower row, third from left")
    ok(K["ministry"][2] == chain["H4"][4] and K["ministry"][5] == chain["H3"][4], "ministry rings 3 and 6 = issuers of H4 and H3")
    ok(all(x in M.ORDER for x in K["ministry"]), "all six ministry answers exist on the ring")
    leak_words = [w.title() for w in K["ministry"]] + [code_a, code_b, " ".join(code_a), " ".join(code_b)]
else:
    print("  (no ANSWER_KEY.json: codes printed only, not compared)")
    leak_words = [code_a, code_b]

gc = os.path.join(HERE, "riddle_cards.html")
if os.path.exists(gc):
    g = open(gc, encoding="utf-8").read()
    t = text(g)
    ok(not [w for w in leak_words if re.search(rf"\b{re.escape(w)}\b", t)], "guest cards: no answer word or code in the text")
    ok(not re.search(r"<!--", g), "guest cards: no HTML comments")
    ok(not re.search(r"\bhints?\b|\banswer\s*:", t, re.I), "guest cards: no \"Hint\" or \"Answer:\" lines")

print("ALL GOOD" if not FAIL else f"{len(FAIL)} PROBLEM(S)")
sys.exit(1 if FAIL else 0)
