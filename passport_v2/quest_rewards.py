"""Reward (stamps) per quest ID. Overrides column C of the "quests to print" tab (the xlsx stays read-only).

Decided 2026-11-28: don't be too generous with easy quests; chains must mean something.
  1 stamp  = easy: alone or with one or two people, a few minutes, nothing to find.
  2 stamps = real effort: something hidden to find, strangers from several ministries, stealth, or a crowd.
  3 stamps = the really hard ones: big searches, 20-citizen counts.
  Chains escalate per step and pay 5 at the finale (see chains.py); that is the only way past 3.
Only IDs listed here change; everything else keeps its xlsx value.
"""

REWARD = {
    # PERSONAL: easy social ones down to 1
    "I03": "1",  # one data centre photo (the D chain and I31 pay for the real search)
    "I06": "1",
    "I08": "1",
    "I15": "1",
    "I16": "1",
    "I19": "1",
    "I25": "1",
    "I29": "1",
    "I33": "2",  # was 3
    "I34": "1",
    "I39": "1",
    "I42": "1",
    "I45": "1",
    # MINISTRY: one-minute group gestures down to 1
    "M07": "1",
    "M12": "1",
    "M13": "1",
    "M16": "1",
    "M18": "1",
    "M23": "1",
    # RIVAL
    "R04": "1",
    "R07": "1",
    # COLLABORATION: only the 10-citizen slogan stays at 2 each
    "C01": "1 each",
    "C02": "1 each",
    "C04": "1 each",
    "C08": "1 each",
    # REBEL
    "RB06": "1",
}
