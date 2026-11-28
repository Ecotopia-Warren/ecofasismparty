# Quest card changes (2026-11-28)

Goal: every card says clearly WHAT to do, WHEN it is done, and HOW it is verified.
Regenerate: `python3 passport_v2/make_quest_cards.py`, then `cd passport_v2 && python3 make_quest_doc.py`.

## What changed on every card

- **New text source:** `passport_v2/quest_texts.py` (`TEXT`) overrides column B of the xlsx "quests to print" tab, so the xlsx stays read-only and untouched. `load()` warns about any quest ID without an override. Chain texts were edited in `chains.py`.
- **Quest text:** starts with an imperative action, then "Done when ..." (count, duration or end state), then special proof where it isn't the reg. no. (photo, clip, recital). Recipients named in the text now match the mode line: "the police", "a host" and "the Ministry of X" became "a Vigilance / Industry / X citizen". Consent lines ("Ask first", "with a yes", "They may say no", "Agree the limits first") are all kept; some were added (I05, I07, I25, R08).
- **Front mode line**, which replaces the small italic TOGETHER / REPORT / WITNESS sentence:
  - TOGETHER: `DO IT WITH: a Breath citizen` (ministry quests: `the Ministry of Joy`; collaboration quests: `the Ministry of Industry (your collaborator)`)
  - REPORT: `BRING IT TO: a Vigilance citizen`
  - WITNESS: `SHOW IT TO: a Service citizen (they watch you do it)`; rebel cards: `a fellow rebel`
  - Chain cards keep "Next step: at the gate." / "Captives may say no." as a small line under it.
- **How-to strip** on every front except the role cards: `1 Do it -> 2 get their reg. no. -> 3 hand in at the gate`. This replaces "Hand in this card for your stamps."
- **Back:** `Completed by: your reg. no.`, then `DONE WITH / BROUGHT TO / SHOWN TO a X citizen:` + `Write their reg. no. here ___` + "Numbers only, no names." This replaces the "Taking part / Received by / Witness" lines and the rule sentence. Role card backs are unchanged.
- **Fit:** checked in print mode with Playwright on all 123 fronts and 123 backs. There is no overflow or clipping, every how-to strip fits on one line, and every mode line fits within 2 lines. I also checked PNGs of front pages 2, 5, 9, 13 and 14 and back page 11 by eye.

## Cryptex-linked wording (kept on purpose, do not change)

The cryptex riddles depend on these facts, which are still printed:
- **H0** (role card, text unchanged): still free at **23:00**; deny it **twice**, confess the **third** time.
- **H1:** note "A hacker may deny it **twice**. The third time, they must confess." (unchanged). Text: done when you bring the hacker to a Vigilance citizen.
- **H2:** "Ask **THREE** questions about the stolen file" at the **Interrogation** station (capitals added, fact unchanged).
- **H3** (Radiance): bring the hacker to **Carbon Confessions**; note "Carbon Confessions is in the **Kinderkamer**." (unchanged).
- **H4** (Humus, witness): the hacker is renewed at the **recycling plant**.

No passport text was touched (page 4 underlined digits, page 8 "19.12").

## Card texts, old -> new (111 of 123 rewritten)

Unchanged: I29, I37, I43, I44, M21, R04, C04, RB01, RB06, RB09, H0, S0.

| ID | Old | New |
|---|---|---|
| I01 | Boop the nose of 5 citizens. Ask first. | Boop the nose of 5 citizens. Ask first. Done at nose number 5. |
| I02 | Kiss 3 citizens on the cheek. Ask first, and leave the credits out of it. | Kiss 3 citizens on the cheek. Ask first, and leave the credits out of it. Done at kiss number 3. |
| I03 | Find one of R.E.I.G.N.'s data centres, hidden somewhere in the house. Take a photo of its label. | Find one of R.E.I.G.N.'s hidden data centres. Photograph its label. Done when a Humus citizen has seen the photo. |
| I04 | Find your carbon twin: a citizen whose starting debt is within 50 credits of yours. Celebrate together, loudly. | Find your carbon twin: a citizen whose starting debt is within 50 credits of yours. Compare passports, then celebrate together, loudly. |
| I05 | There are rebels among us. Find one and report them to the police. | Find one of the rebels hiding among us. Bring them to a Vigilance citizen. They may say no. |
| I06 | Introduce two citizens who have never met. Stay until they find one thing they have in common. | Introduce two citizens who have never met. Done when they find one thing they have in common. |
| I07 | Slow dance with a citizen you have never met, for one whole song. | Slow dance with a citizen you have never met. Ask first. Done when the song ends. |
| I08 | Ask the same official the same question three times. Notice what changes, and what does not. | Ask one official the same question three times. Done after the third answer: tell your witness what changed, and what did not. |
| I09 | Whisper a life-improving eco tip into the ear of 5 citizens. | Whisper a life-improving eco tip into the ears of 5 citizens. Done at ear number 5. |
| I10 | Guard the door of the premium toilet for 5 minutes. Only elite citizens may enter: check each ribbon and let the toilet host decide who counts as elite. Never block anyone in a hurry. | Guard the door of the premium toilet for 5 minutes. Check each ribbon: only elite citizens may enter. |
| I11 | Get 3 citizens to give you a 10-second hug. Body heat is renewable energy. | Get 3 citizens to give you a 10-second hug, counted out loud. Body heat is renewable energy. Done at hug number 3. |
| I12 | Compliment 3 different plants out loud, with a big smile, in front of other citizens. | Compliment 3 different plants out loud, with a big smile, where other citizens can hear. Done at plant number 3. |
| I13 | Ask 5 citizens: "Who decides how many credits you get?" Remember the strangest answer. | Ask 5 citizens: "Who decides how many credits you get?" Done when you tell the strangest answer to a Flow citizen. |
| I14 | Write a secret word on a citizen's back with your finger. They get three guesses. | Write a secret word on a citizen's back with your finger. They get three guesses. Done when they guess it or run out. |
| I15 | Make up the story of how Ecotopia began and tell it to 3 citizens. Each of them adds one sentence before you move on. | Make up how Ecotopia began. Tell it to 3 citizens; each adds one sentence. Done when the story has 3 new sentences. |
| I16 | Find a citizen who doubts Ecotopia. Gently convince them until they say "Ecotopia is perfect" out loud. | Find a citizen who doubts Ecotopia and gently convince them. Done when they say "Ecotopia is perfect" out loud. |
| I17 | Find a citizen wearing something more than 10 years old. Ask for its story, then tell that story to someone else. | Find a citizen wearing something more than 10 years old. Hear its story. Done when you retell it to someone else. |
| I18 | Ask a citizen who in the room they find radiant. Fly to that person like a bee and deliver an anonymous compliment from them. | Ask a citizen who in the room they find radiant. Fly there like a bee. Done when you deliver their anonymous compliment. |
| I19 | Tie 4 citizens into a human knot: everyone holds two different hands. Untangle without letting go. | Tie 4 citizens into a human knot: everyone holds two different hands. Done when you untangle without letting go. |
| I20 | Find the R.E.I.G.N. resource monitor. | Find the R.E.I.G.N. resource monitor hidden in the house. Do not move it. Done when a Humus citizen knows exactly where it is. |
| I21 | Start a chant praising R.E.I.G.N. that spreads to 3 different ministries. | Start a chant praising R.E.I.G.N. Done when citizens of 3 different ministries chant along. |
| I22 | Listen for citizens complaining about credits, the rules or R.E.I.G.N. Tell the police their ribbon colour, never their name. | Hear a citizen complain about credits, the rules or R.E.I.G.N.? Report it to a Vigilance citizen: ribbon colour only, never a name. |
| I23 | Breathe in sync with a citizen for 30 seconds while holding eye contact. Shared breath halves your emissions. | Breathe in sync with a citizen for 30 seconds, holding eye contact. Shared breath halves your emissions. |
| I24 | Get a group from another ministry to serenade you for 20 seconds. | Get a group of 3 or more citizens to serenade you. Done after 20 seconds of song. |
| I25 | Give a 30-second shoulder massage to a citizen who is massaging someone else. Build a chain of 5. | Build a shoulder-massage chain of 5 citizens, each massaging the next. Ask first. Done after 30 seconds. |
| I26 | Look into a camera and say slowly: "Hello. I am a human." Film it. | Film yourself on a phone, looking into the camera, saying slowly: "Hello. I am a human." Done when your witness has seen the clip. |
| I27 | Lead a ceremonial sacrifice of a small object, with 3 citizens from different ministries. Give the object back afterwards. | Lead a ceremonial sacrifice of a small object with 3 citizens from different ministries. Done when you give the object back. |
| I28 | Escort a citizen of high carbon standing to the premium toilet and announce them at the door like royalty. | Escort a citizen with a high ribbon to the premium toilet. Done when you announce them at the door like royalty. |
| I30 | Learn the names of 5 citizens from 5 different ministries. Recite them to the host when you claim. | Learn the names of 5 citizens from 5 different ministries. Done when you recite all 5 to the official at the gate, without notes. |
| I31 | Find 3 different R.E.I.G.N. data centres and read what each one says. Tell a citizen what R.E.I.G.N. needs. | Read the messages of 3 different R.E.I.G.N. data centres. Done when you tell a Humus citizen what R.E.I.G.N. needs. |
| I32 | Whisper your most unsustainable desire to a citizen. They whisper theirs back. | Whisper your most unsustainable desire to a citizen. Done when they whisper theirs back. |
| I33 | Get 3 strangers from different ministries to act out a 30-second play about life in Ecotopia. | Get 3 strangers from 3 different ministries to act out a 30-second play about life in Ecotopia. Done after the bow. |
| I34 | Get 5 citizens to swear out loud: "I trust R.E.I.G.N. and will report anything unusual." | Get 5 citizens to swear out loud: "I trust R.E.I.G.N. and will report anything unusual." Done at oath number 5. |
| I35 | Swap one item of clothing with a citizen you just met, for 10 minutes. | Swap one item of clothing with a citizen you just met. Done when you swap back after 10 minutes. |
| I36 | Ask a citizen about the last time they were really out in nature. Retell it to someone else as if it happened to you. | Ask a citizen about the last time they were really out in nature. Done when you retell it to someone else as if it happened to you. |
| I38 | Offer yourself as the devoted servant of a citizen with a higher ribbon than yours, for 5 minutes. Agree the limits first. | Be the devoted servant of a citizen with a higher ribbon than yours. Agree the limits first. Done after 5 minutes. |
| I39 | Visit the recycling plant and find a citizen who has been renewed. Ask them what they remember. | Find a renewed citizen at the recycling plant and ask what they remember. Done when you tell a Humus citizen. |
| I40 | Make a toast with 3 strangers to something small you are grateful for today. | Make a toast with 3 strangers to something small you are grateful for today. Done when the glasses clink. |
| I41 | Teach your ministry's secret handshake to a citizen from another ministry. No handshake yet? Invent one first. | Teach your ministry's secret handshake to a citizen of another ministry (none yet? invent one). Done when they do it alone. |
| I42 | Spot a citizen laughing at an announcement, humming an old song or talking to a plant. Thank them for their enthusiasm and walk them to an official for a happiness check. They may say no. | Spot a citizen laughing at an announcement, humming an old song or talking to a plant. Walk them to a Vigilance citizen for a happiness check. They may say no. |
| I45 | Ask 3 different officials: "Have you ever met R.E.I.G.N.?" Remember their answers. | Ask 3 different officials: "Have you ever met R.E.I.G.N.?" Done when you report their answers to a Service citizen. |
| I46 | Wear something the wrong way (a scarf as a belt, a sock as a glove). Declare it the new standard and get 3 citizens to comply. | Wear something the wrong way (a scarf as a belt, a sock as a glove). Declare it the new standard. Done when 3 citizens copy you. |
| I47 | Write a short love poem to a plant or to R.E.I.G.N. and read it aloud to a citizen. | Write a short love poem to a plant or to R.E.I.G.N. Done when you read it aloud to a citizen. |
| I48 | Find the rebel hideout. Tell the police where it is. | Find the rebel hideout. Done when a Vigilance citizen knows where it is. |
| I49 | Find a citizen born in the same month as you. Plant an imaginary tree together and give it a name. | Find a citizen born in the same month as you. Done when you have planted an imaginary tree together and named it. |
| I50 | Get 3 citizens from 3 different ministries to perform a short dance routine together. | Get 3 citizens from 3 different ministries to dance a routine together. Done after 20 seconds of dancing. |
| M01 | Get 20 citizens from other ministries to say your ministry's slogan out loud. | Get 20 citizens from other ministries to say your ministry's slogan out loud. Keep count. Done at citizen number 20. |
| M02 | Organise a slogan battle with another ministry. The crowd picks the winner. | Hold a slogan battle with another ministry. Done when the crowd picks a winner. Losing counts too. |
| M03 | Have a dance battle against another ministry. | Challenge another ministry to a dance battle: one song each. Done when the crowd picks a winner. Losing counts too. |
| M04 | Hold a 2-minute press conference: one minister takes questions from another ministry and may only answer in positive words. | Hold a 2-minute press conference: one minister takes questions from another ministry and answers only in positive words. |
| M05 | Rebel hunt: rebels are hiding somewhere in Ecotopia. Find their hideout as a ministry and bring the police to it. | Hunt for the rebel hideout as a ministry. Done when a Vigilance citizen knows where it is. |
| M06 | Get the bar team, or any team at work, to sing a song together, smiling in sync, while they work. | Get the bar team, or any team at work, to sing a song together, smiling in sync, while they work. Done after one chorus. |
| M07 | Flicker the lights in a room three times, then cheerfully tell everyone in it how much power they just saved. | Flicker the lights in a room three times. Done when you have cheerfully told everyone in it how much power they just saved. |
| M08 | Find the worst toilet in Ecotopia. Knock twice and ask: "Is there room for nature?" Go together as a ministry. | Go as a whole ministry to the worst toilet in Ecotopia. Knock twice and ask together: "Is there room for nature?" |
| M09 | Set up a two-minute swap shop and get citizens to swap hats, scarves or accessories on the spot. | Set up a two-minute swap shop. Done when 5 citizens have swapped hats, scarves or accessories on the spot. |
| M10 | Build the tallest tower you can from empty cups in 3 minutes. Another ministry judges. | Build the tallest tower you can from empty cups in 3 minutes. Done when another ministry has judged it. |
| M11 | Write a ministry compost song and get another ministry to sing the chorus. | Write a ministry compost song. Done when another ministry sings the chorus with you. |
| M12 | Take a group photo where everyone pretends to be a different vegetable. Another ministry guesses each one. | Take a group photo where everyone pretends to be a different vegetable. Done when another ministry has guessed each one. |
| M13 | Start a silent flash mob: your whole ministry slowly grows from the floor like a plant at the same moment. | Silent flash mob: at the same moment your whole ministry slowly grows from the floor like a plant. Done when all stand tall. |
| M14 | Make a short clip about your ministry and send it to the organisers. | Film a short clip (max 1 minute) about your ministry. Show it to an Industry citizen, then send it to the organisers. |
| M15 | Get 20 citizens to swear out loud: "We trust R.E.I.G.N. and will report anything unusual." | Get 20 citizens to swear out loud: "We trust R.E.I.G.N. and will report anything unusual." Keep count. Done at oath number 20. |
| M16 | Make a photo series of your ministry in different poses about the birth of Ecotopia. | Shoot a photo series of 5 poses of your ministry about the birth of Ecotopia. Done when your witness has seen all 5. |
| M17 | Perform a one-minute play about how beautiful the future of Ecotopia will be. | Perform a one-minute play about how beautiful the future of Ecotopia will be, for at least 5 watching citizens. |
| M18 | Take your whole ministry to the garden. Each of you holds a plant and stands in silence for one minute, for the old forest. | Take your whole ministry to the garden. Each holds a plant and stands in silence for one minute, for the old forest. |
| M19 | Choose your ministry's Citizen of the Hour and lead them like royalty in a procession through the ground floor. | Choose your ministry's Citizen of the Hour. Done when you have led them like royalty in a procession through the ground floor. |
| M20 | Hold a march in praise of something very small, like forgotten socks, and get another ministry to join. | March in praise of something very small, like forgotten socks. Done when another ministry has joined your march. |
| M22 | Start a whisper chain with another ministry. The message must be an eco slogan. Compare how it ended up. | Start a whisper chain of an eco slogan with another ministry. Done when you compare the first and last version out loud. |
| M23 | Pollination drill: for one minute your whole ministry buzzes like bees from citizen to citizen, landing on each just long enough to give a compliment. | Pollination drill: for one minute your whole ministry buzzes like bees from citizen to citizen, landing just long enough to give a compliment. |
| M24 | Make a ministry flag or banner and hang it where everyone can see it. | Make a ministry flag or banner. Done when it hangs where everyone can see it. |
| M25 | Announcement duty: post two members by the speakers during an announcement. Anyone who laughs or talks through it gets a polite happiness check from the police. | Announcement duty: post two members by the speakers during an announcement. Give anyone who laughs or talks a polite happiness check. |
| M26 | Sum up your ministry's policy in one sentence. Get 10 citizens from other ministries to repeat it back word for word. | Sum up your ministry's policy in one sentence. Done when 10 citizens from other ministries repeat it back word for word. |
| M27 | Build a small sustainability artifact from rubbish found in the house and present it to a host. | Build a small sustainability artifact from rubbish found in the house. Done when you present it to an Industry citizen. |
| M28 | Visit the recycling plant as a ministry. Ask the operators how citizens are renewed, then report back to another ministry, cheerfully. | Visit the recycling plant as a ministry and ask the operators how citizens are renewed. Done when you cheerfully tell another ministry. |
| M29 | Write a new rule that makes everyone happier and hand it to the announcement team. | Write down a new rule that makes everyone happier. Hand it to a Service citizen, who passes it to the announcement team. |
| M30 | Ask 20 citizens: "What would you give up for the planet?" Present the 3 funniest answers to another ministry. | Ask 20 citizens: "What would you give up for the planet?" Done when you present the 3 funniest answers to another ministry. |
| R01 | Convince 3 members of your rival ministry that dry crackers are more ecological than a glass of water. | Convince 3 members of your rival ministry that dry crackers are more ecological than a glass of water. Done at convert number 3. |
| R02 | Catch 2 members of your rival ministry saying something unsustainable and report them to the police. | Catch 2 members of your rival ministry saying something unsustainable. Done when you report both to a Vigilance citizen. |
| R03 | Get your rival ministry to sing a song, smiling in sync, while they tidy up their empty glasses. | Get your rival ministry to sing a song, smiling in sync, while they tidy up their empty glasses. Done after one chorus. |
| R05 | Flicker the lights where your rival ministry is gathering, then thank them loudly for saving so much power. | Flicker the lights where your rival ministry is gathering. Done when you have thanked them loudly for saving so much power. |
| R06 | Hand 3 members of your rival ministry a playful fine for a made-up eco crime, like "overconfident breathing". | Hand 3 members of your rival ministry a playful fine for a made-up eco crime, like "overconfident breathing". Done at fine number 3. |
| R07 | Keep a member of your rival ministry busy for 3 minutes by asking them to explain their ministry's policy in great detail. | Ask a member of your rival ministry to explain their ministry's policy in great detail. Done when you have kept them busy for 3 minutes. |
| R08 | Inspect 3 members of your rival ministry for plastic or fake leather and give each a polite warning. | Inspect 3 members of your rival ministry for plastic or fake leather, with a yes. Give each a polite warning. |
| R09 | Convince a member of your rival ministry to wear your ministry's colours (ribbon or sticker) for 10 minutes. | Convince a member of your rival ministry to wear your ministry's colours (ribbon or sticker). Done after 10 minutes. |
| R10 | Teach your rival ministry to chant your slogan at the next announcement. | Teach your rival ministry your slogan. Done when they chant it at the next announcement. |
| R11 | Pay 5 members of your rival ministry a compliment each. They must answer "Thank you, Minister." | Pay 5 members of your rival ministry a compliment each. They must answer "Thank you, Minister." Done at number 5. |
| R12 | Announce loudly, in front of 5 citizens, why your ministry is better than your rival. | Announce loudly, in front of 5 citizens, why your ministry is better than your rival ministry. |
| C01 | Build the tallest tower from empty cups together with your collaborator ministry in 3 minutes. | Build the tallest tower you can from empty cups together with your collaborator ministry. Done after 3 minutes. |
| C02 | Perform a joint song of 30 seconds for the crowd. | Perform a joint 30-second song with your collaborator ministry. Done when the crowd applauds. |
| C03 | Swap secret handshakes: every member learns the other ministry's handshake and shows it to a host. | Swap secret handshakes: every member learns the other ministry's handshake. Done when you all show it to an official. |
| C05 | Take a group photo where both ministries together act out one scene from the history of Ecotopia. | Take a group photo where both ministries together act out one scene from the history of Ecotopia. Show the photo. |
| C06 | Swap one member each for 10 minutes and let them teach their new ministry a sustainability hack. | Swap one member each for 10 minutes. Done when each guest has taught their new ministry a sustainability hack. |
| C07 | Invent one joint slogan that combines both ministries and teach it to 10 citizens. | Invent one joint slogan that combines both ministries. Done when 10 citizens can say it. |
| C08 | Do a joint silent flash mob where both ministries slowly grow from the floor at the same moment. | Joint silent flash mob: at the same moment both ministries slowly grow from the floor. Done when all stand tall. |
| RB02 | Get an official to admit they have never met R.E.I.G.N. | Get an official to admit, out loud, that they have never met R.E.I.G.N. |
| RB03 | Find the folder marked HUMUS_DELETIONS at the recycling plant and bring it to the rebel bar. | Find the folder marked HUMUS_DELETIONS at the recycling plant. Done when it is at the rebel bar. |
| RB04 | Return a confiscated item to its owner after the police have taken it, without being caught. | After the police take an item, return it to its owner without being caught. |
| RB05 | Make a protest sign with a one-line message of your own, like "I am a human" or "Nature first", and hold it up in front of 5 citizens. | Make a protest sign with a one-line message of your own, like "I am a human". Done when you hold it up in front of 5 citizens. |
| RB07 | Quietly bring one trustworthy citizen to the rebel bar. | Quietly bring one trustworthy citizen to the rebel bar. Done when a rebel welcomes them. |
| RB08 | Get 5 citizens to say "I am a human" into a camera, one at a time. | Get 5 citizens to say "I am a human" into a phone camera, one at a time. Done at citizen number 5. |
| RB10 | Decode the message on the cipher card and ask it, out loud, to an official. | Decode the message on the cipher card. Done when you have asked it, out loud, to an official. |
| RB11 | Find all 7 data centres. Pin what each one says on the What We Know wall. | Find all 7 data centres. Done when what each one says is pinned on the What We Know wall. |
| H1 | A hacker hides among us. Ask citizens "Are you the hacker?" until one confesses. Bring them to the Ministry of Vigilance. | A hacker hides among us. Ask citizens "Are you the hacker?" until one confesses. Done when you bring them to a Vigilance citizen. |
| H2 | Escort the captured hacker to the Interrogation station. Ask three questions about the stolen file. | Escort the captured hacker to the Interrogation station. Ask THREE questions about the stolen file. Done after the third answer. |
| H3 | Bring the hacker to Carbon Confessions to be corrected. Make sure they confess loudly, with a smile. | Bring the hacker to Carbon Confessions to be corrected. Done when they have confessed loudly, with a smile, to a Radiance citizen. |
| H4 | Walk the corrected hacker to the recycling plant and witness their renewal. | Walk the corrected hacker to the recycling plant. Done when they have been renewed, with your witness watching. |
| D1 | Find a R.E.I.G.N. data centre. Memorise its message word for word and recite it to the Ministry of Humus. | Find a R.E.I.G.N. data centre and memorise its message. Done when you recite it word for word to a Humus citizen. |
| D2 | Decode the data centre message together with a citizen of Vigilance. Agree on what R.E.I.G.N. is hiding. | Decode the data centre message together with a Vigilance citizen. Done when you agree on what R.E.I.G.N. is hiding. |
| D3 | Turn the decoded message into a cheerful official announcement. Deliver it to the Ministry of Service. | Turn the decoded message into a cheerful official announcement. Done when you deliver it to a Service citizen. |
| S1 | A smuggler carries a forbidden item. Inspect citizens, with a yes, until you find it. Bring the item and its owner to the Ministry of Light. | A smuggler carries a forbidden item. Inspect citizens, with a yes, until you find it. Done when you bring the item and its owner to a Light citizen. |
| S2 | Take the confiscated item and its owner to the recycling plant. Have the item processed, with ceremony. | Take the confiscated item and its owner to the recycling plant. Done when the item is processed, with ceremony. |
| S3 | Return the processed item to the smuggler with a celebration loud enough that 5 citizens join in. | Return the processed item to the smuggler with a celebration. Done when 5 citizens join in. |

## Extra instructions (notes), old -> new

| ID | Old | New |
|---|---|---|
| I20 | Tell the Ministry of Humus where it is, without moving it. | (removed: now in the quest text or the mode line) |
| I22 | Never give names. Ribbon colour only. | (removed: now in the quest text or the mode line) |
| I30 | The host = the official at the gate who stamps your card. | (removed: now in the quest text or the mode line) |
| C01 | Your collaborator ministry is the ministry on this card. | (removed: now in the quest text or the mode line) |
| C02 | Your collaborator ministry is the ministry on this card. | (removed: now in the quest text or the mode line) |
| C03 | Your collaborator ministry is the ministry on this card. | (removed: now in the quest text or the mode line) |
| C04 | Your collaborator ministry is the ministry on this card. | (removed: now in the quest text or the mode line) |
| C05 | Your collaborator ministry is the ministry on this card. | (removed: now in the quest text or the mode line) |
| C06 | Your collaborator ministry is the ministry on this card. | (removed: now in the quest text or the mode line) |
| C07 | Your collaborator ministry is the ministry on this card. | (removed: now in the quest text or the mode line) |
| C08 | Your collaborator ministry is the ministry on this card. | (removed: now in the quest text or the mode line) |

## Open (design decisions, not guessed)

- **Rival pairings:** R01-R12 still say "your rival ministry", which no card defines. The proposal in QUEST_SYSTEM.md (Purity-Flow, Vigilance-Joy, Industry-Humus, Light-Breath, Radiance-Service) is not printed. Do we announce it at the gate, or print it on the card?
- **I20 resource monitor:** what does it look like, and where is it? The card now says "hidden in the house", but players don't know what to look for.
- **RB10 cipher card:** where do players get the cipher card?
- **M14 clip:** how does a clip reach "the organisers" (an email, a phone number, a QR code)? The card now has the player show it to an Industry citizen first.
- **"Host" / "official":** I30 now says "the official at the gate", and C03 says "an official" (it used to say "a host"). Confirm that any official can verify.
- **Police vs Vigilance:** REPORT cards that mentioned the police (I05, I22, I48, M05, R02) now say "bring it to a Vigilance citizen", because the back needs a Vigilance reg. no. The notes on I48 and M05 still say Vigilance fetches the police. M25's happiness check is done by the ministry members themselves. Is that OK?
- **How-to strip size:** it prints at 5.6 pt, which is legible but small. If that's too small, drop the arrows or move the strip to the back.
