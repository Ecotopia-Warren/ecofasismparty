# Ecotopia quest system

Decided on 2026-11-26 (Chris), for the party on Sat 28 Nov. Reference for the gate crew and the stations.
Cards: `passport_v2/quest_cards.pdf` (fronts) + `quest_cards_backs.pdf` (backs), 61 x 90 mm stickers for poker cards.
Regenerate: `python3 passport_v2/make_quest_cards.py`, then `cd passport_v2 && python3 make_quest_doc.py` for this file.

## Scoring

- Every credit stamp is worth **100 CC**. A quest gives **1, 2 or 3 stamps** (3 = the really hard ones).
- Stamps go in the credit boxes on passport pages 6 and 7. Final balance (page 8) = carbon debt + stamps x 100.
- Every credit above 0 counts for your ministry. At the **Grand Assembly (23:30)** only the **top 3 ministries** may compete for **Ascension** (a privilege, not a right) with a song, a chant, a formation, or more.
- Scoreboard at the gate (Chris makes it).
- **Secret victory, Most supportive ministry:** the ministry whose quests were completed most. Count the handed-in cards per issuing ministry. Not printed anywhere.

## Anatomy of a card

**Front**
- Icon + kind (Personal / Ministry / Rival / Collaboration / Rebel / Chain quest / Secret role) + **issuing ministry**.
- Chain and role cards: a black bar, e.g. `THE HACKER · STEP 2 OF 4`.
- The quest. Complex quests get an **extra instruction** (i, small italic).
- **How the issuing ministry is involved** (TOGETHER / REPORT / WITNESS, below).
- Reward: number of stamps (+CC).
- **SEAL circle, "this quest scores for":** stamped at the gate with the seal of the ministry that scores the quest.

**Back** (sticker on the other side of the poker card)
- Icon + "A QUEST OF THE MINISTRY OF X" (the issuing ministry), or "RESISTANCE".
- `Completed by: reg. no. ___`
- `Witness / Taking part / Received by: reg. no. ___`: must be a citizen of the **issuing ministry**.
- Registration **numbers only, no names**. Quest ID at the bottom to match back and front when sticking.

## Three ways to involve the issuing ministry

| Mode | Front says | Back says | Example |
|---|---|---|---|
| **TOGETHER** | at least one citizen of the issuing ministry takes part | Taking part: reg. no. | slow dance with a Breath citizen; "another ministry" in a quest = the issuing ministry |
| **REPORT** | bring what (or who) you found to a citizen of the issuing ministry | Received by: reg. no. | bring a rebel or hacker to Vigilance; a data centre label to Humus |
| **WITNESS** | a citizen of the issuing ministry watches you do it | Witness: reg. no. | ask an official the same question three times (Service watches) |

Data: `passport_v2/quest_ministries.py`: `ISSUER` (chosen by mandate), modes in `TOGETHER` and `DELIVER`, extra instructions in `NOTES`.
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

- Poker cards: about **3 packs** available (3 x 52 = 156 cards, plus jokers). 123 cards designed now, so about 33 left for duplicates of popular quests or more chains.

## Open

- Rebel cards show "The Resistance" on both sides: OK, or disguise them as a ministry quest?
- Which seal goes on a card at the gate: always the citizen's own ministry?
- How many copies of each card, and how many role cards (how many hackers and smugglers)?
- Rival quests (R): rival pairings to confirm (proposal: Purity-Flow, Vigilance-Joy, Industry-Humus, Light-Breath, Radiance-Service).
- Who counts at the end, when, and who updates the scoreboard?

## All cards (123)

Per issuing ministry: Breath 9, Flow 10, Humus 12, Industry 10, Joy 14, Light 11, Purity 9, Radiance 11, Resistance 11, Service 12, Vigilance 12.

| ID | Kind | Issued by | Mode | Stamps | Quest |
|---|---|---|---|---|---|
| I01 | Personal quest | Purity | TOGETHER | 1 | Boop the nose of 5 citizens. Ask first. |
| I02 | Personal quest | Purity | TOGETHER | 1 | Kiss 3 citizens on the cheek. Ask first, and leave the credits out ... |
| I03 | Personal quest | Humus | REPORT | 2 | Find one of R.E.I.G.N.'s data centres, hidden somewhere in the hous... |
| I04 | Personal quest | Joy | WITNESS | 1 | Find your carbon twin: a citizen whose starting debt is within 50 c... |
| I05 | Personal quest | Vigilance | REPORT | 2 | There are rebels among us. Find one and report them to the police. |
| I06 | Personal quest | Flow | TOGETHER | 2 | Introduce two citizens who have never met. Stay until they find one... |
| I07 | Personal quest | Breath | TOGETHER | 1 | Slow dance with a citizen you have never met, for one whole song. |
| I08 | Personal quest | Service | WITNESS | 2 | Ask the same official the same question three times. Notice what ch... |
| I09 | Personal quest | Breath | TOGETHER | 1 | Whisper a life-improving eco tip into the ear of 5 citizens. |
| I10 | Personal quest | Flow | WITNESS | 1 | Guard the door of the premium toilet for 5 minutes. Only elite citi... |
| I11 | Personal quest | Radiance | TOGETHER | 1 | Get 3 citizens to give you a 10-second hug. Body heat is renewable ... |
| I12 | Personal quest | Radiance | WITNESS | 1 | Compliment 3 different plants out loud, with a big smile, in front ... |
| I13 | Personal quest | Flow | REPORT | 1 | Ask 5 citizens: "Who decides how many credits you get?" Remember th... |
| I14 | Personal quest | Breath | TOGETHER | 1 | Write a secret word on a citizen's back with your finger. They get ... |
| I15 | Personal quest | Flow | TOGETHER | 2 | Make up the story of how Ecotopia began and tell it to 3 citizens. ... |
| I16 | Personal quest | Joy | TOGETHER | 2 | Find a citizen who doubts Ecotopia. Gently convince them until they... |
| I17 | Personal quest | Light | TOGETHER | 1 | Find a citizen wearing something more than 10 years old. Ask for it... |
| I18 | Personal quest | Radiance | TOGETHER | 1 | Ask a citizen who in the room they find radiant. Fly to that person... |
| I19 | Personal quest | Industry | TOGETHER | 2 | Tie 4 citizens into a human knot: everyone holds two different hand... |
| I20 | Personal quest | Humus | REPORT | 2 | Find the R.E.I.G.N. resource monitor. |
| I21 | Personal quest | Breath | TOGETHER | 2 | Start a chant praising R.E.I.G.N. that spreads to 3 different minis... |
| I22 | Personal quest | Vigilance | REPORT | 1 per report, max 2 | Listen for citizens complaining about credits, the rules or R.E.I.G... |
| I23 | Personal quest | Breath | TOGETHER | 1 | Breathe in sync with a citizen for 30 seconds while holding eye con... |
| I24 | Personal quest | Joy | TOGETHER | 1 | Get a group from another ministry to serenade you for 20 seconds. |
| I25 | Personal quest | Industry | TOGETHER | 2 | Give a 30-second shoulder massage to a citizen who is massaging som... |
| I26 | Personal quest | Vigilance | WITNESS | 1 | Look into a camera and say slowly: "Hello. I am a human." Film it. |
| I27 | Personal quest | Light | TOGETHER | 1 | Lead a ceremonial sacrifice of a small object, with 3 citizens from... |
| I28 | Personal quest | Service | TOGETHER | 1 | Escort a citizen of high carbon standing to the premium toilet and ... |
| I29 | Personal quest | Purity | TOGETHER | 2 | Kiss someone for exactly 10 seconds while a witness counts out loud... |
| I30 | Personal quest | Service | TOGETHER | 2 | Learn the names of 5 citizens from 5 different ministries. Recite t... |
| I31 | Personal quest | Humus | REPORT | 3 | Find 3 different R.E.I.G.N. data centres and read what each one say... |
| I32 | Personal quest | Purity | TOGETHER | 1 | Whisper your most unsustainable desire to a citizen. They whisper t... |
| I33 | Personal quest | Joy | TOGETHER | 3 | Get 3 strangers from different ministries to act out a 30-second pl... |
| I34 | Personal quest | Vigilance | TOGETHER | 2 | Get 5 citizens to swear out loud: "I trust R.E.I.G.N. and will repo... |
| I35 | Personal quest | Light | TOGETHER | 1 | Swap one item of clothing with a citizen you just met, for 10 minut... |
| I36 | Personal quest | Flow | TOGETHER | 1 | Ask a citizen about the last time they were really out in nature. R... |
| I37 | Personal quest | Service | WITNESS | 1 | Check the ribbons of 5 citizens waiting for the premium toilet. Pol... |
| I38 | Personal quest | Industry | TOGETHER | 1 | Offer yourself as the devoted servant of a citizen with a higher ri... |
| I39 | Personal quest | Humus | REPORT | 2 | Visit the recycling plant and find a citizen who has been renewed. ... |
| I40 | Personal quest | Radiance | TOGETHER | 1 | Make a toast with 3 strangers to something small you are grateful f... |
| I41 | Personal quest | Joy | TOGETHER | 1 | Teach your ministry's secret handshake to a citizen from another mi... |
| I42 | Personal quest | Vigilance | REPORT | 2 | Spot a citizen laughing at an announcement, humming an old song or ... |
| I43 | Personal quest | Purity | TOGETHER | 1 | Feed a small snack to a citizen from another ministry, and let them... |
| I44 | Personal quest | Light | TOGETHER | 1 | Carry a citizen piggyback across a room, with their yes. Never on t... |
| I45 | Personal quest | Service | REPORT | 2 | Ask 3 different officials: "Have you ever met R.E.I.G.N.?" Remember... |
| I46 | Personal quest | Light | TOGETHER | 1 | Wear something the wrong way (a scarf as a belt, a sock as a glove)... |
| I47 | Personal quest | Humus | TOGETHER | 1 | Write a short love poem to a plant or to R.E.I.G.N. and read it alo... |
| I48 | Personal quest | Vigilance | REPORT | 3 | Find the rebel hideout. Tell the police where it is. |
| I49 | Personal quest | Light | TOGETHER | 1 | Find a citizen born in the same month as you. Plant an imaginary tr... |
| I50 | Personal quest | Joy | TOGETHER | 2 | Get 3 citizens from 3 different ministries to perform a short dance... |
| M01 | Ministry quest | Joy | TOGETHER | 3 | Get 20 citizens from other ministries to say your ministry's slogan... |
| M02 | Ministry quest | Joy | TOGETHER | 2 | Organise a slogan battle with another ministry. The crowd picks the... |
| M03 | Ministry quest | Joy | TOGETHER | 2 | Have a dance battle against another ministry. |
| M04 | Ministry quest | Service | TOGETHER | 2 | Hold a 2-minute press conference: one minister takes questions from... |
| M05 | Ministry quest | Vigilance | REPORT | 3 | Rebel hunt: rebels are hiding somewhere in Ecotopia. Find their hid... |
| M06 | Ministry quest | Flow | WITNESS | 2 | Get the bar team, or any team at work, to sing a song together, smi... |
| M07 | Ministry quest | Radiance | WITNESS | 2 | Flicker the lights in a room three times, then cheerfully tell ever... |
| M08 | Ministry quest | Flow | WITNESS | 3 | Find the worst toilet in Ecotopia. Knock twice and ask: "Is there r... |
| M09 | Ministry quest | Light | WITNESS | 2 | Set up a two-minute swap shop and get citizens to swap hats, scarve... |
| M10 | Ministry quest | Industry | TOGETHER | 2 | Build the tallest tower you can from empty cups in 3 minutes. Anoth... |
| M11 | Ministry quest | Humus | TOGETHER | 2 | Write a ministry compost song and get another ministry to sing the ... |
| M12 | Ministry quest | Purity | TOGETHER | 2 | Take a group photo where everyone pretends to be a different vegeta... |
| M13 | Ministry quest | Breath | WITNESS | 2 | Start a silent flash mob: your whole ministry slowly grows from the... |
| M14 | Ministry quest | Industry | REPORT | 2 | Make a short clip about your ministry and send it to the organisers. |
| M15 | Ministry quest | Vigilance | WITNESS | 3 | Get 20 citizens to swear out loud: "We trust R.E.I.G.N. and will re... |
| M16 | Ministry quest | Humus | WITNESS | 2 | Make a photo series of your ministry in different poses about the b... |
| M17 | Ministry quest | Joy | WITNESS | 2 | Perform a one-minute play about how beautiful the future of Ecotopi... |
| M18 | Ministry quest | Light | WITNESS | 2 | Take your whole ministry to the garden. Each of you holds a plant a... |
| M19 | Ministry quest | Radiance | WITNESS | 2 | Choose your ministry's Citizen of the Hour and lead them like royal... |
| M20 | Ministry quest | Joy | TOGETHER | 2 | Hold a march in praise of something very small, like forgotten sock... |
| M21 | Ministry quest | Radiance | WITNESS | 3 | Throw a 2-minute welcome party for 5 citizens who came on their own... |
| M22 | Ministry quest | Breath | TOGETHER | 2 | Start a whisper chain with another ministry. The message must be an... |
| M23 | Ministry quest | Industry | WITNESS | 2 | Pollination drill: for one minute your whole ministry buzzes like b... |
| M24 | Ministry quest | Industry | WITNESS | 2 | Make a ministry flag or banner and hang it where everyone can see it. |
| M25 | Ministry quest | Vigilance | WITNESS | 2 | Announcement duty: post two members by the speakers during an annou... |
| M26 | Ministry quest | Service | TOGETHER | 2 | Sum up your ministry's policy in one sentence. Get 10 citizens from... |
| M27 | Ministry quest | Industry | REPORT | 2 | Build a small sustainability artifact from rubbish found in the hou... |
| M28 | Ministry quest | Humus | TOGETHER | 2 | Visit the recycling plant as a ministry. Ask the operators how citi... |
| M29 | Ministry quest | Service | REPORT | 2 | Write a new rule that makes everyone happier and hand it to the ann... |
| M30 | Ministry quest | Flow | TOGETHER | 3 | Ask 20 citizens: "What would you give up for the planet?" Present t... |
| R01 | Rival quest | Purity | WITNESS | 1 | Convince 3 members of your rival ministry that dry crackers are mor... |
| R02 | Rival quest | Vigilance | REPORT | 2 | Catch 2 members of your rival ministry saying something unsustainab... |
| R03 | Rival quest | Flow | WITNESS | 1 | Get your rival ministry to sing a song, smiling in sync, while they... |
| R04 | Rival quest | Light | WITNESS | 2 | Borrow one small item from 3 members of your rival ministry "for re... |
| R05 | Rival quest | Radiance | WITNESS | 1 | Flicker the lights where your rival ministry is gathering, then tha... |
| R06 | Rival quest | Breath | WITNESS | 1 | Hand 3 members of your rival ministry a playful fine for a made-up ... |
| R07 | Rival quest | Service | WITNESS | 2 | Keep a member of your rival ministry busy for 3 minutes by asking t... |
| R08 | Rival quest | Purity | WITNESS | 1 | Inspect 3 members of your rival ministry for plastic or fake leathe... |
| R09 | Rival quest | Humus | WITNESS | 2 | Convince a member of your rival ministry to wear your ministry's co... |
| R10 | Rival quest | Joy | WITNESS | 2 | Teach your rival ministry to chant your slogan at the next announce... |
| R11 | Rival quest | Radiance | WITNESS | 1 | Pay 5 members of your rival ministry a compliment each. They must a... |
| R12 | Rival quest | Joy | WITNESS | 1 | Announce loudly, in front of 5 citizens, why your ministry is bette... |
| C01 | Collaboration quest | Industry | TOGETHER | 2 each | Build the tallest tower from empty cups together with your collabor... |
| C02 | Collaboration quest | Flow | TOGETHER | 2 each | Perform a joint song of 30 seconds for the crowd. |
| C03 | Collaboration quest | Service | TOGETHER | 1 each | Swap secret handshakes: every member learns the other ministry's ha... |
| C04 | Collaboration quest | Purity | TOGETHER | 2 each | Hold a 30-second wedding between your two ministries, with vows to ... |
| C05 | Collaboration quest | Radiance | TOGETHER | 1 each | Take a group photo where both ministries together act out one scene... |
| C06 | Collaboration quest | Light | TOGETHER | 1 each | Swap one member each for 10 minutes and let them teach their new mi... |
| C07 | Collaboration quest | Industry | TOGETHER | 2 each | Invent one joint slogan that combines both ministries and teach it ... |
| C08 | Collaboration quest | Breath | TOGETHER | 2 each | Do a joint silent flash mob where both ministries slowly grow from ... |
| RB01 | Rebel quest | Resistance | WITNESS | 2 | Swap a rule poster in a hallway for a protest sign of your own, wit... |
| RB02 | Rebel quest | Resistance | WITNESS | 1 | Get an official to admit they have never met R.E.I.G.N. |
| RB03 | Rebel quest | Resistance | WITNESS | 2 | Find the folder marked HUMUS_DELETIONS at the recycling plant and b... |
| RB04 | Rebel quest | Resistance | WITNESS | 2 | Return a confiscated item to its owner after the police have taken ... |
| RB05 | Rebel quest | Resistance | WITNESS | 1 | Make a protest sign with a one-line message of your own, like "I am... |
| RB06 | Rebel quest | Resistance | WITNESS | 2 | Tear out your debt page and rip it to pieces at the rebel bar, in f... |
| RB07 | Rebel quest | Resistance | WITNESS | 2 | Quietly bring one trustworthy citizen to the rebel bar. |
| RB08 | Rebel quest | Resistance | WITNESS | 1 | Get 5 citizens to say "I am a human" into a camera, one at a time. |
| RB09 | Rebel quest | Resistance | WITNESS | 1 | Pin something you found on the What We Know wall, under the right q... |
| RB10 | Rebel quest | Resistance | WITNESS | 1 | Decode the message on the cipher card and ask it, out loud, to an o... |
| RB11 | Rebel quest | Resistance | WITNESS | 3 | Find all 7 data centres. Pin what each one says on the What We Know... |
| H0 | Secret role | Resistance | - | Still free at 23:00? 3 | You are THE HACKER. You stole a file from R.E.I.G.N. Keep this card... |
| S0 | Secret role | Resistance | - | Item never found? 2 | You are THE SMUGGLER. Hide one forbidden item on you: a plastic str... |
| H1 | Chain | Vigilance | REPORT | 2 | A hacker hides among us. Ask citizens "Are you the hacker?" until o... |
| H2 | Chain | Service | TOGETHER | 2 | Escort the captured hacker to the Interrogation station. Ask three ... |
| H3 | Chain | Radiance | REPORT | 2 | Bring the hacker to Carbon Confessions to be corrected. Make sure t... |
| H4 | Chain | Humus | WITNESS | 3 | Walk the corrected hacker to the recycling plant and witness their ... |
| D1 | Chain | Humus | REPORT | 2 | Find a R.E.I.G.N. data centre. Memorise its message word for word a... |
| D2 | Chain | Vigilance | TOGETHER | 2 | Decode the data centre message together with a citizen of Vigilance... |
| D3 | Chain | Service | REPORT | 3 | Turn the decoded message into a cheerful official announcement. Del... |
| S1 | Chain | Light | REPORT | 2 | A smuggler carries a forbidden item. Inspect citizens, with a yes, ... |
| S2 | Chain | Humus | TOGETHER | 2 | Take the confiscated item and its owner to the recycling plant. Hav... |
| S3 | Chain | Joy | WITNESS | 2 | Return the processed item to the smuggler with a celebration loud e... |
