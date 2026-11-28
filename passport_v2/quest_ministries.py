"""Which ministry issues each quest (printed on the card back; its citizens witness it).

Chosen by mandate (CANON.md, ministries table). Edit freely, then re-run make_quest_cards.py.
Rebel quests (RB) are issued by the resistance, not by a ministry.
Secret "most supportive ministry" victory: count the handed-in cards per back.
"""

ISSUER = {
    # PURITY: what enters the body, honest appetites
    "I01": "PURITY", "I02": "PURITY", "I29": "PURITY", "I32": "PURITY", "I43": "PURITY",
    "M12": "PURITY", "R01": "PURITY", "R08": "PURITY", "C04": "PURITY",
    # RADIANCE: warmth, light, the glow of a contented face
    "I11": "RADIANCE", "I12": "RADIANCE", "I18": "RADIANCE", "I40": "RADIANCE", "M07": "RADIANCE",
    "M19": "RADIANCE", "M21": "RADIANCE", "R05": "RADIANCE", "R11": "RADIANCE", "C05": "RADIANCE",
    # BREATH: air, whispers, sighing is an emission
    "I09": "BREATH", "I14": "BREATH", "I23": "BREATH", "I21": "BREATH", "M22": "BREATH",
    "M13": "BREATH", "R06": "BREATH", "I07": "BREATH", "C08": "BREATH",
    # FLOW: drinks, queues, conversation
    "I06": "FLOW", "I13": "FLOW", "I15": "FLOW", "I36": "FLOW", "M06": "FLOW",
    "M08": "FLOW", "M30": "FLOW", "R03": "FLOW", "I10": "FLOW", "C02": "FLOW",
    # LIGHT: living lightly, possessions, the weight of a citizen
    "I17": "LIGHT", "I27": "LIGHT", "I35": "LIGHT", "I44": "LIGHT", "I46": "LIGHT",
    "I49": "LIGHT", "M09": "LIGHT", "M18": "LIGHT", "R04": "LIGHT", "C06": "LIGHT",
    # INDUSTRY: the hive, useful labour
    "I19": "INDUSTRY", "I25": "INDUSTRY", "I38": "INDUSTRY", "M10": "INDUSTRY", "M14": "INDUSTRY",
    "M23": "INDUSTRY", "M24": "INDUSTRY", "M27": "INDUSTRY", "C01": "INDUSTRY", "C07": "INDUSTRY",
    # HUMUS: soil, decay, return, the records
    "I03": "HUMUS", "I20": "HUMUS", "I31": "HUMUS", "I39": "HUMUS", "I47": "HUMUS",
    "M11": "HUMUS", "M16": "HUMUS", "M28": "HUMUS", "R09": "HUMUS",
    # SERVICE: order, placement, every citizen in their box
    "I08": "SERVICE", "I28": "SERVICE", "I30": "SERVICE", "I37": "SERVICE", "I45": "SERVICE",
    "M04": "SERVICE", "M26": "SERVICE", "M29": "SERVICE", "R07": "SERVICE", "C03": "SERVICE",
    # VIGILANCE: keeps the list, receives every concern
    "I05": "VIGILANCE", "I22": "VIGILANCE", "I34": "VIGILANCE", "I42": "VIGILANCE", "I48": "VIGILANCE",
    "M05": "VIGILANCE", "M15": "VIGILANCE", "M25": "VIGILANCE", "R02": "VIGILANCE", "I26": "VIGILANCE",
    # JOY: mandatory celebration
    "I04": "JOY", "I16": "JOY", "I24": "JOY", "I33": "JOY", "I41": "JOY", "I50": "JOY",
    "M01": "JOY", "M02": "JOY", "M03": "JOY", "M17": "JOY", "M20": "JOY", "R10": "JOY", "R12": "JOY",
}
RESISTANCE = "RESISTANCE"  # all RB quests

# How the issuing ministry is involved. TOGETHER: at least one of its citizens actively takes part
# (the "another ministry" / "a citizen" in the quest is from the issuing ministry). Everything else: WITNESS only.
TOGETHER = {
    "I01", "I02", "I06", "I07", "I09", "I11", "I14", "I15", "I16", "I17", "I18", "I19", "I21", "I23",
    "I24", "I25", "I27", "I28", "I29", "I30", "I32", "I33", "I34", "I35", "I36", "I38", "I40", "I41", "I43",
    "I44", "I46", "I47", "I49", "I50",
    "M01", "M02", "M03", "M04", "M10", "M11", "M12", "M20", "M22", "M26", "M28", "M30",
    "C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08",
}

# DELIVER: you bring what you found (or who you caught) TO a citizen of the issuing ministry,
# e.g. a rebel to Vigilance, a data-centre label to Humus.
DELIVER = {
    "I03", "I05", "I13", "I20", "I22", "I31", "I39", "I42", "I45", "I48",
    "M05", "M14", "M27", "M29", "R02",
}
assert not TOGETHER & DELIVER

# (I20, I22, I30 and C01-C08 notes were folded into quest_texts.py / the mode line on 2026-11-28.)
# Extra instructions for the more complex quests: printed small on the front, under the quest text.
NOTES = {
    "I03": "There are 7 data centres in the house: small boxes with a R.E.I.G.N. label.",
    "I31": "There are 7 data centres in the house: small boxes with a R.E.I.G.N. label.",
    "I39": "The recycling plant is a station. Lost? Ask any official.",
    "M28": "The recycling plant is a station. Lost? Ask any official.",
    "I48": "Found it? Do not go in. Bring a citizen of Vigilance and they fetch the police.",
    "M05": "Found it? Do not go in. Bring a citizen of Vigilance and they fetch the police.",
    "I05": "Rebels are citizens too: they may deny it. Your Vigilance contact decides.",
    "M25": "They may say no. Then thank them anyway and let them go.",
    "I10": "The toilet host always has the final say. Let anyone in a hurry pass.",
    "I37": "The toilet host always has the final say. Let anyone in a hurry pass.",
}
