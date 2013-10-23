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
        ])
}