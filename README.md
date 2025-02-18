# PokerBots

## Alexander Nichols, 2025

All code is my own / created using open source materials

### TODO

Shuffling - Fisher Yates shuffle w/ hardware random number generators see if I can make this open source without issues. Will need to document, but I'll make it open source. I would also have a discard pile, and then we can dynamically shuffle the remaining cards in the deck on top of the discard, further randomizing the shuffle

Stack - Python & Bash for backend, will have API endpoints to connect (could expect json data?). Maybe onnx/pickle for models (likely pickle). I'll obviously need to specify input / outputs, for a variety of different languages that I would have to choose.

    Accepted languages - Python, C++, C, Java, Scala? 

Classes 

    Deck - List of Cards, Actions (flop, river, burn, etc.), shuffle

    Game - Holds Deck, Pot, Players, order, etc.

    Players - hosting ai model, send/receive information about game(s). Active games, turn counts, etc.

    Testing - test deck randomness, basically everything else

    Logging - where our logging data is. Maybe display as well, maybe thats a different class

Logs - Obviously, all actions of the game will be logged and returned to the human player for viewing. I think I'd want to offer this live, though obviously summaries will be sent. Later would could include visualization tools (possibly a premium service?) where people can see the results of their model and analyze it all statistically (for iterating, training, whatever). Maybe downloading a csv of it could be a premium thing as well. Could provide deck order as well, post shuffle, assuming that doesn't allow for reverse engineering

Network - could I just receive the onnx/pickle of the model, host it locally, and send it back? I'm worried about players worrying about transparency / integrity of the game. Would providing the logs be sufficient security in that sense?

UX - Maybe later on we have accounts with people who can host different bots etc. I don't want to keep hold of their cash in an account, for security purposes. I'd rather people just add money as they play, and gets withdrawn after their bot stops playing the game. They would add their money for the game, and withdraw at the end (whether they won money off their opponent's bot or lost money). Something else is that in the instane of a larger player base, we'd obviously have varied stakes, and the opportunity to choose a table to join (which would provide information about which player is at the table at what seat. MAYBE - providing name of bot person is using)

Help - Obviously, have the necessary gambling hotline and resources and all that. Will also include regulation standards, just in case. Also will include documentation and how to, obviously. Will include input / output directions, pickle directions, how things work, etc. Later on, when having an actual UI, will put this stuff in the UI and all that

Monetization - While not an immediate concern, would be nice to think about. Premium log analysis will be nice, though obviously since my audience is coders they might be able to do it themselves. My pitch would be nice UI, which unfortunately is my weakness, but I'll be able to figure it out. Downloading a CSV of the logs might be a good one too, but it would be difficult to enforce considering people could add logging into their model (counterargument - state not saved after games (i.e. if the machine learned something), so if it saved logs it won't be returned with the game / model? But they could set up something to email (unless I can block that, obv). The core service, hosting bots and games, I want to be free. Ads would also be something I could do later on. Also hosting their pickles & maintaining stats across states? That could be a service. I don't want to change the price of these services based on how much money the player puts it, and I'd want the price to be low and accessible. I'd also want a dynamic family plan (something like $20 monthly for one person, $17.50 for two, $15 for three, $12.50 for four, and $10 for each subsequent person up to some number like 8) to encourage bringing more friends to the site. I would include options like if people would want to share their model pickle / model statistics with people on their plan, and have a toggle on/off thing. This would be a later account thing though. Something good would be to offer paid table setting creation, like if someone wants to host a game a paid service could be creating a table with settings (blinds, time to decide, max turns, etc.)
Size - Ideally I host as little information as possible. Hopefully, all I need on my end (and in the instance of this becoming big, smaller cloud hosting services) is the games + associated model pickles, as well as any of the visualization software and logs etc. I don't want to store money, bots (outside of their pickle connected to their account)

Security - How to ensure pickled model isn't running malicious code, whether it's to hack my system or try to hack the game. Would running in a container remove this risk? Would open-sourcing this part too also be good? It isn't something I'm good at either so would require further research

Game - 10 seconds for a model decision? Is that too much? Ideally, when choosing a game, we will have a hook to automate leaving (like a person can code if we've won/lost some amount to leave, or play a certain number of hands, etc. Should have a maximum 1000 turns played. Would also need to enforce rules (i.e. pot limit? min bet? etc) What happens when the bots try to do something not allowed? Auto check/fold?
