changelog = {
    3020300: ("3.2.3.0", "07 October 2013", [
        "Added a changelog dialog that displays when a game is started.",
        "Added a table submenu to separately enable/disable alignment, autoscripts, and attachment aligning.",
        "Attaching a card to another player's card will pass control of it to your opponent.",
        "Detached auras will trigger destroy scripts remotely for the player who controls the aura.",
        "Manually moving a card around the table will move all its attachments with it (while attachment aligning is enabled).",
        "Fixed the mana symbols showing up in the chat log.",
        "Added Theros Intro packs and Event deck.",
        "RTR's Izzet Ingenuity intro deck now contains the correct basic lands.",
        "Fixed Clear All (esc) not removing target arrows.",
        "Clear All (esc) will not remove the Does Not Untap highlight.",
        "Removed all manipulations of cards you don't control from alignment code (all done remotely now)."
        ]),
    3020400: ("3.2.4.0", "09 October 2013", [
        "Fixed a game-breaking bug involving the attachments script.",
        "Initial support for Monstrosity abilities.",
        "Added marker images for Monstrous, Morph and Choice autoscript indicators.",
        "Fixed activated model abilities asking to choose an ability twice.",
        "Fixed a bug where casting an aura with a target would align the aura behind the target, instead of on the stack."
        ]),
    3020500: ("3.2.5.0", "23 October 2013", [
        "Added 'Scry' Library action (CTRL+SHIFT+C), which lets you scry a specified number of cards on top of your library.",
        "Added a catch to prevent a few illegal attachment pairings.",
        "Bestow creatures will now auto-attach like auras if you target something while casting them.",
        "Behind the scenes changes to askChoice dialog windows, and the Stack alignment."
        ]),
    3020600: ("3.2.6.0", "30 October 2013", [
        "Added Commander 2013 cards and decks."
        ]),
    3020700: ("3.2.7.0", "11 December 2013", [
        "Alignment no longer breaks when a player leaves the game.",
        "Cards entering the battlefield won't zoom out the tale.",
        "Fixed a python error when you cancel out of the scry window.",
        "Fixed ampersands showing up in the mana costs of some cards."
        ]),
    3020800: ("3.2.8.0", "12 December 2013", [
        "Fixed a bug where this changelog window kept popping up.",
        "Favorite Token artworks will now be saved properly.",
        "Attack, block, exile, activate, tap/untap process faster when performed on a selection of cards.",
        "Fixed some bugs with the alignment and autoscript toggles."
        ]),
    3020900: ("3.2.9.0", "17 December 2013", [
        "Added Theros Prerelease Packs to the sealed deck editor.",
        "Added a debug option in the 'Autoscript Settings' menu. It will be used to debug lag times in the game.",
        "Manually moving a card on the table will anchor it to the table, blocking it from alignment.",
        "Added 'Align Card' action for cards on the table.  Using this on an anchored card will remove the anchor and align the card.",
        "Using the 'Re-Align Cards' table action now removes the anchors on all cards, forcing them to align."
        ]),
    3021000: ("3.2.10.0", "20 January  2014", [
        "Added an Autoscript Setting to toggle Alignment Anchoring.",
        "-> Enabled: Manually dragging a card will anchor it.  Card alignment will ignore it.",
        "-> Disabled: Manually dragging a card will allow you to rearrange the order of your cards with alignment.",
        "Added more data to the debug option.",
        "Added 'Pass Priority' (F6) toggle function which will automatically pass your priority if you have Autoscripts enabled.",
        "Added some missing tokens from the Commander sets.",
        "Fixed Xenagos's Token and the corruped 10th Edition intro decks."
        ]),
    3021100: ("3.2.11.0", "28 January 2014", [
        "Added Born of the Gods cards and tokens.",
        "Updated the Help document for some newer functions.",
        "Added 'View Update Log' action for the table, to view all previous changelog windows."
        ]),
    3021200: ("3.2.12.0", "05 May 2014", [
        "Added Duel Decks Jace vs Vraska cards & Preconstructed Decks.",
        "Added Journey into Nyx cards, Tokens, Preconstructed Decks.",
        "Added Born of the Gods and Journey Into Nyx Prerelease Seeded Booster Packs."
        ]),
    3021202: ("3.2.12.2", "22 May 2014", [
        "Quick Matchmaking update, multiple formats are now available for matchmaking."
        ]),
    3021300: ("3.2.13.0", "06 June 2014", [
        "Added Conspiracy+tokens, and Modern Event Deck 2014."
        ]),
    3021400: ("3.2.14.0", "08 July 2014", [
        "Added M15+Tokens, and Vintage Masters.",
        "Added M15 Clash Pack deck files, found in the Event Decks folder"
        ]),
    3021501: ("3.2.15.1", "16 September 2014", [
        "Added Khans of Tarkir+Tokens.",
        "Updated the card database for the most recent Oracle text.",
        "Added the Challenge Decks and Hero supplemental cards from Theros Block.",
        "Updated the pre-con decks (Khans decks not yet available).",
        "Fixed a bug where peeked Morph cards (facedown) will align with their face-up equivalents, revealing the card identity to other players.",
        "Updated script recognition of the new Modal card template.",
        "Casting a card face-down (Morphing it) will auto-peek it for you."
        ]),
    3021600: ("3.2.16.0", "18 September 2014", [
        "Updated Khans of Tarkir to the Gatherer text.",
        "Khans and Ravnica watermarks now show on proxy images.",
        "Added Speed vs Cunning and FTV Annihilation.",
        "Fixed a bug stopping morph triggers from triggering."
        ]),
    3021602: ("3.2.16.2", "05 November 2014", [
        "Added Commander 2014 set and tokens."
        ]),
    3021700: ("3.2.17.0", "13 January 2015", [
        "Added Fate Reforged cards and tokens.",
        "Added Khans of Tarkir Seeded Boosters (You'll need to add both the Booster and the Promo pack to generate a complete Seeded booster pack.)",
        "Fixed a bug preventing Planeswalkers and other cards activated abilities from working."
        ]),
    3021800: ("3.2.18.0", "30 January 2015", [
        "Random discard function now properly notifies the card name.",
        "Fixed a bug where auras randomly move to the graveyard from your hand or deck after you scoop the game.",
        "Planes and Scheme cards are now larger in size.",
        "Added the previously unavailable promo Planes and Schemes.",
        "NOTE: A new image pack is available for the larger card images, which is required for them to appear normally in the game"
        ]),
    3021900: ("3.2.19.0", "17 March 2015", [
        "Added Dragons of Tarkir + Tokens.",
        "Added Duel Decks Elspeth vs Kiora + precon decks.",
        "Added support for modal cards that allow more than one choice (commands, entwine, etc).",
        "Added Manifest mechanic, you can manifest cards from piles or the table via right-click menu.",
        "Resolving Tribute cards (fanatic of xenagos) will prompt your opponent to pay tribute, their choice appears in chat window.",
        "The Outpost cycle (from fate reforged) will allow you to place dragon or khans markers on them.",
        "Fixed an error with Auto-Create Token."
        ]),
    3022000: ("3.2.20.0", "07 July 2015", [
        "Added Magic Origins, Modern Masters 2015, Masters Edition IV",
        "Fixed an issue with the stack not aligning properly",
        "Improved the scry mechanic to display card images",
        "Proxy texts are easier to read"
        ]),
    3022100: ("3.2.21.0", "30 August 2015", [
        "Added Tempest Remastered, FTV Angels, Zendikar vs Eldrazi",
        "Added a bunch of missing precon decks.",
        "Fixed some bugs where the autoscripts tried to add a marker that wasnt defined.",
        "Fixed a minor error message with the end-turn function."
        ]),
    3022101: ("3.2.21.1", "September 21 2015", [
        "Added Pre-release version of Battle for Zendikar"
        ]),
    3022103: ("3.2.21.3", "November 17 2015", [
        "Added Commander 2015"
        ]),
    3030000: ("3.3.0.0", "January 13 2016", [
        "Welcome to version 3.3.0!!",
        "Added Oath of the Gatewatch + Tokens",
        "Mana symbols are now searchable by their {X} notation",
        "Added colorless mana symbol {C}",
        "Updated text on all sets",
        "Enhanced scry window to new split-dialog window",
        "Upgraded all python scripts to 3.1.0.2 API version",
        "Fixed bug with creating multiple tokens",
        "Cloning a token will copy the artwork"
        ]),
    3030001: ("3.3.0.1", "February 9 2016", [
        "Fixed a bug with scry window not reporting when cancelled."
        ]),
    3030100: ("3.3.1.0", "March 29 2016", [
        "Added Shadows over Innistrad and Blessed vs Cursed."
        ]),
    3030103: ("3.3.1.3", "June 8 2016", [
        "Added Eternal Masters."
        ]),
    3030200: ("3.3.2.0", "June 21 2016", [
        "Madness now works properly.",
        "",
        "Substantial rewrite of autoscript engine. Hopefully everything still works, there shouldn't be any noticeable changes for players.",
        "Please report any errors or unusual gameplay behaviour to OCTGN chat (ping brine) or the issue tracker at http://www.github.com/brine/mtg-octgn/issues"
        ]),
    3030300: ("3.3.3.0", "July 13 2016", [
        "Eldritch Moon is now available."
        ]),
    3030400: ("3.3.4.0", "August 25 2016", [
        "Conspiracy 2 and FTV Lore added."
        ]),
    3030402: ("3.3.4.2", "September 6 2016", [
        "Fixed a bug with buyback cards."
        ]),
    3030500: ("3.3.5.0", "September 21 2016", [
        "Kaladesh added."
        ]),
    3030502: ("3.3.5.2", "September 22 2016", [
        "Changed all instances of the AE symbol to Ae.",
        "Updated player counters to include new colorless symbol, energy, and experience.",
        "Some back-end autoscript updates and minor bug fixes.",
        "Autoscripts can adjust player counters other than life now."
        ]),
    3030503: ("3.3.5.3", "October 13 2016", [
        "Added the Phase bar to the game interface.",
        "Fixed a bug with exile scripts breaking."
        ]),
    3030600: ("3.3.6.0", "November 9 2016", [
        "Added Commander 2016."
        ]),
    3030700: ("3.3.7.0", "January 10 2017", [
        "Added Aether Revolt."
        ]),
    3030702: ("3.3.7.2", "March 7 2017", [
        "Added Modern Masters 2017."
        ]),
    3030800: ("3.3.8.0", "April 19 2017", [
        "Added Amonkhet, Nissa vs Ob Nixilis, Mind vs Might.",
        "Added support for 'does not untap on next untap step', AKA the Exert keyword.  Older card scripts will eventually be updated to support this.",
        "CTRL+V shortcut is now for Exert (originally the permanent does-not-untap toggle).",
        "CTRL+SHIFT+V shortcut is now Keep Tapped During All Untap Steps (the old CTRL+V functionality, renamed).",
        "New Table group action (CTRL+U) to untap all your permanents, doesn't change the active phase.",
        "Added scripting support for activated abilities in graveyards (including Embalm).",
        "BUG FIX: clicking the untap phase would untap your opponents cards.",
        "BUG FIX: Attacking while tapped wouldn't trigger attack scripting (bypass dialog didn't work).",
        "KNOWN BUG: Split cards (including aftermath) aren't working properly, will fix in the next update."
        ]),
    3030801: ("3.3.8.1", "April 19 2017", [
        "Split cards are working again."
        ]),
    3030900: ("3.3.9.0", "July 5 2017", [
        "Added Hour of Devastation."
        ]),
    3031000: ("3.3.10.0", "August 16 2017", [
        "Added Commander 2017, Archenemy Nicol Bolas, Masters Edition IV."
        ]),
    3040000: ("3.4.0.0", "September 18 2017", [
        "Added rich text formatting for mana costs and rules text in deck editor, providing full color mana symbols.",
        "Added a Deck Editor Plugin which downloads and installs card images.  No more image packs needed!",
        "Added Ixalan and Iconic Masters.",
        "Fixed some bugs relating to activated ability scripting.",
        "Passing priority hotkey will always announce even if you've already passed priority.",
        "Changing phases will reset the priority tracker.",
        "Added a 'Move All Cards To' submenus in all groups, with more destination groups available."
        ]),
    3040001: ("3.4.0.1", "September 20 2017", [
        "White corners on card images shouldn't appear in the game table.",
        "Fixed issues with image downloader fetching some wrong token arts and not rotating plane cards.",
        "Please re-download the Tokens, Planechase, and Planechase 2012 images from the plugin to correct this error."
        ]),
    3040003: ("3.4.0.3", "November 9 2017", [
        "Fixed many serious errors with the image downloader plugin.",
        "Added ability to download images from all sets at once",
        "Temporarily disabled Theros Challenge Decks and Unique Promotional Cards sets"
        ]),
    3040100: ("3.4.1.0", "December 6 2017", [
        "Added Unstable, Duel Deck Merfolk vs Goblins, FTV Transform."
        ]),
    3040200: ("3.4.2.0", "December 12 2017", [
        "Fixed issues with Unstable text extraction and booster generator (how do you give high fives or throw Slaying Mantis cards on OCTGN?).",
        "Oracle text update to all sets (legendary planeswalker, dinosaurs, and wording updates).",
        "Card color no longer defaults to colorless for cards that have a color indicator.",
        "Fixed major bugs with the image downloader plugin.",
        "Added new option in image downloader plugin to skip downloading new versions of images if a hi-res version is already installed."
        ]),
    3040300: ("3.4.3.0", "January 6 2018", [
        "Added Rivals of Ixalan",
        "Added a dialog window to image downloader plugin when an image file download errors out."
        ]),
    3040400: ("3.4.4.0", "January 23 2018", [
        "Minor Text Fixes to Ixalan Block sets and recent supplemental releases",
        "Fixed some issues with Ixalan booster packs not generating accurately and including Planeswalker deck cards."
        ]),
    3040500: ("3.4.5.0", "March 4 2018", [
        "Oracle text update - fixes issues with 0 cost colored cards showing as colorless",
        "Added Masters 25.",
        "Attacking and blocking cards will separate from alignment piles."
        ]),
    3040600: ("3.4.6.0", "April 12 2018", [
        "Added Dominaria"
        ]),
    3040700: ("3.4.7.0", "May 13 2018", [
        "Fixed an issue with merfolk hexproof tokens being shown as illusion tokens",
        "bug fix with multi-modal spells",
        "Updated oracle text for dominaria's big changes"
        ]),
    3040800: ("3.4.8.0", "June 3 2018", [
        "Added Battlebond",
        "Added Duel Decks: Elves vs Inventors"
        ]),
    3040900: ("3.4.9.0", "June 24 2018", [
        "Added Core Set 2019, Global Deck Series, Jace Spellbook, and Commander Anthology 2"
        ]),
    3040901: ("3.4.9.1", "July 10 2018", [
        "Fixed some bugs with meld cards not working in-game, in the deck editor, and through the image downloader"
        ]),
    3040902: ("3.4.9.2", "July 11 2018", [
        "Added M19 tokens"
        ]),
    3040903: ("3.4.9.3", "July 30 2018", [
        "Added Commander 2018"
        ]),
    3041000: ("3.4.10.0", "September 22 2018", [
        "Added Guilds of Ravnica",
        "Land Creatures now align in creature row",
        "Minor performance improvements to alignment when using certain actions on a selection of cards"
        ]),
    3041001: ("3.4.10.1", "October 12 2018", [
        "Updated Guilds of Ravnica with proper booster pack content and added tokens",
        "Removed some unused tokens -- previously saved token arts may have changed"
        ]),
    3041002: ("3.4.10.2", "December 19 2018", [
        "Added Ultimate Masters (tokens coming soon)"
        ]),
    3041003: ("3.4.10.3", "January 12 2019", [
        "Added Ravnica Allegiance",
        "Added RNA and UMA tokens"
        ]),
    3041100: ("3.4.11.0", "January 23 2019", [
        "Replaced autoscript settings actions with a single dialog window",
        "Redesign of automatic alignment system, fixing several bugs involving alignment of attachments",
        "Rancor-style attachments will no longer crash OCTGN when the target card leaves play",
        "Changes to the Auto-Pass Priority system, and how it interacts with players who have autoscripts disabled",
        "Alignment now groups tapped cards separately from untapped cards",
        "NOTE: Some of these changes may have bugs -- please let me know via the discord channel if any oddities occur!"
        ]),
    3041101: ("3.4.11.1", "January 28 2019", [
        "Removed Attachment Alignment setting -- it's now shared with regular alignment",
        "Dragging a card to the table will not anchor it to the table by default",
        "Fixed moving a card to the bottom of a pile"
        ]),
    3041102: ("3.4.11.2", "April 21 2019", [
        "Added War of the Spark"
        ]),
    3041103: ("3.4.11.3", "June 2 2019", [
        "Added Modern Horizons and Gideon Spellbook"
        ]),
    3041104: ("3.4.11.4", "July 8 2019", [
        "Added Core Set 2020"
        ]),
    3041105: ("3.4.11.5", "August 29 2019", [
        "Added Commander 2019"
        ]),
    3041106: ("3.4.11.6", "September 20 2019", [
        "Added Throne of Eldraine"
        ]),
    3050000: ("3.5.0.0", "October 14 2019", [
        "Massive changes to set structure -- most GUIDs for cards have changed. All decks should still be valid, however they may have changed printings.",
        "You will need to run the image downloader plugin to re-install most images due to this change.",
        "Lots of fixes to card data, including Adventure, Split, Meld, and other non-standard card layouts.",
        "Mulligans have been updated to the London rules.",
        "Adventure card support in scripting."
        ]),
    3050001: ("3.5.0.1", "January 11 2020", [
        "Added Theros Beyond Death"
        ]),
    3050002: ("3.5.0.2", "March 15 2020", [
        "Added Mystery Boosters"
        ]),
    3050004: ("3.5.0.4", "April 8 2020", [
        "Added Secret Lair Drops, Commander 2020 (no tokens yet)"
        ]),
    3050005: ("3.5.0.5", "April 10 2020", [
        "Added Ikoria"
        ]),
    3060000: ("3.6.0.0", "May 23 2020", [
        "Added missing planes and schemes sets",
        "fixed some bugs with the image downloader",
        ]),
    3060100: ("3.6.1.0", "June 17 2020", [
        "Added M21, Chandra Spellbook, Secret Lair Ultimate Edition,  and Unsanctioned",
        "New table card action:  CTRL+SHIFT+C  toggles the Commander indicator marker on the card.",
        "New Command Zone card action:  DOUBLE-CLICK casts the card as your Commander.",
        "Changed Command Zone card action hotkey: CTRL+C  Cast Card (was the default double-click action.)",
        "Anchoring a card or putting the Commander indicator marker on a card will prevent it from auto-aligning.",
        "fixed a bug affecting token images in the image downloader.",
        ]),
    3060101: ("3.6.1.1", "June 20 2020", [
        "Added Jumpstart"
        ]),
    3060102: ("3.6.1.2", "June 22 2020", [
        "Added Jumpstart",
        "Jumpstart decks can be loaded directly from the preset decks menu option.",
        "An option to load two random Jumpstart decks has also been added to the Library group actions menu."
        ]),
    3060103: ("3.6.1.3", "July 31 2020", [
        "Added Double Masters"
        ]),
    3060200: ("3.6.2.0", "September 14 2020", [
        "Added Zendikar Rising and Commander Green",
        "Scripting support for casting modal double-faced cards (works like adventure cards)",
        "Removed flavor text property (at least until they can decide on a consistent formatting)",
        "Large update to image fetcher plugin:",
        "- should start up faster, use less CPU and RAM, and download less data",
        "-  a checkbox to skip cards that already have an image installed",
        "-  support for downloading images in other languages (does not affect card database properties)"
        ]),
    3060202: ("3.6.2.2", "October 16 2020", [
        "Added Zendikar Rising Commander, Mythic Edition Promos, and updated Secret Lair set."
        ]),
    3060203: ("3.6.2.3", "November 7 2020", [
        "Added Commander Legends.",
        "Fixed Dominaria booster packs to properly seed the legendary creature slot."
        ]),
    3060204: ("3.6.2.4", "December 11 2020", [
        "Added The Prismatic Piper to the Commander Legends unlimited land booster.",
        "Added a few missing cards from the CMR set."
        ]),
    3060205: ("3.6.2.5", "January 20 2021", [
        "Added Kaldheim.",
        "Updated Secret Lair cards."
        ]),
    3060207: ("3.6.2.7", "January 24 2021", [
        "Added missing Game Night expansions"
        ]),
    3060208: ("3.6.2.8", "February 4 2021", [
        "Added a new table action to manage secret/hidden values"
        ]),
    3060210: ("3.6.2.10", "April 4 2021", [
        "Added Strixhaven (tokens and japanese masterpiece not yet available)"
        ]),
    3060212: ("3.6.2.12", "June 3 2021", [
        "Added Strixhaven Alt-Art Mystical Archives",
        "Updated Secret Lair sets",
        "Added Modern Horizons 2"
        ]),
    3060213: ("3.6.2.13", "July 12 2021", [
        "Added Adventures in the Forgotten Realms",
        "New table group action (underneath the 'create a token...' action to create dungeon tokens",
        "(Use the 'activate ability' card action to choose a room to venture into)",
        "Removed PT Box and MultiverseId card properties, added a new Loyalty property",
        "Updated all rules text, including the Phyrexian creature type errata"
        ]),
    3060214: ("3.6.2.14", "July 13 2021", [
        "Improved the 'shuffle cards to bottom of library' table action to not reveal the order the cards appear"
        ]),
    3060215: ("3.6.2.15", "September 11 2021", [
        "Added Innistrad Midnight Hunt (tokens coming soon)"
        ]),
    3060217: ("3.6.2.17", "September 25 2021", [
        "Added Innistrad Midnight Hunt tokens, and fixed the booster algorithm for the draft set"
        ]),
    3060218: ("3.6.2.18", "November 6 2021", [
        "Added Crimson Vow + Commander, updated secret lairs"
        ]),
    3060220: ("3.6.2.20", "February 6 2022", [
        "Added Kamigawa Neon Dynasty (full commander decks and tokens coming soon)"
        ]),
    3060222: ("3.6.2.22", "March 26 2022", [
        "Added GRN/RNA Guild Kits, updated secret lair sets",
        "Unique JPN and Phyrexian language cards (i.e. mystical archives) added to sets",
        "Some cleanup to older sets",
        ]),
    3060224: ("3.6.2.24", "April 29 2022", [
        "New Capenna update"
        ]),
    3060226: ("3.6.2.26", "June 4 2022", [
        "Commander Legends 2 update",
        "Removed duplicate token arts.  You will need to re-download the Tokens set images to update the correct arts."
        ]),
    3060228: ("3.6.2.28", "September 4 2022", [
        "Dominaria United added"
        ]),
    3060230: ("3.6.2.30", "October 13 2022", [
        "Added W40K, 30th Anniversry, Unfinity"
        ]),
    3060231: ("3.6.2.31", "November 12 2022", [
        "Added Brothers War, some missing promos and tokens"
        ]),
    3060300: ("3.6.3.0", "Jan 7 2023", [
        "Disabled autoscript tag web queries.  Cards no longer have individual automation scripting",
        "New submenu for cards in table for auto-token and auto-counter features",
        "'Auto-Create Token' (ctrl+shift+T) now recognizes tokens referenced in card text",
        "'Manually-Assign Token' card action lets you override specific tokens to a card (in the event the auto-create action malfunctions",
        "'Auto-Add Counter' (ctrl+1) now recognizes counters referenced in card text",
        "'Manually-Assign Counters' (ctrl+shift+1) card action lets you override specific counters to a card (if the auto-add fails)",
        "'Smart-Copy Counter' (ctrl+2),  will copy the card's counter data into the clipboard (previously used in the 'smart counter' automation code",
        "'Add Smart Counter' (ctrl+shift+1) changed to 'Smart-Paste Counter' (ctrl+shift+2)",
        "Removed the 'remove counter' actions as they can be removed by simply dragging counters off the card.",
        "'Add +1+1 counter' hotkey changed to ctrl+3",
        "'Add -1-1 counter' hotkey changed to ctrl+shift+3"
        ])
}