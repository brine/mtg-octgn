import re
import time
import clr
from System import Convert
from System import Text

#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------

phases = [
    "It is now the Pre-game Setup Phase",
    "It is now {}'s UNTAP Step",
    "It is now {}'s UPKEEP Step",
    "It is now {}'s DRAW Step",
    "It is now {}'s FIRST MAIN Phase",
    "It is now {}'s BEGINNING OF COMBAT Step",
    "It is now {}'s DECLARE ATTACKERS Step",
    "It is now {}'s DECLARE BLOCKERS Step",
    "It is now {}'s COMBAT DAMAGE Step",
    "It is now {}'s SECOND MAIN Phase",
    "It is now {}'s ENDING Phase"]

AttackColor = "#ff0000"
BlockColor = "#00ff00"
DoesntUntapColor = "#000000"
AutoscriptColor = "#0000ff"
AttackDoesntUntapColor = "#660000"
BlockDoesntUntapColor = "#007700"
MiracleColor = "#1D7CF2"

defaultX = 30
defaultY = 25

phaseIdx = 0
diesides = 20

playerside = None
sideflip = None
offlinedisable = False
savedtags = { }
timer = []
debugMode = False
alignIgnore = []

stackDict = {} ## Needs to move to a global variable for game reconnects
costMemory = (0,0)
#---------------------------------------------------------------------------
# Event Stuff
#---------------------------------------------------------------------------

def registerPlayer(player, groups = []): #this function triggers off loading a deck, and registers the player as active
    mute()
    if player == me: #only process the local player
        playersDict = eval(getGlobalVariable('activePlayers')) #the activePlayers variable just keeps track of the active players in the game
        playersDict[me._id] = autoscriptCheck() #keeps track of who's allergic to fun
        setGlobalVariable('activePlayers', str(playersDict))

def priorityResolve(name, oldValue, value):
    if name == 'priority' and value == '[]':
        stack = [c for c in table
                if isStack(c)]
        if len(stack) == 0:
            return
        if stack[-1].controller == me and autoscriptCheck() == "True":
            resolve(stack[-1])
            cardalign()

def endTurn(player):
    mute()
    if player == me:
        clearAll(table, x = 0, y = 0)

def moveEvent(player, card, fromGroup, toGroup, oldIndex, index, oldX, oldY, x, y, isScriptMove):
    mute()
    if isScriptMove:  ## Ignore script-based movements
        return
    if player != me:
        return
    if fromGroup != table or toGroup != table:  ## Ignore non-table movements
        return
    global alignIgnore
    if not card in alignIgnore and alignCheck() == "True":  ## Moving a card will automatically disable it from alignment
        alignIgnore.append(card)  ## anchors the card to the table
    if attachCheck():
        alignAttachments(card)

def initializeGame():
    mute()
    #### INITIALIZE VARIABLES
    global debugMode
    debugMode = getSetting("debugTimer", "False")
    #### LOAD UPDATES
    v1, v2, v3, v4 = gameVersion.split('.')  ## split apart the game's version number
    v1 = int(v1) * 1000000
    v2 = int(v2) * 10000
    v3 = int(v3) * 100
    v4 = int(v4)
    currentVersion = v1 + v2 + v3 + v4  ## An integer interpretation of the version number, for comparisons later
    lastVersion = getSetting("lastVersion", convertToString(currentVersion - 1))  ## -1 is for players experiencing the system for the first time
    lastVersion = int(lastVersion)
    for log in sorted(changelog):  ## Sort the dictionary numerically
        if lastVersion < log:  ## Trigger a changelog for each update they haven't seen yet.
            stringVersion, date, text = changelog[log]
            updates = '\n-'.join(text)
            confirm("What's new in {} ({}):\n-{}".format(stringVersion, date, updates))
    setSetting("lastVersion", convertToString(currentVersion))  ## Store's the current version to a setting

#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------
def respond(group, x = 0, y = 0):
    notify('{} RESPONDS!'.format(me))

def passPriority(group, x = 0, y = 0, autoscriptOverride = False):
    if autoscriptCheck() == "True" or autoscriptOverride == True:
        priorityList = eval(getGlobalVariable('priority'))
        if me._id in priorityList:
            priorityList.remove(me._id)
            setGlobalVariable('priority', str(priorityList))
            notify('{} passes priority.'.format(me))
        elif autoscriptOverride == False:
            whisper('You already passed priority.')
    else:
        notify('{} passes priority to an opponent.'.format(me))

def autoPass(group, x = 0, y = 0):
    mute()
    if not autoscriptCheck():  ## autoscripts must be enabled to use this
        return
    if me.getGlobalVariable("f6") == "False":
        me.setGlobalVariable("f6", "True")
        whisper("You are now auto-passing priority.")
        passPriority(group)
    else:
        me.setGlobalVariable("f6", "False")
        whisper("You turned off auto-pass priority.")

def showCurrentPhase(group, x = 0, y = 0):
    notify(phases[phaseIdx].format(me))

def nextPhase(group, x = 0, y = 0):
    global phaseIdx
    if phaseIdx == 10:
        phaseIdx = 1
    else:
        phaseIdx += 1
    if phaseIdx == 1:
        untapStep(group)
    showCurrentPhase(group)

def untapStep(group, x = 0, y = 0):
    mute()
    myCards = (card for card in table
        if card.controller == me
        and card.highlight != DoesntUntapColor)
    for card in myCards:
        if card.highlight == AttackDoesntUntapColor or card.highlight == BlockDoesntUntapColor:
            card.highlight = DoesntUntapColor
        else:
            card.orientation &= ~Rot90
            card.highlight = None

def goToUpkeep(group, x = 0, y = 0):
    global phaseIdx
    phaseIdx = 2
    untapStep(group)
    showCurrentPhase(group)

def goToFirstMain(group, x = 0, y = 0):
    global phaseIdx
    phaseIdx = 4
    showCurrentPhase(group)

def goToCombat(group, x = 0, y = 0):
    global phaseIdx
    phaseIdx = 5
    showCurrentPhase(group)

def goToSecondMain(group, x = 0, y = 0):
    global phaseIdx
    phaseIdx = 9
    showCurrentPhase(group)

def goToEnding(group, x = 0, y = 0):
    global phaseIdx
    phaseIdx = 10
    showCurrentPhase(group)

def lose1Life(group, x = 0, y = 0):
    me.life -= 1

def gain1Life(group, x = 0, y = 0):
    me.life += 1

def scoop(group, x = 0, y = 0):
    mute()
    if not confirm("Are you sure you want to scoop?"):
        return
    me.life = 20
    me.poison = 0
    me.white = 0
    me.blue = 0
    me.black = 0
    me.red = 0
    me.green = 0
    me.colorless = 0
    me.general = 0
    for card in me.Library:
        card.moveTo(card.owner.Library)
    myCards = (card for card in table
        if card.controller == me)
    for card in myCards:
        card.moveTo(card.owner.Library)
    for card in me.Graveyard:
        card.moveTo(card.owner.Library)
    for card in me.hand:
        card.moveTo(card.owner.Library)
    exile = me.piles['Exiled Zone']
    for card in exile:
        card.moveTo(card.owner.Library)
    notify("{} scoops.".format(me))

def clearAll(group, x = 0, y = 0):
    notify("{} clears all targets and highlights.".format(me))
    for card in group:
#        if card.targetedBy and card.targetedBy == me:    ### Commented out until target arrows are fixed
        if card.controller == me:
            card.target(False)
            if card.highlight in [AttackColor, BlockColor]:
                card.highlight = None
            elif card.highlight in [AttackDoesntUntapColor, BlockDoesntUntapColor]:
                card.highlight = DoesntUntapColor

def setDie(group, x = 0, y = 0):
    mute()
    global diesides
    num = askInteger("How many sides?\n\nFor Coin, enter 2.\nFor Chaos die, enter 6.", diesides)
    if num != None and num > 0:
        diesides = num
        dieFunct(diesides)

def rollDie(group, x = 0, y = 0):
    mute()
    global diesides
    dieFunct(diesides)

def dieFunct(num):
    if num == 6:
        n = rnd(1, 6)
        if n == 1:
            notify("{} rolls 1 (PLANESWALK) on a 6-sided die.".format(me))
        elif n == 6:
            notify("{} rolls 6 (CHAOS) on a 6-sided die.".format(me))
        else:
            notify("{} rolls {} on a 6-sided die.".format(me, n))
    elif num == 2:
        n = rnd(1, 2)
        if n == 1:
            notify("{} rolls 1 (HEADS) on a 2-sided die.".format(me))
        else:
            notify("{} rolls 2 (TAILS) on a 2-sided die.".format(me))
    else:
        n = rnd(1, num)
        notify("{} rolls {} on a {}-sided die.".format(me, n, num))
      
def token(group, x = 0, y = 0):
    card, quantity = askCard({"Rarity":"Token"}, "And")
    if quantity == 0:
        return
    token = table.create(card, x, y, quantity)
    artDict = getSetting('tokenArts', convertToString({}))
    artDict = eval(artDict)
    if token.model in artDict:
        token.switchTo(artDict[token.model])

#--------------------------------
# Autoscript-Linked Card functions
#--------------------------------

def scry(group = me.Library, x = 0, y = 0, count = None):
    mute()
    if count == None:
        count = askInteger("Scry how many cards?", 1)
    if count == None or count == 0:
        return
    topCards = group.top(count)
    buttons = []  ## This list stores all the card objects for manipulations.
    for c in topCards:
        c.peek()  ## Reveal the scryed cards to python
        buttons.append(c)
    topList = []  ## This will store the cards selected for the top of the pile
    bottomList = []  ## For cards going to the bottom of the pile
    rnd(1,2)  ## allow the peeked card's properties to load
    loop = 'BOTTOM'  ## Start with choosing cards to put on bottom
    while loop != None:
        desc = "Select a card to place on {}:\n\n{}\n///////DECK///////\n{}".format(
                loop,
                '\n'.join([c.Name for c in topList]),
                '\n'.join([c.Name for c in bottomList]))
        if loop == 'TOP':
            num = askChoice(desc, [c.Name for c in buttons], customButtons = ["Switch to BOTTOM"])
            if num == -1:
                loop = 'BOTTOM'
            elif num != 0:
                card = buttons.pop(num - 1)
                topList.insert(0, card)
        else:
            num = askChoice(desc, [c.Name for c in buttons], customButtons = ["Switch to TOP"])
            if num == -1:
                loop = 'TOP'
            elif num != 0:
                card = buttons.pop(num - 1)
                bottomList.append(card)
        if len(buttons) == 0: ##  End the loop
            loop = None
        if num == None:  ## closing the dialog window will cancel the scry, not moving any cards, but peek status will stay on.
            return
    topList.reverse()  ## Gotta flip topList so the moveTo's go in the right order
    for c in topList:
        c.moveTo(group)
    for c in bottomList:
        c.moveToBottom(group)
    for c in group:  ## This is currently the only way to un-peek at cards.
        c.isFaceUp = True
        c.isFaceUp = False
    notify("{} scryed for {}, {} on top, {} on bottom.".format(me, count, len(topList), len(bottomList)))

def play(card, x = 0, y = 0):
    mute()
    timer = time.clock()
    if autoscriptCheck() == "True":
        src = card.group
        if src == me.hand:
            srcText = ""
        else:
            srcText = " from {}".format(src.name)
        text = autoParser(card, 'cast')
        timer = debugWhisper("play1", card, timer)
        if text != "BREAK":
            timer = time.clock()
            ## Checks to see if the cast card is an Aura, then check to see if a target was made to resolve-attach to
            if (card.Subtype != None and re.search(r'Aura', card.Subtype)) or re.search(r'Bestow ', card.Rules):  ## Automatically register the card as an attachment if it's an Aura or Bestow
                target = (card for card in table if card.targetedBy)
                targetcount = sum(1 for card in table if card.targetedBy)
                if targetcount == 1:
                    for targetcard in target:
                        cattach = eval(getGlobalVariable('cattach'))
                        cattach[card._id] = targetcard._id
                        targetcard.target(False)
                        setGlobalVariable('cattach', str(cattach))
                        text += ", targeting {}".format(targetcard)
            timer = debugWhisper("play2", card, timer)
            ## If its a land, automatically resolve it
            if re.search('Land', card.Type):
                text += autoParser(card, 'resolve')
                notify("{} plays {}{}.".format(me, card, text))
                autoParser(card, 'etb')
                timer = debugWhisper("play3", card, timer)
            else:
                modeTuple = stackDict[card]['mode']
                if modeTuple[0] == 0:
                    notify("{} casts {}{}{}.".format(me, card, srcText, text))
                else:
                    notify("{} casts {} (mode #{}){}{}.".format(me, card, modeTuple[0], srcText, text))
                timer = debugWhisper("play4", card, timer)
            cardalign()
            timer = debugWhisper("play5", card, timer)
    else:
        src = card.group
        if re.search("Instant", card.Type) or re.search("Sorcery", card.Type):
            card.moveTo(card.owner.Graveyard)
        else:
            card.moveToTable(defaultX, defaultY)
        notify("{} plays {} from their {}.".format(me, card, src.name))
        timer = debugWhisper("play6", card, timer)
        cardalign()
        timer = debugWhisper("play7", card, timer)

def flashback(card, x = 0, y = 0):
    mute()
    global stackDict
    play(card)
    stackDict[card]['moveto'] = 'exile'

def batchResolve(cards, x = 0, y = 0):
    mute()
    for card in cards:
        resolve(card)
    cardalign()

def resolve(card, x = 0, y = 0):
    mute()
    global stackDict
    if autoscriptCheck() == "True":
        if scriptMarkers['suspend'] in card.markers:
            if counters['time'] in card.markers:
                card.markers[counters['time']] -= 1
            if counters['time'] in card.markers:
                notify("{} removed a time counter from suspended {}.".format(me, card))
            else:
                text = autoParser(card, 'cast')
                if text != "BREAK":
                    card.markers[scriptMarkers['suspend']] = 0
                    notify("{} casts suspended {}{}.".format(me, card, text))
            return
        if card in stackDict:
            tagClass = stackDict[card]['class']
            tagSrc = stackDict[card]['src']
            moveTo = stackDict[card]['moveto']
            text = autoParser(card, 'resolve')
            if tagClass == 'miracle':
                if tagSrc in me.hand:
                    play(tagSrc)
                else:
                    notify("{}'s {} Miracle trigger is countered.".format(me, card))
            else:
                notify("{} resolves {} ({}){}".format(me, card, tagClass, text))
            if moveTo == 'exile':
                card.moveTo(card.owner.piles['Exiled Zone'])
            elif tagClass == 'cast' and not re.search('Instant', card.Type) and not re.search('Sorcery', card.Type): #handles permanents etb triggers
                autoParser(card, 'etb')
            else: #non-permanents and ability triggers are sent to graveyard after resolution
                card.moveTo(card.owner.Graveyard)
        else:
            card.orientation ^= Rot90
            if card.orientation & Rot90 == Rot90:
                notify('{} taps {}'.format(me, card))
            else:
                notify('{} untaps {}'.format(me, card))
    else:
        card.orientation ^= Rot90
        if card.orientation & Rot90 == Rot90:
            notify('{} taps {}'.format(me, card))
        else:
            notify('{} untaps {}'.format(me, card))

def batchDestroy(cards, x = 0, y = 0):
    mute()
    for card in cards:
        destroy(card)
    cardalign()

def destroy(card, x = 0, y = 0):
    mute()
    global stackDict
    src = card.group
    if autoscriptCheck() == "True" and src == table:
        if card in stackDict: #Destroying a card on a stack is considered countering that spell
            if stackDict[card]['moveto'] == 'exile':
                card.moveTo(card.owner.piles['Exiled Zone'])
            else:
                card.moveTo(card.owner.Graveyard)
            del stackDict[card]
            notify("{}'s {} was countered.".format(me, card))
            return
        text = autoParser(card, 'destroy')
        if text != "BREAK":
            card.moveTo(card.owner.Graveyard)
            notify("{} destroys {}{}.".format(me, card, text))
    else:
        card.moveTo(card.owner.Graveyard)
        notify("{} destroys {}.".format(me, card))

def discard(card, x = 0, y = 0):
    mute()
    src = card.group
    if autoscriptCheck() == "True":
        if src == me.hand:  ## Only run discard scripts if the card is discarded from hand
            text = autoParser(card, 'discard')
        else:
            text = ""
        if text != "BREAK":
            card.moveTo(card.owner.Graveyard)
            notify("{} discards {} from {}{}.".format(me, card, src, text))
    else:
        card.moveTo(card.owner.Graveyard)
        notify("{} discards {} from {}.".format(me, card, src))

def batchExile(cards, x = 0, y = 0):
    mute()
    for card in cards:
        exile(card)
    cardalign()

def exile(card, x = 0, y = 0):
    mute()
    src = card.group
    if autoscriptCheck() == "True" and src == table:
        text = autoParser(card, 'exile')
        if text != "BREAK":
            card.moveTo(card.owner.piles['Exiled Zone'])
            notify("{} exiles {}{}.".format(me, card, text))
    else:
        fromText = " from the battlefield" if src == table else " from their " + src.name
        card.moveTo(card.owner.piles['Exiled Zone'])
        notify("{} exiles {}{}.".format(me, card, fromText))

def batchAttack(cards, x = 0, y = 0):
    mute()
    for card in cards:
        attack(card)
    cardalign()

def attack(card, x = 0, y = 0):
    mute()
    if autoscriptCheck() == "True":
        if card.orientation == Rot90:
            if confirm("Cannot attack: already tapped. Continue?") != True:
                return
        elif card.highlight == AttackColor or card.highlight == AttackDoesntUntapColor:
            if confirm("Cannot attack: already attacking. Continue?") != True:
                return
        card.orientation |= Rot90
        if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
            card.highlight = AttackDoesntUntapColor
        else:
            card.highlight = AttackColor
        text = autoParser(card, 'attack')
        if text != "BREAK":
            notify("{} attacks with {}{}.".format(me, card, text))
    else:
        card.orientation |= Rot90
        if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
            card.highlight = AttackDoesntUntapColor
        else:
            card.highlight = AttackColor
        notify('{} attacks with {}'.format(me, card))

def batchAttackWithoutTapping(cards, x = 0, y = 0):
    mute()
    for card in cards:
        attackWithoutTapping(card)
    cardalign()

def attackWithoutTapping(card, x = 0, y = 0):
    mute()
    if autoscriptCheck() == "True":
        if card.orientation == Rot90:
            if confirm("Cannot attack: {} is tapped. Continue?".format(card)) != True:
                return
        elif card.highlight == AttackColor or card.highlight == AttackDoesntUntapColor:
            if confirm("Cannot attack: already attacking. Continue?") != True:
                return
        if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
            card.highlight = AttackDoesntUntapColor
        else:
            card.highlight = AttackColor
        text = autoParser(card, 'attack')
        if text != "BREAK":
            notify("{} attacks without tapping with {}{}.".format(me, card, text))
    else:
        if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
            card.highlight = AttackDoesntUntapColor
        else:
            card.highlight = AttackColor
        notify('{} attacks without tapping with {}'.format(me, card))

def batchBlock(cards, x = 0, y = 0):
    mute()
    for card in cards:
        block(card)
    cardalign()

def block(card, x = 0, y = 0):
    mute()
    if autoscriptCheck() == "True":
        if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
            card.highlight = BlockDoesntUntapColor
        else:
            card.highlight = BlockColor
        text = autoParser(card, 'block')
        if text != "BREAK":
            notify("{} blocks with {}{}.".format(me, card, text))
    else:
        if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
            card.highlight = BlockDoesntUntapColor
        else:
            card.highlight = BlockColor
        notify('{} blocks with {}'.format(me, card))

def batchActivate(cards, x = 0, y = 0):
    mute()
    for card in cards:
        activate(card)
    cardalign()

def activate(card, x = 0, y = 0):
    mute()
    if autoscriptCheck() == "True":
        text = autoParser(card, 'acti')
        if text != "BREAK":
            (num, text) = text
            notify("{} activates {}'s ability #{}{}.".format(me, card, num, text))
    else:
        notify("{} uses {}'s ability.".format(me, card))

def morph(card, x = 0, y = 0):
    mute()
    if autoscriptCheck() == "True":
        card.isFaceUp = False
        text = autoParser(card, 'cast', True)
        cardalign()
        if text == "BREAK":
            card.isFaceUp = True
        else:
            notify("{} casts a card face-down.".format(me))
    src = card.group
    notify("{} casts a card face-down from their {}.".format(me, src.name))
    card.moveToTable(defaultX, defaultY, True)
    if autoscriptCheck() == "True":
        card.markers[scriptMarkers['cast']] = 1
        cardalign()

def transform(card, x = 0, y = 0):
    mute()
    alt = card.alternates
    if 'transform' in alt:
        notify("{} transforms {}.".format(me, card))
        if card.alternate == '':
            card.switchTo('transform')
        else:
            card.switchTo()
    elif 'flip' in alt:
        notify("{} flips {}.".format(me, card))
        if card.alternate == '':
            card.switchTo('flip')
        else:
            card.switchTo()
    else:
        if card.isFaceUp == True:
            notify("{} morphs {} face down.".format(me, card))
            card.isFaceUp = False
        else:
            if autoscriptCheck() == "True":
                card.peek()
                rnd(1,10)
                text = autoParser(card, 'morph') ## The card will flip up in the autoParser
                cardalign()
                if text != "BREAK":
                    notify("{} morphs {} face up{}.".format(me, card, text))
            else:
                card.isFaceUp = True
                notify("{} morphs {} face up.".format(me, card))

def suspend(card, x = 0, y = 0):
    mute()
    num = askInteger("Suspending {}, what is X?)".format(card.Name), 0)
    if num != 0 and num != None:
        card.moveToTable(defaultX, defaultY)
        card.markers[scriptMarkers['suspend']] = 1
        card.markers[counters['time']] = num
        cardalign()
        notify("{} suspends {} for {}.".format(me, card, num))

def blink(card, x = 0, y = 0):
    mute()
    src = card.group
    if src == table:
        if autoscriptCheck() == "True":
            text = autoParser(card, 'exile')
            if text == "BREAK":
                return
            card.moveTo(card.owner.piles['Exiled Zone'])
            cardalign()
            card.moveToTable(defaultX, defaultY)
            autoParser(card, 'cast', True)
            cardalign()
            notify("{} blinks {}.".format(me, card))
        else:
            clear(card)
            notify("{} blinks {}.".format(me, card))

#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def rulings(card, x = 0, y = 0):
    mute()
    if not card.MultiverseId == None:
        openUrl('http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid={}'.format(card.MultiverseId))

def generaltoggle(card, x = 0, y = 0): ## This isn't used anymore
    mute()
    if counters['general'] in card.markers:
        card.markers[counters['general']] = 0
        notify("{}'s commander {} enters the battlefield.".format(me, card))
    else:
        card.markers[counters['general']] = 1
        notify("{}'s commander {} leaves the battlefield.".format(me, card))

def doesNotUntap(card, x = 0, y = 0):
    mute()
    if card.highlight == AttackColor:
        card.highlight = AttackDoesntUntapColor
        notify("{0}'s {1} will not untap during {0}'s untap step.".format(me, card))
    elif card.highlight == AttackDoesntUntapColor:
        card.highlight = AttackColor
        notify("{0}'s {1} can now untap during {0}'s untap step.".format(me, card))
    elif card.highlight == BlockColor:
        card.highlight = BlockDoesntUntapColor
        notify("{0}'s {1} will not untap during {0}'s untap step.".format(me, card))
    elif card.highlight == BlockDoesntUntapColor:
        card.highlight = BlockColor
        notify("{0}'s {1} can now untap during {0}'s untap step.".format(me, card))
    elif card.highlight == DoesntUntapColor:
        card.highlight = None
        notify("{0}'s {1} can now untap during {0}'s untap step.".format(me, card))
    else:
        card.highlight = DoesntUntapColor
        notify("{0}'s {1} will not untap during {0}'s untap step.".format(me, card))

def flip(card, x = 0, y = 0):
    mute()
    if card.isFaceUp == True:
        notify("{} flips {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} flips {} face up.".format(me, card))

def clear(card, x = 0, y = 0):
    notify("{} clears {}.".format(me, card))
    card.highlight = None
    card.target(False)

def clone(cards, x = 0, y = 0):
    for card in cards:
        copy = table.create(card.model, x, y, 1)
        if card.alternate != '':
            copy.switchTo()
        x, y = table.offset(x, y)

#---------------------------------------------------------------------------
# Marker Manipulations
#---------------------------------------------------------------------------

def addMarker(cards, x = 0, y = 0):
    mute()
    marker, quantity = askMarker()
    if quantity == 0:
        return
    for card in cards:
        card.markers[marker] += quantity
        notify("{} adds {} {} counters to {}.".format(me, quantity, marker[0], card))

def addMinusOneMarker(card, x = 0, y = 0):
    mute()
    notify("{} adds a -1/-1 counter to {}.".format(me, card))
    if counters['p1p1'] in card.markers:
        card.markers[counters['p1p1']] -= 1
    else:
        card.markers[counters['m1m1']] += 1

def addPlusOneMarker(card, x = 0, y = 0):
    mute()
    notify("{} adds a +1/+1 counter to {}.".format(me, card))
    if counters['m1m1'] in card.markers:
        card.markers[counters['m1m1']] -= 1
    else:
        card.markers[counters['p1p1']] += 1

def addChargeMarker(card, x = 0, y = 0):
    mute()
    notify("{} adds a Charge counter to {}.".format(me, card))
    card.markers[counters['charge']] += 1

def removePlusOneMarker(card, x = 0, y = 0):
    mute()
    addmarker = counters['p1p1']
    if addmarker in card.markers:
        card.markers[addmarker] -= 1
        markername = addmarker[0]
        notify("{} removes a {} from {}".format(me, markername, card))

def removeMinusOneMarker(card, x = 0, y = 0):
    mute()
    addmarker = counters['m1m1']
    if addmarker in card.markers:
        card.markers[addmarker] -= 1
        markername = addmarker[0]
        notify("{} removes a {} from {}".format(me, markername, card))

def removeChargeMarker(card, x = 0, y = 0):
    mute()
    addmarker = counters['charge']
    if addmarker in card.markers:
        card.markers[addmarker] -= 1
        markername = addmarker[0]
        notify("{} removes a {} from {}".format(me, markername, card))

#---------------------------
#Group Movement Actions
#---------------------------

def tolibrary(card, x = 0, y = 0):
    mute()
    src = card.group
    fromText = "Battlefield" if src == table else src.name
    notify("{} moves {} from {} to Library.".format(me, card, fromText))
    card.moveTo(card.owner.Library)

def tolibraryposition(card, x = 0, y = 0):
    mute()
    pos = askInteger("Move to what position?\nNOTE: 0 is the top.", 0)
    if pos == None:
        return
    src = card.group
    fromText = "the Battlefield" if src == table else src.name
    if pos == None:
        return
    if pos > len(me.Library):
        notify("{} moves {} from {} to Library (bottom).".format(me, card, fromText))
        card.moveToBottom(card.owner.Library)
    elif pos == 0:
        notify("{} moves {} from {} to Library (top).".format(me, card, fromText))
        card.moveTo(card.owner.Library)
    else:
        notify("{} moves {} from {} to Library ({} from top).".format(me, card, fromText, pos))
        card.moveTo(card.owner.Library, pos)

def libraryBottomAllShuffle(cards, x = 0, y = 0):
    mute()
    count = 0
    emergencyStop = len(cards) + 4 ## just in case something causes an infinite while loop
    while len(cards) > 0:
        emergencyStop -= 1
        if emergencyStop == 0:
            break
        index = rnd(0, len(cards) - 1)
        card = cards.pop(index)
        if card.controller == me:
            card.moveToBottom(card.owner.piles['Library'])
            count += 1
    notify("{} shuffles {} selected cards to the bottom of their Library.".format(me, count))

def tohand(card, x = 0, y = 0):
    mute()
    src = card.group
    if src == table:
        notify("{} moves {} to their hand from the battlefield.".format(me, card))
    else:
        if card.isFaceUp == False:
            if confirm("Reveal to all players?"):
                card.isFaceUp = True
                rnd(10,100)
                cardname = card
            else:
                cardname = "a card"
        else:
            cardname = card
        notify("{} moves {} to their hand from their {}.".format(me, cardname, src.name))
    card.moveTo(card.owner.hand)

def randomDiscard(group, x = 0, y = 0):
    mute()
    card = group.random()
    if card == None:
        return
    card.isFaceUp = True
    rnd(10,100)
    notify("{} randomly discards {}.".format(me, card))
    card.moveTo(card.owner.Graveyard)

def randomPick(group, x = 0, y = 0):
    mute()
    card = group.random()
    if card == None:
        return
    card.select()
    card.target(True)
    if not card.isFaceUp:
        if confirm("Reveal randomly-picked {}?".format(card.Name)):
            card.isFaceUp = True
        rnd(10,100)
    if group == table:
        notify("{} randomly picks {}'s {} on the battlefield.".format(me, card.controller, card))
    else:
        notify("{} randomly picks {} from their {}.".format(me, card, group.name))

def mulligan(group, x = 0, y = 0):
    mute()
    newCount = len(group) - 1
    if newCount < 0:
        return
    if not confirm("Mulligan down to %i ?" % newCount):
        return
    notify("{} mulligans down to {}".format(me, newCount))
    for card in group:
        card.moveTo(card.owner.Library)
    uselessvar = rnd(10, 1000)
    shuffle(me.Library, silence = True)
    for card in me.Library.top(newCount):
        card.moveTo(card.owner.hand)

def draw(group, x = 0, y = 0):
    mute()
    if len(group) == 0:
        return
    card = group[0]
    card.moveTo(card.owner.hand)
    rnd(10,100)
    if re.search(r'Miracle ', card.Rules):
        if confirm("Cast this card for its Miracle cost?\n\n{}\n{}".format(card.Name, card.Rules)):
            if autoscriptCheck() == "True":
                text = autoParser(card, 'miracle')
                card.highlight = MiracleColor
                cardalign()
            else:
                miracletrig = card
                miracletrig.moveToTable(defaultX, defaultY)
                text = ""
            notify("{} draws a miracle {}{}.".format(me, card, text))
            return
    notify("{} draws a card.".format(me))

def drawMany(group, x = 0, y = 0):
    if len(group) == 0:
        return
    mute()
    count = askInteger("Draw how many cards?", 7)
    if count == None:
        return
    for card in group.top(count):
        card.moveTo(card.owner.hand)
    notify("{} draws {} cards.".format(me, count))

def mill(group, x = 0, y = 0):
    if len(group) == 0:
        return
    mute()
    count = askInteger("Mill how many cards?", 1)
    if count == None:
        return
    for card in group.top(count):
        card.moveTo(card.owner.Graveyard)
    notify("{} mills top {} cards from Library.".format(me, count))

def exileMany(group, x = 0, y = 0):
    if len(group) == 0:
        return
    mute()
    count = askInteger("Exile how many cards?", 1)
    if count == None:
        return
    for card in group.top(count):
        card.moveTo(card.owner.piles['Exiled Zone'])
    notify("{} exiles top {} cards from Library.".format(me, count))

def revealtoplibrary(group, x = 0, y = 0):
    mute()
    if group[0].isFaceUp:
        notify("{} hides {} from top of Library.".format(me, group[0]))
        group[0].isFaceUp = False
    else:
        group[0].isFaceUp = True
        notify("{} reveals {} from top of Library.".format(me, group[0]))

def exileAll(group, x = 0, y = 0):
    mute()
    for card in group:
        card.moveTo(card.owner.piles['Exiled Zone'])
    notify("{} exiles all cards from {}.".format(me, group.name))

def graveyardAll(group, x = 0, y = 0):
    mute()
    for card in group:
        card.moveTo(card.owner.piles['Graveyard'])
    notify("{} moves all cards from their {} to Graveyard.".format(me, group.name))

def libraryTopAll(group, x = 0, y = 0):
    mute()
    for card in group:
        card.moveTo(card.owner.piles['Library'])
    notify("{} moves all cards from their {} to top of Library.".format(me, group.name))

def libraryBottomAll(group, x = 0, y = 0):
    mute()
    for card in group:
        card.moveToBottom(card.owner.piles['Library'])
    notify("{} moves all cards from their {} to bottom of Library.".format(me, group.name))

#-------------------------------------------------------------
# Misc. Functions
#-------------------------------------------------------------

def shuffle(group, x = 0, y = 0, silence = False):
    mute()
    for card in group:
        if card.isFaceUp:
            card.isFaceUp = False
    group.shuffle()
    if silence == False:
        notify("{} shuffled their {}".format(me, group.name))