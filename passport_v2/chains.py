"""Chain quests and secret role cards (card game + role play).

A ROLE card is handed out at the gate to a volunteer, who plays that character all night.
Chain quests: only step 1 is handed out at the start. Hand in a step at the gate -> you get the next step.
Each step is issued by a different ministry, so the ministries depend on each other.
mode: W = witness, T = together (takes part), D = report (bring it/them to the ministry).
"""

ROLES = [
    # id, chain, text, reward
    ("H0", "THE HACKER",
     "You are THE HACKER. You stole a file from R.E.I.G.N. Keep this card hidden. "
     "Asked \"Are you the hacker?\" Deny it twice. The third time, confess and play the captive.",
     "Still free at 23:00? 3"),
    ("S0", "THE SMUGGLER",
     "You are THE SMUGGLER. Hide one forbidden item on you: a plastic straw, a sweet, a lighter. "
     "If an inspector finds it, hand it over with a sigh and follow it through the system.",
     "Item never found? 2"),
]

CHAINS = [
    # id, chain, step, of, issuer, mode, text, stamps
    ("H1", "THE HACKER", 1, 4, "VIGILANCE", "D",
     "A hacker hides among us. Ask citizens \"Are you the hacker?\" until one confesses. "
     "Done when you bring them to a Vigilance citizen.", "2"),
    ("H2", "THE HACKER", 2, 4, "SERVICE", "T",
     "Escort the captured hacker to the Interrogation station. Ask THREE questions about the stolen file. Done after the third answer.", "2"),
    ("H3", "THE HACKER", 3, 4, "RADIANCE", "D",
     "Bring the hacker to Carbon Confessions to be corrected. Done when they have confessed loudly, with a smile, to a Radiance citizen.", "2"),
    ("H4", "THE HACKER", 4, 4, "HUMUS", "W",
     "Walk the corrected hacker to the recycling plant. Done when they have been renewed, with your witness watching.", "3"),
    ("D1", "THE DATA CENTRE", 1, 3, "HUMUS", "D",
     "Find a R.E.I.G.N. data centre and memorise its message. Done when you recite it word for word to a Humus citizen.", "2"),
    ("D2", "THE DATA CENTRE", 2, 3, "VIGILANCE", "T",
     "Decode the data centre message together with a Vigilance citizen. Done when you agree on what R.E.I.G.N. is hiding.", "2"),
    ("D3", "THE DATA CENTRE", 3, 3, "SERVICE", "D",
     "Turn the decoded message into a cheerful official announcement. Done when you deliver it to a Service citizen.", "3"),
    ("S1", "THE SMUGGLER", 1, 3, "LIGHT", "D",
     "A smuggler carries a forbidden item. Inspect citizens, with a yes, until you find it. "
     "Done when you bring the item and its owner to a Light citizen.", "2"),
    ("S2", "THE SMUGGLER", 2, 3, "HUMUS", "T",
     "Take the confiscated item and its owner to the recycling plant. Done when the item is processed, with ceremony.", "2"),
    ("S3", "THE SMUGGLER", 3, 3, "JOY", "W",
     "Return the processed item to the smuggler with a celebration. Done when 5 citizens join in.", "2"),
]

NOTES = {
    "H0": "Caught? You go along: Vigilance, Interrogation, Carbon Confessions, Recycling.",
    "H1": "A hacker may deny it twice. The third time, they must confess.",
    "H2": "The Interrogation station stamps the hacker's passport. Questions only: no touching.",
    "H3": "Carbon Confessions is in the Kinderkamer.",
    "H4": "The recycling plant is a station. Lost? Ask any official.",
    "D1": "There are 7 data centres in the house: small boxes with a R.E.I.G.N. label.",
    "D2": "No right answer: agree on one meaning together and remember it.",
    "S1": "Ask before you inspect. Pockets and bags only if they say yes.",
    "S2": "The recycling plant is a station. Lost? Ask any official.",
}
