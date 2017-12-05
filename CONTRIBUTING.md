Looking to contribute? Please read this first!

### RE: Set Definitions

OCTGN game plugins include the data for all the game's cards, organized within Set Definition files.  In the case of MTG, I have developed a tool which extracts card data from www.scryfall.com (an online MTG card database with a json API), and compiles them into OCTGN's XML set definition format.  The tool will update existing sets (if there's oracle text changes, for example), or generate new sets.

What does this mean for you?  With this current setup, only set data generated via the extractor tool will be committed to the repository.  **Pull requests including new sets or changes to sets will NOT be merged.** The tool saves a lot of time that would otherwise be spent manually typing out these sets, which is zero fun for everyone involved.  If a set is missing for a long period of time, please open up an issue ticket as a reminder to get it included.

Technical bits: The GUIDs assigned to cards are stored in an online database.  The extractor tool will query this database in order to determine a card's GUID value whenever it generates a set file.  This is important as OCTGN indexes cards into its local database via its GUID (whether its for installed images, loading deck files, or networking card data between users in games).  If a GUID changes, for example if a user-submitted set has different card GUIDs from a set generated through the extractor tool, then it will break existing decks or image packs that include that card.  We need to ensure that card GUIDs never change.
