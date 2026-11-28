#!/usr/bin/env python3
"""Ecotopia station signs: one A5 sign per station (#17-#34), two per A4 landscape.

Each sign: R.E.I.G.N. name + plain subtitle, the ministry (in-world label, only
where a current source supports it), 3 steps "what you do here", reward in
stamps (1 stamp = 100 CC), the quest/chain cards that bring you here, a safety
and consent line, and a small crew box. Anything not decided prints as a grey
"TBD" field with room to write by hand.

Sources: CANON.md station plan, QUEST_SYSTEM.md, passport_v2/chains.py,
customs/CUSTOMS_CREW_GUIDE.md, "Party Design - Committee Working Doc.md",
_ministries.qmd, OPEN_QUESTIONS.md, gh issues #17-#34.
Canon rule (OPEN_QUESTIONS #2): stations are crew-run and NOT aligned with the
ministries. The ministry line is flavour only; no ministry scores for a station.

Style and helpers are imported from props/shooting_range/make_targets.py
(Archivo / Archivo Black, black + one red accent, B&W safe).

Output:
  props/station_signs/out/station_signs_A5.html/.pdf      one A5 sign per page (18)
  props/station_signs/out/station_signs_2xA5_on_A4.html/.pdf  2 per A4 landscape (9)
  props/station_signs/PRINT_ALL_station_signs.pdf          = the 2-up file, print this

Usage: python3 props/station_signs/make_station_signs.py
"""
import html
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
sys.path.insert(0, os.path.join(HERE, "..", "shooting_range"))
import make_targets as mt  # noqa: E402  (main is guarded; we only use helpers + constants)

RED, FONTS = mt.RED, mt.FONTS
TBD_RE = re.compile(r"\{TBD(?::([^}]*))?\}")


def tbd(note=""):
    note = f" · {html.escape(note)}" if note else ""
    return f'<span class="tbd">TBD{note}</span>'


def t(s):
    """Text with inline {TBD} / {TBD:note} markers. None -> a TBD field."""
    if s is None:
        return tbd()
    return TBD_RE.sub(lambda m: tbd(m.group(1) or ""), s)


def tbd_block(label):
    return f'<div class="tbdbox"><span>TBD</span> {html.escape(label)}</div>'


# ------------------------------------------------------------------ DATA
# Steps: a string (may hold {TBD} markers) or None (grey write-in line).
# HTML allowed in strings. Keep each sign short: it must fit A5.
DIST, DARTS = mt.DISTANCE_M, mt.DARTS
B, R_, P_ = mt.BULL, mt.RING, mt.PORTRAIT
PG, PV = mt.PENALTY["guardian"], mt.PENALTY["governor"]
CAP = mt.STAMP_CAP

NOCRED_P3 = "No credits here. You get a status stamp on passport page 3"
GATE = "Finished cards go to the gate for stamps."

STATIONS = [
    dict(n=17, floor="BG", loc="Washing room",
         ministry="Purity",
         name="THE TRIAL OF<br>HONEST APPETITES",
         sub="Blind tasting: taste the most sustainable food.",
         steps=["Tell the official your allergies and anything you do not eat. Blindfold on, only if you want.",
                "Taste what you are offered. Spit cup on the table; you may skip any bite.",
                "Guess which bite is the most sustainable. How it is scored: {TBD}"],
         reward=None, cards="None. " + GATE,
         safety="Allergies first: ask what is in it before you taste. Blindfold only with your yes, off any time.",
         checks="Ask allergies and diet before every tasting. Ingredient list at the table.",
         stamps=None),
    dict(n=18, floor="BG", loc="Kinderkamer",
         ministry=None,
         name="R.E.I.G.N. ACCEPTS<br>CONFESSIONS",
         sub="Carbon Confessions: confess the worst thing you have done to the planet.",
         steps=["Sit down. Take your time: R.E.I.G.N. has all night.",
                "Confess the worst thing you have done to the planet. One confession is enough.",
                "Be forgiven: the official stamps <b>FORGIVEN</b> in the CORRECTED · CARBON CONFESSIONS box, passport page 3."],
         reward=NOCRED_P3 + ": <b>FORGIVEN</b>.",
         cards="<b>H3</b> The Hacker, step 3: the hacker is brought here. Citizens caught cheating are sent here to be corrected. " + GATE,
         safety="Share only what you want to share. You may stop or leave at any time.",
         checks="H3: the hacker confesses loudly, with a smile, to a Radiance citizen (their reg. no. on the card). Cheaters: corrected, no credits taken.",
         stamps="CARBON CONFESSIONS · FORGIVEN on p. 3 (if the stamp is made)."),
    dict(n=19, floor="BG", loc="Tribune",
         ministry=None,
         name="THINK INSIDE<br>THE BOX",
         sub='The "box": what happens here is {TBD}.',
         steps=[None, None, None],
         reward=None, cards="None. " + GATE,
         safety="You may step out of the box at any time. {TBD:station-specific safety}",
         checks=None, stamps=None),
    dict(n=20, floor="BG", loc=None,
         ministry="Vigilance",
         name="THE GALLERY OF<br>GENTLE CORRECTION",
         sub="Shooting range: foam darts at official portraits.",
         steps=[f"Stand behind the line, <b>{DIST} metres</b>. <b>{DARTS} foam darts</b> from the official, one round, then rejoin the queue.",
                f"Hit an enemy of the green state: bull <b>{B}</b>, ring <b>{R_}</b>, anywhere on the portrait <b>{P_}</b> CC.",
                f"<b>DO NOT SHOOT</b> the official portraits: Governor &minus;{PV}, Guardian &minus;{PG} CC off this round."],
         reward=f"Every <b>100 CC</b> in a round = <b>1 stamp</b>, max {CAP} per round. A bad round never costs credits you already have. "
                "<i>Proposal: scoring still open (#14).</i>",
         cards="None. " + GATE,
         safety="Aim only at the frames, never at faces, people or animals. Wait behind the line until the official calls CLEAR.",
         checks="Count the round, call CLEAR, fetch the darts yourself. Full rules: the range sign.",
         stamps=f"Credit stamps p. 6-7, max {CAP} per round."),
    dict(n=21, floor="BG", loc="Woonzaal or BG kitchen floor: {TBD:which}",
         ministry=None,
         name="THE LOTTERY OF<br>GENTLE FORTUNE",
         sub="Gambling station: gamble with your carbon credits.",
         steps=["The game: {TBD}", "Stakes, and can you lose stamps here: {TBD}", "Payout: {TBD}"],
         reward=None, cards="None. " + GATE,
         safety="Play only if you want to. {TBD:station-specific safety}",
         checks=None, stamps=None),
    dict(n=22, floor="BG", loc=None,
         ministry=None, kicker="EVERY MINISTRY · NO MINISTRY RUNS IT",
         name="THE REHEARSAL<br>FOR ASCENSION",
         sub="Ministry ritual preparation: get your ministry ready for the Grand Assembly.",
         steps=["Gather your ministry: everyone with your ministry's seal.",
                "Prepare what you will show: a song, a chant, a formation, or more.",
                "Be as ready as possible by <b>23:30</b>. Only the top 3 ministries may compete for Ascension."],
         reward=None, cards="None. " + GATE,
         safety="Join in as much or as little as you like.",
         checks=None, stamps=None),
    dict(n=23, floor="BG", loc=None,
         ministry=None,
         name="THE BUREAU<br>OF YES",
         sub="Consent giving: what happens here is {TBD}.",
         steps=[None, None, None],
         reward=None, cards="None. " + GATE,
         safety="A yes can always become a no. {TBD:station-specific safety}",
         checks=None, stamps=None),
    dict(n=24, floor="BG", loc=None,
         ministry=None,
         name="THE BOOTH OF<br>CARBON ZERO",
         sub="Let your carbon footprint go back to zero, or change ministry.",
         steps=["Step into the booth, with your passport.",
                "Choose: your carbon footprint back to zero, or a new ministry.",
                "What happens then (ritual, stamp, new name): {TBD}"],
         reward=None, cards="None. " + GATE,
         safety="This is theatre. Not OK tonight? Say <b>OZONE</b> or find any crew member.",
         checks="Keep it soft and light. Never pressure anyone in. Keep or drop this station: {TBD:#24}",
         stamps=None),
    dict(n=25, floor="BG", loc=None,
         ministry=None,
         name="ESMA IS NOT ANGRY,<br>ONLY DISAPPOINTED",
         sub="Esma guilt trip: what happens here is {TBD}.",
         steps=[None, None, None],
         reward=None, cards="None. " + GATE,
         safety="You may walk away at any time. {TBD:station-specific safety}",
         checks=None, stamps=None),
    dict(n=26, floor="BG", loc="Woonzaal kitchen",
         ministry=None,
         name="EVERY DROP<br>ACCOUNTED FOR",
         sub="Greenwashing the dishes: wash glasses with as little water as you can.",
         steps=["Take one sponge from the official.",
                "Wash the glasses you are given, using as little water as possible. How many: {TBD}",
                "The official inspects every glass before you go."],
         reward=None, cards="None. " + GATE,
         safety="Careful with glass and hot water. Something breaks? Stop, call the official, do not pick it up.",
         checks="Inspect each glass. Broken glass: you clear it, not the citizen.",
         stamps=None),
    dict(n=27, floor="BG", loc=None,
         ministry=None, kicker="EVERY MINISTRY MAY SPEAK",
         name="THE PODIUM OF<br>GLAD TIDINGS",
         sub="Rally speeches: win the crowd for your ministry.",
         steps=["Write a short rally speech that pushes your ministry's policies.",
                "Add a signature hand gesture.",
                "Take the mic and get the crowd enthusiastic about joining. How long: {TBD}"],
         reward=None, cards="None. " + GATE,
         safety="Speaking is voluntary. The crowd cheers; it never heckles.",
         checks=None, stamps=None),
    dict(n=28, floor="Everywhere", loc="Everywhere",
         ministry=None, kicker="WHO THE POLICE ARE: {TBD:#28b}",
         name="THE CIVIC<br>COURTESY PATROL",
         sub="Police: what to do when an officer stops you.",
         steps=["Stay calm and show your passport when asked.",
                "Answer the officer's questions. Questions are welcome; they have already been answered.",
                "Caught cheating? No credits are taken. You are corrected at Interrogation or Carbon Confessions (stamp on page 3)."],
         reward="No credits from the police. Only correction: a status stamp on passport page 3.",
         cards="Some quests involve the police; who they are: {TBD:#28b}. " + GATE,
         safety="Officers never search, touch or take anything without your yes.",
         checks="Spot checks on cards and stamps. Send cheaters to Interrogation (#34) or Carbon Confessions (#18).",
         stamps="None. Correction stamps are given at #34 / #18."),
    dict(n=29, floor="Everywhere", loc="Everywhere (the speakers)",
         ministry=None, kicker="R.E.I.G.N. ITSELF",
         name="THE VOICE<br>OF R.E.I.G.N.",
         sub="Intercom announcements: when R.E.I.G.N. speaks, listen.",
         steps=["When the speakers chime, stop and listen.",
                "Do what the voice asks, cheerfully, right away.",
                "Laughing at an announcement may be noticed. The Guardian forgives most of it."],
         reward="No credits for listening.",
         cards="<b>M25</b> Announcement duty: posted by the speakers during an announcement. " + GATE,
         safety="An announcement never overrides your own yes or no.",
         checks="Script: slogans.qmd, Intercom one-liners (#29). Announcer: {TBD}",
         stamps="None."),
    dict(n=30, floor="Downstairs", loc="Beside the bar, centre of the garage",
         ministry=None, kicker="ALL TEN MINISTRIES · NO MINISTRY RUNS IT",
         name="WHERE YOUR<br>MINISTRY MEETS",
         sub="Ministry goal setting: meet your ministry, decide what it wants tonight.",
         steps=["Find the citizens of your ministry. Your ministry is on passport page 2.",
                "Work out together who you are, what your ministry is about, and what it wants to achieve.",
                "Leave with a plan: credits for your ministry, and something to show at the Grand Assembly, <b>23:30</b>."],
         reward=None, cards="None. " + GATE,
         safety="Nobody leads unless the ministry chooses it. Join in your own way.",
         checks="The gate sends every new citizen here. Help them find their ministry.",
         stamps=None),
    dict(n=31, floor="Downstairs", loc="Centre of the garage (was the welcome bar)",
         ministry=None, kicker="THE RESISTANCE", resist=True,
         name="YOU ARE<br>A HUMAN HERE",
         sub="The rebel bar.",
         steps=["Come in quietly. Bring only a citizen you trust.",
                "Tear out your debt page and rip it up, here, in front of a rebel.",
                "Want to join? Only a rebel can give you the stamp."],
         reward="Rebel quests give stamps like any quest. " + GATE,
         cards="<b>RB06</b> rip up your debt page here · <b>RB07</b> bring a trustworthy citizen here. What We Know wall: {TBD:where}",
         safety="Drink water as well. Joining is always your own choice.",
         checks="Public bar or hidden: {TBD}. Bar team: {TBD}",
         stamps="None at the bar."),
    dict(n=32, floor="Downstairs", loc="Garage, a car park: {TBD:which one}",
         ministry="Humus",
         name="THE PRIVILEGE<br>OF RENEWAL",
         sub="Recycling plant: citizens (and confiscated items) are renewed here.",
         steps=["Sent here? Congratulations: it is a promotion, not a punishment.",
                "Go through renewal with the operators. What it involves (ritual, new name, debt): {TBD}",
                "Leave renewed: the operator stamps <b>RENEWED</b> in the RECYCLING box, passport page 3."],
         reward=NOCRED_P3 + ": <b>RENEWED</b>.",
         cards="<b>H4</b> hacker renewed · <b>S2</b> confiscated item processed · <b>I39</b> ask a renewed citizen · <b>M28</b> ministry visit. " + GATE,
         safety="Renewal is theatre: nothing physical is forced. You may say no at any time.",
         checks="H4: renewal with the witness watching. S2: item processed with ceremony. M28: tell visitors how citizens are renewed.",
         stamps="RECYCLING · RENEWED on p. 3 (if the stamp is made)."),
    dict(n=33, floor="Downstairs", loc="Garage entrance",
         ministry="Service",
         name="THE MINISTRY WILL<br>SEE YOU NOW",
         sub="Inburgering: the gate. Passport, ministry, quest, and stamps for finished cards.",
         steps=["Arrive 20:30-21:00. Applied? Give your name. Not on the list? A few questions first, at Interrogation.",
                "Take your passport and quest card. Your debt is on page 2. <b>1 stamp = 100 CC</b>.",
                "After 21:00 the gate is the quest desk: hand in finished cards, get your stamps and your next chain step."],
         reward="Quest cards are stamped here: <b>1, 2 or 3 stamps</b> per card. The top 3 ministries compete at 23:30.",
         cards="<b>All finished cards</b>. Chains (Hacker, Data Centre, Smuggler): the next step is given here.",
         safety="Nothing is searched or taken. You can step out of the game at any time.",
         checks="Both reg. nos. on the back vs the ministry lists. Keep the card, tick the issuing ministry's sheet, into its tray.",
         stamps="Seal on the card, ENTRY p. 2, VERDICT p. 3 (if made), credit stamps p. 6-7."),
    dict(n=34, floor="Downstairs", loc="Garage entrance",
         ministry=None,
         name="QUESTIONS<br>ARE WELCOME",
         sub="Interrogation: a short carbon audit for citizens who did not apply.",
         steps=["Take the chair. Two officers ask about your carbon habits.",
                "Answer as you like. Questions are welcome; they have already been answered.",
                "Leave with your carbon debt and <b>ANSWERED</b> in the INTERROGATION box, passport page 3."],
         reward=NOCRED_P3 + ": <b>ANSWERED</b>.",
         cards="<b>H2</b> The Hacker, step 2: escorted here, three questions about the stolen file. Walk-ins and caught cheaters come here too. " + GATE,
         safety="You can say no. The door stays open. About 2 minutes, never more. Nobody touches you.",
         checks="Walk-ins: set the debt ({TBD:default 200-300 CC}), then Desk 6. H2: three questions, then stamp the hacker's p. 3.",
         stamps="INTERROGATION · ANSWERED + VERDICT on p. 3 (if made)."),
]

# --------------------------------------------------------------- RENDER
HDR_H = 17


def header(resist=False):
    w, h = 128, HDR_H
    if resist:
        body = (f'<rect width="{w}" height="{h}" fill="#fff"/>'
                f'<line x1="4" y1="{h / 2}" x2="{w / 2 - 11}" y2="{h / 2}" stroke="{RED}" stroke-width="0.8"/>'
                f'<line x1="{w / 2 + 11}" y1="{h / 2}" x2="{w - 4}" y2="{h / 2}" stroke="{RED}" stroke-width="0.8"/>'
                + mt.inner_svg(mt.RESIST, w / 2 - 8, 0.5, 16))
    else:
        body = (f'<rect width="{w}" height="{h}" fill="#111"/>' + mt.sunburst(w / 2, h + 4, 110, 40, "#333")
                + mt.stag(w / 2, 1.2 + 78 * 0.122, 0.122, mt.PAPER, "#111"))
    return mt.svg_doc(w, h, body).replace("<svg ", '<svg class="hdr" ', 1)


def kicker(s):
    if s.get("kicker"):
        return t(s["kicker"])
    if s["ministry"]:
        return f'UNDER THE CARE OF THE MINISTRY OF {s["ministry"].upper()}'
    return "MINISTRY " + tbd()


def sign(s):
    steps = "".join(f"<li><span>{t(x)}</span></li>" if x else f'<li class="blank"><span>{tbd("what you do")}</span></li>'
                    for x in s["steps"])
    loc = t(s["loc"]) if s["loc"] else tbd("location")
    crew_checks = t(s["checks"]) if s["checks"] else tbd()
    crew_stamps = t(s["stamps"]) if s["stamps"] else tbd()
    return f"""<div class="pg{' res' if s.get('resist') else ''}"><div class="frame"></div>
{header(s.get('resist'))}
<div class="k">{kicker(s)}</div>
<h1>{s['name']}</h1>
<div class="sub">{t(s['sub'])}</div>
<div class="where">{html.escape(s['floor'])} · {loc}</div>
<div class="sec">WHAT YOU DO HERE</div>
<ol>{steps}</ol>
<div class="row">
<div class="box rew"><h3>REWARD</h3>{t(s['reward']) if s['reward'] else tbd('credits / stamps')}</div>
<div class="box cards"><h3>CARDS THAT BRING YOU HERE</h3>{t(s['cards'])}</div>
</div>
<div class="safe"><h2>SAFETY &amp; CONSENT</h2>{t(s['safety'])} One word stops all play: <b>OZONE</b>.</div>
<div class="crew"><h3>CREW</h3>
<p><b>Check:</b> {crew_checks}</p>
<p><b>Stamp:</b> {crew_stamps}</p>
<p class="dim">Crew-run station. No ministry scores for running it. Safety lead {tbd('name / tel')} Medical {tbd('name / tel')}</p>
</div>
<div class="foot">Station #{s['n']} · R.E.I.G.N. decides, so that citizens are free.</div>
</div>"""


CSS = f"""{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#444;-webkit-print-color-adjust:exact;print-color-adjust:exact;font-family:'Archivo','DejaVu Sans',sans-serif;color:#111}}
.pg{{width:148.5mm;height:210mm;background:#fff;margin:6mm auto;padding:7.5mm 9.5mm 7mm;display:flex;flex-direction:column;position:relative;overflow:hidden}}
.frame{{position:absolute;inset:4.5mm;border:2px solid #111;pointer-events:none}}
.frame:after{{content:"";position:absolute;inset:1.2mm;border:.6px solid #111}}
.hdr{{display:block;width:128mm;height:{HDR_H}mm;margin:0 auto 2mm;flex:none}}
.k{{font-family:'Archivo Black',sans-serif;font-size:7.6pt;letter-spacing:1.6px;text-align:center;color:{RED}}}
h1{{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:22pt;line-height:.98;text-align:center;margin:1.2mm 0 1.2mm}}
.sub{{font-size:9.2pt;font-weight:700;font-style:italic;text-align:center;line-height:1.2}}
.where{{font-size:7.6pt;font-weight:800;text-align:center;letter-spacing:.6px;text-transform:uppercase;margin:1.2mm 0 2mm}}
.sec{{font-family:'Archivo Black',sans-serif;font-size:8pt;letter-spacing:1.6px;border-top:2px solid #111;padding-top:1.2mm;margin-bottom:1.6mm}}
ol{{list-style:none;counter-reset:r;display:flex;flex-direction:column;gap:1.9mm}}
ol li{{counter-increment:r;display:flex;gap:2.3mm;align-items:flex-start;font-size:10pt;font-weight:700;line-height:1.22}}
ol li:before{{content:counter(r);flex:none;width:6mm;height:6mm;border-radius:50%;background:#111;color:#fff;
 font-family:'Archivo Black',sans-serif;font-size:9pt;display:flex;align-items:center;justify-content:center;margin-top:-.3mm}}
ol li.blank span{{flex:1;display:block}}
ol li.blank .tbd{{display:block;height:6mm;line-height:6mm;padding:0 2mm}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:2mm;margin:2.6mm 0 2.2mm}}
.box{{border:2px solid #111;border-radius:1.5mm;padding:1.3mm 1.8mm;font-size:7.8pt;font-weight:700;line-height:1.25}}
.box h3{{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:7.4pt;letter-spacing:1.2px;color:{RED};margin-bottom:.6mm}}
.safe{{margin-top:auto;background:#111;color:#fff;padding:1.8mm 2.6mm;font-size:8pt;font-weight:700;line-height:1.28}}
.safe h2{{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:8.4pt;letter-spacing:1px;margin-bottom:.4mm}}
.safe .tbd{{background:#444;color:#ddd}}
.crew{{border:1px dashed #111;margin-top:2mm;padding:1.2mm 2mm;font-size:6.9pt;font-weight:700;line-height:1.25}}
.crew h3{{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:6.8pt;letter-spacing:1.4px;margin-bottom:.3mm}}
.crew p+p{{margin-top:.4mm}}
.crew .dim{{color:#555;font-weight:600}}
.tbd{{display:inline-block;background:#e6e6e6;color:#6a6a6a;font-family:'Archivo',sans-serif;font-weight:700;font-style:normal;
 font-size:.82em;letter-spacing:.4px;padding:0 1.4mm;border-radius:.8mm;min-width:16mm;text-transform:none}}
.foot{{font-size:6.6pt;font-weight:700;font-style:italic;text-align:center;margin-top:1.4mm}}
.res .k{{color:#111}}
@page{{size:148.5mm 210mm;margin:0}}
@media print{{body{{background:none}}.pg{{margin:0;page-break-after:always}}}}"""

TWO = (CSS.replace("@page{size:148.5mm 210mm;margin:0}", "@page{size:297mm 210mm;margin:0}")
       .replace(".pg{margin:0;page-break-after:always}", ".pg{margin:0}")
       + ".two{width:297mm;height:210mm;display:flex;background:#fff;margin:6mm auto;position:relative}.two .pg{margin:0}"
       + ".two .cut{position:absolute;left:148.5mm;top:0;bottom:0;border-left:.3mm dashed #999}"
       + "@media print{.two{margin:0;overflow:hidden;page-break-after:always}}")


def doc(title, css, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{css}</style></head><body>{body}</body></html>')


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    with open(p, "w") as f:
        f.write(content)
    return p


def render_and_check(paths):
    """PDF via Chromium; fail loudly if any sign's content overflows its A5 page."""
    from playwright.sync_api import sync_playwright
    bad = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.set_default_timeout(300_000)
        for p in paths:
            pg.goto("file://" + p, wait_until="networkidle")
            pg.evaluate("document.fonts.ready.then(() => true)")
            pg.emulate_media(media="print")
            over = pg.evaluate("""() => [...document.querySelectorAll('.pg')].map((el, i) => {
                const pad = parseFloat(getComputedStyle(el).paddingBottom);
                const lim = el.getBoundingClientRect().bottom - pad + 0.5;
                const last = [...el.children].filter(c => !c.classList.contains('frame')).pop();
                return [i, el.scrollHeight - el.clientHeight, last.getBoundingClientRect().bottom - lim];
            }).filter(([i, s, d]) => s > 0 || d > 0)""")
            bad += [(os.path.basename(p), *o) for o in over]
            pg.pdf(path=p[:-5] + ".pdf", prefer_css_page_size=True, print_background=True)
            print(p[:-5] + ".pdf")
        b.close()
    return bad


if __name__ == "__main__":
    signs = [sign(s) for s in STATIONS]
    a5 = write("station_signs_A5.html", doc("Ecotopia station signs A5", CSS, "".join(signs)))
    sheets = "".join(f'<div class="two">{signs[i]}{signs[i + 1] if i + 1 < len(signs) else ""}<div class="cut"></div></div>'
                     for i in range(0, len(signs), 2))
    two = write("station_signs_2xA5_on_A4.html", doc("Ecotopia station signs 2x A5 on A4", TWO, sheets))
    bad = render_and_check([a5, two])
    final = os.path.join(HERE, "PRINT_ALL_station_signs.pdf")
    shutil.copy(two[:-5] + ".pdf", final)
    print(final)
    if bad:
        for f, i, s, d in bad:
            print(f"OVERFLOW {f} page {i + 1}: scroll {s}px, last block {d:.1f}px past the margin")
        sys.exit(1)
    print(f"{len(STATIONS)} signs, {(len(STATIONS) + 1) // 2} A4 sheets, no overflow")
