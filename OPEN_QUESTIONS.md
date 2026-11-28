# Ecotopia: open questions about the party

Collected 2026-11-26 (party: Sat 28 Nov). "Known so far" = what CANON.md or the citizen export already says.

**Quest system (cards, chains, roles, scoring): see QUEST_SYSTEM.md.**

## For the call with Jack (blocks printing)

- ~~#6 Stamps vs credits~~ ANSWERED: stamps are just credits.
- ~~#6b Win condition~~ ANSWERED: the top 3 ministries (most credits) compete at the midnight Grand Assembly for the right to Ascension. Every stamp = 100 CC; quests give 1, 2 or 3 stamps.
- **#6c Ascension:** how do the top 3 compete (performance, jury, applause)? Who judges? What does Ascension mean in the story?
- **#11 Who gives the stamps:** the stations themselves? Who stamps quests and − credits? Stamp sets per station?
- **#16 Alliances and rivalries:** which ministries are allies and rivals? (Jack's doc.) Print on the passport?
- **#28b Who is the police?** Link to the Ministry of Vigilance: (A) crew police in Vigilance uniform, or (B) Vigilance citizens deputised as police? 9 quests depend on it.
- **#8 / #9 The end:** when is the score counted, and who counts it?
- **#15 Quests:** game cards, many per citizen. How many at the door, where do they get new ones, and how many copies of each card do we print?
- **#1 The 20 unplaced citizens:** place them now (spread over the smallest ministries) or at the door?
- **#18 Rebel cards:** disguise them as personal quests?

## Ministries

1. **Do we assign players to ministries right away?**
   Known so far: yes. The site says every citizen is assigned one ministry and one quest at intake.
   130 of 150 citizens in the export already have a ministry (11 to 15 each). 20 are "Not yet placed".
   Open: who places those 20 (spread them over the smallest ministries?), and when: before printing or at the door?
2. ~~Do ministries interact with specific stations/experiences for extra points?~~ **ANSWERED: no. Ministries are NOT aligned with the experiences in any way.**
   Follow-up: CANON.md still says ministries can "support" stations and earn credits for it. Remove that line?
3. ~~Is a station also the "head" of a ministry/faction?~~ **ANSWERED: no** (same answer as #2; matches CANON).
4. **Do ministries get special powers?** (e.g. Ministry of Industry gets half of the carbon debt for taking on new people)
   Open. Nothing defined yet.
5. **Ministry mandates** (what each of the ten is about) are still DRAFT in CANON.md (#4). Who signs them off?

## Scoring and credits

6. ~~Stamps vs credits~~ **ANSWERED: stamps are just credits.** UPDATE: every stamp is worth 100 CC; quests give 1, 2 or 3 stamps.
   Quest rewards 1 / 2 / 3 are printed on the cards as +25 / +50 / +100 CC.
   Still open: are there − stamps, and what values? The STL set in stamps/stampmaker_stl_small has +10/+20/+50 and −10/−20/−50: are there new +25/+50/+100 stamps?
6b. ~~What decides the winning ministry?~~ **ANSWERED: the ministry with the most credits at the end wins** (as printed on passport page 7).
7. ~~Are 24 credit boxes enough?~~ The passport now has **40 square 15.5 mm credit boxes** (fits the 15 mm credit stamps).
8. **Win condition: the ministry with the most credits at the end wins.** When is "the end": the midnight Grand Assembly, or later?
9. **Who counts the ministry totals, and how?** Collect passports? Officials with a tally sheet? Live scoreboard?
10. **What does the winning ministry get?**
11. **Who holds the + and − stamps?** (FOR THE CALL WITH JACK) Chris: maybe the experiences/stations give the stamps themselves.
   **ANSWERED (quests): completed quests are stamped either at the door or by the experience/station.** Printed on every quest card.
   Open: does each station get its own credit stamp set? Who gives − stamps? How many stamp sets do we have?
   The passport is neutral on this ("each earns you + credit stamps"), so printing does not depend on the answer.
12. **What earns − stamps exactly?** (unsustainable behaviour, rule-breaking, getting caught by the police: is there a list for officials/police?)
13. **What is the "Clearance / permit" page (page 8) used for?** Who signs it, and what does it unlock?
14. **Do the gun range and other stations give credits?** How many, and is it per hit/score?

## Quests

15. ~~How are quests handed out?~~ **ANSWERED: quests are game cards, and citizens do many of them.** (No quest on the passport.)
   Open: how many cards does a citizen get at the door? Where do they get new ones (door, stations, a draw pile)? Do they hand in finished cards?
   111 unique cards: if 150+ citizens each do several, do we print several copies of each card?
16. **Rival (R) and Collaboration (C) quests need ministry pairings.** (FOR THE CALL WITH JACK) Who is whose rival and ally? Print it on the passport (page 2: "Your ally: X · Your rival: Y")?
   Found so far: old quest_cards_and_facilitator_pack.md (Part IV, pre-purge) has rivals: Purity↔Flow, Vigilance→Joy→Industry→Humus→Light→Breath→Radiance→Service→Vigilance. No alliances anywhere; Jack's design doc (#3) may have them.
   Proposal: 5 mutual rival pairs (Purity–Flow, Vigilance–Joy, Industry–Humus, Light–Breath, Radiance–Service) + 5 different mutual ally pairs.
   ~~Card backs~~ **APPROVED (2026-11-26): every quest must be confirmed (signed) by a citizen of the ministry on the back of the card.** This forces cooperation (and non-cooperation) between ministries.
   **Quest flow (2026-11-26):** cards are handed out at the gate and stamped there with the **ministry seal** of the ministry whose interest the quest serves (front). The **back** names the **issuing ministry**; the **witness must be a citizen of that issuing ministry**. Back has citizen numbers only (completed by + witness), no names. The **seal on the front** = the ministry that scores the quest. The finished card is handed in (and goes back in the deck) for the credit stamps.
   **Anti-cheat:** card kept when stamped; witness writes citizen no.; only officials hold stamps; officials count; police spot checks give − stamps. **Scoreboard at the gate** (Chris makes it).
   **Issuing ministry per quest:** assigned by mandate in passport_v2/quest_ministries.py (9-13 per ministry); RB quests have a RESISTANCE back (witness = a fellow rebel). Review/edit that file.
   **Secret victory "Most supportive ministry":** the ministry whose quests were completed most (count the handed-in cards per back). Not printed anywhere. Gate needs a tray per ministry for handed-in cards.
   Open: which seal goes on which card at the gate (the citizen's own ministry, or a fixed ministry per quest)? Who updates the scoreboard, and how often?
   Still open: random backs, or tie them to the quest type (rival quests confirmed by your rival, collaboration quests by your ally)?
17. **Ministry (M) quests: one card per ministry, or one per citizen?**
18. **Rebel (RB) quests:** CANON says nobody can tell rebels apart, but the cards currently say "REBEL QUEST" and IDs start with RB. Disguise them as personal quests?
19. **How many rebels, and how are they chosen?**
20. **What do the rebels win?** How does the resistance raid at the Grand Assembly interact with the ministry competition?
21. **Physical quest props:** data centres (7), the "What We Know" wall, cipher card, HUMUS_DELETIONS folder, rule posters: who makes and places them?

## People and safety

22. **Walk-ins:** who places them in a ministry, and what starting debt do they get? (Site: "processed at the door: a longer wait, and further obligations.") How many blank passports do we need? (40 generated now)
23. **Stepping out of the game:** what happens to that citizen's passport and credits? Who do they tell?
24. **Flags in the export:** 3 Governors, 24 "Spoilers seen", 7 "Asked if it is a party". Does any of these get a role or special treatment? What is a Governor at the party?
25. **Safe word OZONE:** who is briefed, and what happens exactly when someone says it?
26. **Camera:** what is it for, and how do we handle consent and privacy (#74, #76)?

## Stations and story (from CANON.md)

27. **Suicide booth (#24):** it's on the crew station plan but was marked for purge. Keep and re-voice, or drop?
   Also: should the entrance verdict on the passport (page 3) be able to send someone there? Not printed for now; the verdicts are Approved / Further obligations / Sent to recycling / Denied, report back.
28. **Stations with no owner yet:** ministry ritual preparation, rally speeches, police, intercom announcements, ministry goal setting, rebel bar, recycling pant. Who runs them?
28b. **Who is the police (#28)?** Nobody yet. CANON: police are crew playing R.E.I.G.N. Quests that need them: I05, I22, I42, I48, M05, M15, M25, R02, RB04.
   Proposal: link the police to the **Ministry of Vigilance** (CANON: "keeps the list; receives every concern").
   (A) crew police wearing the Vigilance stag, or (B) the Vigilance ministry citizens are deputised as police, led by crew.
   B links the game strongly but contradicts "ministries are not aligned with experiences" (#2).
29. **Shooting range (#20, Chris):** where does it go (#71)?
30. ~~Ottobots: what is their role in the night (#64)?~~ **DROPPED for 28 Nov** (too ambitious). Epic #63 closed as not planned.
31. **Old climax ("expose the cellar AI server") vs the site's AI ban:** which climax are we running?
32. **Design doc from /creators (#3):** still not downloaded. It may already answer many of the questions above.
33. **The public Quarto site names the venue ("De Warren")** while the official site keeps it secret. Fix or accept?

## Printing

34. **Edge-to-edge passports:** the Brother HL-2150N can't print the last ~4 mm at the edges, so the outer frame lines may get clipped. OK, or bring back a small margin?
35. **Quest cards:** keep standard playing-card size (63×88 mm), or enlarge to fill the A4 (~70×99 mm)?
