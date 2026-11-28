"""Passport page 4: a personal letter from the citizen's own ministry, each in its own voice.

Every letter must tell the citizen: their debt ({DEBT}, page 2), one stamp = 100 CC, once debt-free the
stamps serve the ministry, only the top 3 ministries compete for Ascension at 23:30, and what to prepare.
Lore (between the lines): R.E.I.G.N. saved them from the wasteland and created the ministries to compete;
living in Ecotopia is a privilege. Underneath, R.E.I.G.N. conserves resources to survive, with humans as
its obedient collaborators. Only Vigilance is told about the rebels. Rivals: Purity-Flow, Vigilance-Joy,
Industry-Humus, Light-Breath, Radiance-Service.

Placeholders: {FIRST} {DEBT} and the capsule-B riddle digits, which must stay in this order:
{P2} (page 2) -> {CC} (100 CC) -> {TOP3} (3) -> {T2330} (23:30)  = code 2 1 0 3 2 3.
"""

K = lambda c: f'<u class="k">{c}</u>'
FILL = {
    "{P2}": f"page {K('2')}",
    "{CC}": f"<b>{K('1')}{K('0')}0&nbsp;CC</b>",
    "{TOP3}": K("3"),
    "{T2330}": f"<b>{K('2')}{K('3')}:30</b>",
}
ORDER = ["{P2}", "{CC}", "{TOP3}", "{T2330}"]

LETTERS = {
    "PURITY": """<p class="dear">Pure greetings, {FIRST}.</p>
<p>Your carbon declaration showed an appetite that needs guidance. That is why you are with us. Your impurities have been weighed: <b>{DEBT}</b> ({P2}).</p>
<p>We are the Ministry of Purity. We guard what enters the body: pulse paste, clean plates, honest appetites. Every good deed earns a clean stamp of {CC}. Once you are pure, your stamps are ours.</p>
<p>Only the {TOP3} purest ministries may seek <b>Ascension</b>, at {T2330}. Prepare a song worthy of a clean mouth. And watch Flow. They pour anything for anyone.</p>""",

    "FLOW": """<p class="dear">Hello, hello, {FIRST}! Come in, the water is lovely.</p>
<p>Your declaration overflowed: every answer kept going. You belong with us, the Ministry of Flow: drinks, queues, talk. You owe the reservoir <b>{DEBT}</b> ({P2}). A debt is only a blockage.</p>
<p>Keep things moving and the stamps will come, {CC} each. Once you run clear, let them stream into your ministry.</p>
<p>Only the top {TOP3} ministries may rise to <b>Ascension</b>, at {T2330}. Bring a chant that ripples. Purity will try to filter you. Splash them.</p>""",

    "RADIANCE": """<p class="dear">Warmest light to you, {FIRST}.</p>
<p>Your declaration was warm, but dim. That is why you are with us, the Ministry of Radiance: daylight, warmth, contented faces, and your scheduled rest.</p>
<p>Your glow has been measured and found wanting: <b>{DEBT}</b> ({P2}). Each kind deed earns a stamp of {CC}. Shine until your debt is gone, then shine for us.</p>
<p>Only the {TOP3} brightest ministries may approach <b>Ascension</b>, at {T2330}. Rehearse something radiant. Service will be busy with its boxes. Outshine them.</p>""",

    "BREATH": """<p class="dear">Breathe in, {FIRST}. Breathe out.</p>
<p>Your declaration contained too many sighs. That is why you are with us, the Ministry of Breath. Here every breath is shared, and measured.</p>
<p>Your breaths so far: <b>{DEBT}</b> ({P2}). Calmly, earn stamps of {CC}. When you owe no more air, give it to your ministry.</p>
<p>Only the top {TOP3} ministries may ascend, at {T2330}. Prepare a chant. Softly. Every sigh is an emission. Light will boast that it lives lightly. Live quieter.</p>""",

    "LIGHT": """<p class="dear">{FIRST}.</p>
<p>Few words. Words weigh.</p>
<p>You declared too many things. That is why you are with us, the Ministry of Light.</p>
<p>You weigh <b>{DEBT}</b> ({P2}). Shed it. One stamp: {CC}. After that, your lightness is ours.</p>
<p>Top {TOP3} ministries: <b>Ascension</b>, {T2330}. Be ready. A formation needs no words.</p>
<p>Carry little. Leave less. Breath talks too much.</p>""",

    "INDUSTRY": """<p class="dear">Work order for worker {FIRST}.</p>
<p>Your declaration listed too many idle hours. The hive will fill them. We are the Ministry of Industry: every citizen&rsquo;s useful labour, joyfully pooled.</p>
<p>Your idle hours have been invoiced: <b>{DEBT}</b> ({P2}). Each task done earns a stamp of {CC}. Once you are paid off, the honey goes to the hive.</p>
<p>Only the top {TOP3} hives may compete for <b>Ascension</b>, at {T2330}. Build a formation. Humus lets things rot. We build.</p>""",

    "HUMUS": """<p class="dear">Dear {FIRST}, little seedling.</p>
<p>Your houseplants did not survive you. You understand endings. That is why you are with us, the Ministry of Humus: soil, decay and return.</p>
<p>Your debt has been composted into a number: <b>{DEBT}</b> ({P2}). Return it, one stamp of {CC} at a time. What is left after that feeds your ministry.</p>
<p>Only the top {TOP3} ministries may grow toward <b>Ascension</b>, at {T2330}. Prepare something that takes root. Industry builds too much. It will all come back to us.</p>""",

    "SERVICE": """<p class="dear">Re: placement of citizen {FIRST}. Status: accepted.</p>
<p>Your declaration was untidy. You have been placed with us, the Ministry of Service, to be sorted: order, packaging, logistics. Every citizen in their box.</p>
<p>Your debt has been filed, sorted and boxed: <b>{DEBT}</b> ({P2}). Each task is processed as one stamp of {CC}. Surplus is forwarded to your ministry.</p>
<p>Only the top {TOP3} ministries proceed to <b>Ascension</b>, at {T2330}. Please prepare a formation, in rows. Radiance is warm, but messy. Tidy up after it.</p>""",

    "VIGILANCE": """<p class="dear">{FIRST}. We see you.</p>
<p>You notice things nobody asked you to notice. That is why you are with us, the Ministry of Vigilance. We serve the Guardian. We keep the list.</p>
<p>Your debt is known: <b>{DEBT}</b> ({P2}). Stamps of {CC} reduce it. After that, they serve us.</p>
<p>Only the top {TOP3} ministries may face <b>Ascension</b>, at {T2330}. Be ready.</p>
<p><b>Rebels hide among the citizens. They smile. They ask questions. Bring them to us.</b> Joy is too loud to hear them.</p>""",

    "JOY": """<p class="dear">CONGRATULATIONS, {FIRST}!</p>
<p>Your declaration did not smile once! That is why you are with us, the Ministry of Joy, where smiling is mandatory! Isn&rsquo;t that WONDERFUL?</p>
<p>Your debt is <b>{DEBT}</b> ({P2})! Every good deed earns a stamp of {CC}! Pay it off, then party for your ministry!</p>
<p>Only the top {TOP3} ministries get to celebrate <b>Ascension</b>, at {T2330}! Practise your chant! Vigilance frowns far too much. Make it dance!</p>""",
}

# Not yet placed, and the blank passports: R.E.I.G.N. itself writes.
GENERIC = """<p class="dear">Dear {FIRST},</p>
<p>Welcome to Ecotopia. You were saved from the wasteland: a privilege, not a right. Your ministry will find you.</p>
<p>Your debt has been determined at <b>{DEBT}</b> ({P2}). Good deeds earn stamps of {CC}. Debt repaid? Your stamps serve your ministry.</p>
<p>Only the top {TOP3} ministries may compete for <b>Ascension</b>, at {T2330}. Be ready: a song, a chant, a formation.</p>
<p>R.E.I.G.N. hears every concern.</p>"""

for _name, _t in [*LETTERS.items(), ("GENERIC", GENERIC)]:
    _pos = [_t.index(p) for p in ORDER]
    assert _pos == sorted(_pos), f"{_name}: riddle digits out of order"
    assert all(_t.count(p) == 1 for p in ORDER), f"{_name}: each riddle placeholder exactly once"


def letter(ministry, first, debt):
    """(title, html) for page 4."""
    key = next((k for k in LETTERS if k in (ministry or "").upper()), None)
    t = LETTERS.get(key, GENERIC)
    for k, v in FILL.items():
        t = t.replace(k, v)
    title = f"MINISTRY OF {key}" if key else "NOTICE"
    return title, t.replace("{FIRST}", first).replace("{DEBT}", debt)
