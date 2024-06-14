# -*- coding: utf-8 -*-
import re
import time
import clr
from System import Convert
from System import Text

#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------

AttackColor = "#ff0000"
BlockColor = "#00ff00"
DoesntUntapColor = "#000000"
AutoscriptColor = "#0000ff"
AttackDoesntUntapColor = "#660000"
BlockDoesntUntapColor = "#007700"
MiracleColor = "#1D7CF2"

defaultX = 30
defaultY = 25

diesides = 20

playerside = None
sideflip = None
offlinedisable = False
savedtags = { }
alignIgnore = []

stackDict = {} ## Needs to move to a global variable for game reconnects

#---------------------------------------------------------------------------
# Event Stuff
#---------------------------------------------------------------------------

def registerPlayer(args): #this function triggers off loading a deck, and registers the player as active
    mute()
    player = args.player
    if player == me: #only process the local player
        playersDict = eval(getGlobalVariable('activePlayers')) #the activePlayers variable just keeps track of the active players in the game
        playersDict[me._id] = autoscriptCheck() #keeps track of who's allergic to fun
        setGlobalVariable('activePlayers', str(playersDict))

def priorityResolve(args):
    mute()
    name = args.name
    value = args.value
    if name == 'priority' and value == '[]':
        stack = [c for c in table
                if isStack(c)]
        if len(stack) == 0:
            return
        if stack[-1].controller == me and autoscriptCheck():
            resolve(stack[-1])

def endTurn(args):
    mute()
    player = args.player
    if player == me:
        clearAll(table, x = 0, y = 0)

def moveEvent(args):
    global alignIgnore
    for i in range(len(args.cards)):
        card = args.cards[i]
        ## Moving a card will automatically disable it from alignment
        if anchorCheck() and card.group == table and args.toGroups[i] == table and not card in alignIgnore: 
            alignIgnore.append(card)  ## anchors the card to the table
        ## if it's gotten this far, proceed to default movement action
        if args.toGroups[i] == table:
            card.moveToTable(args.xs[i], args.ys[i], not args.faceups[i])
        else:
            card.moveTo(args.toGroups[i], args.indexs[i])
    cardalign()

def initializeGame():
    mute()
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

def changePhase(args):
    mute()
    phaseIdx = currentPhase()[1]
    if phaseIdx == 1 and me.isActive:
        untapStep(table)
    resetPriority()

#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------

def respond(group, x = 0, y = 0):
    notify('{} RESPONDS!'.format(me))

def passPriority(group, x = 0, y = 0, autoscriptOverride = False):
    priorityList = eval(getGlobalVariable('priority'))
    if me._id in priorityList:
        priorityList.remove(me._id)
        setGlobalVariable('priority', str(priorityList))
    notify('{} passes priority.'.format(me))

def autoPass(group, x = 0, y = 0):
    mute()
    if me.getGlobalVariable("f6") == "False":
        me.setGlobalVariable("f6", "True")
        whisper("You are now auto-passing priority.")
        passPriority(group)
    else:
        me.setGlobalVariable("f6", "False")
        whisper("You turned off auto-pass priority.")

def nextPhase(group, x = 0, y = 0):
    mute()
    phaseIdx = currentPhase()[1]
    if phaseIdx == 11:
        setPhase(0)
    else:
        setPhase(phaseIdx + 1)

def untapStep(group, x = 0, y = 0):
    mute()
    myCards = (card for card in table if card.controller == me)
    for card in myCards:
        if card.highlight == DoesntUntapColor:
            card.markers[counters['exert']] = 0
        elif card.highlight == AttackDoesntUntapColor or card.highlight == BlockDoesntUntapColor:
            card.highlight = DoesntUntapColor
            card.markers[counters['exert']] = 0
        elif card.markers[counters['exert']] > 0:
            card.markers[counters['exert']] = 0
        else:
            card.orientation &= ~Rot90
            card.highlight = None
    notify("{} untaps their permanents.".format(me))
    cardalign()

def goToUpkeep(group, x = 0, y = 0):
    untapStep(group)
    setPhase(2)

def goToFirstMain(group, x = 0, y = 0):
    setPhase(4)

def goToCombat(group, x = 0, y = 0):
    setPhase(5)

def goToSecondMain(group, x = 0, y = 0):
    setPhase(10)

def goToEnding(group, x = 0, y = 0):
    setPhase(11)

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
    me.experience = 0
    me.energy = 0
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
    setGlobalVariable("cattach", "{ }")
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
    cardalign()

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
    guid, quantity = askCard({"Rarity":"Token"}, "And")
    if quantity == 0:
        return
    token = table.create(guid, x, y, quantity)
    if quantity == 1:
        token = [token]
    artDict = eval(getSetting('tokenArts', convertToString({})))
    for x in token:
        x.alternate = artDict.get(guid, '')

def changeLog(group, x = 0, y = 0):
    mute()
    allLog = sorted(changelog, reverse = True)  ##sorts the changelog so the most recent entries appear first.
    count = 1
    while count != 0:
        stringVersion, date, text = changelog[allLog[count - 1]]
        updates = '\n-'.join(text)
        num = askChoice("What's new in {} ({}):\n-{}".format(stringVersion, date, updates), [], customButtons = ["<- older", "close", "newer ->"])
        if num == 0 or num == -2: ## If the player closes the window
            count = 0
        elif num == -1: ## If the player chooses 'older'
            if len(allLog) > count:
                count += 1
        elif num == -3 and count > 1: ## If the player chooses 'newer'
            count -= 1
    
def decodeSecrets(val):
    mute()
    ret = {}
    for secret in val.split(" ;; "):
        if not secret: continue ## ignore if the secret string is empty
        secretName, secretValue = secret.split(" ; ")
        ret[secretName] = secretValue
    return ret

def encodeSecrets(secretDict):
    mute()
    return " ;; ".join([x[0] + " ; " + x[1] for x in secretDict.items()])

def secrets(group, x = 0, y = 0):
    mute()
    
    secretsList = []
    secretsColors = []
    mySecrets = decodeSecrets(me.getGlobalVariable("secrets"))
    for k, v in mySecrets.items():
        secretsList.append(k)
        if not v: ## if the value is missing or empty
            secretsColors.append("#666666")
        else:
            secretsColors.append("#000077")
    for player in getPlayers():
        if player != me:
            playerSecrets = decodeSecrets(player.getGlobalVariable("secrets"))
            for k,v in playerSecrets.items():
                if k not in mySecrets:
                    secretsList.append(k)
                    secretsColors.append("#666666")

    descriptiveSecrets = []
    for secret in secretsList:
        if secret in mySecrets: ## if the local player has this secret registered
            if not secret: ## if the value is missing or empty
                descriptiveSecrets.append(secret + "\n(missing value)")
            else:  ## if there is a value
                descriptiveSecrets.append(secret + "\nvalue: " + mySecrets[secret])
        else: ## if the local player has not yet registered this secret
            descriptiveSecrets.append(secret + "\n(not yet assigned)")
    mode = askChoice("Secret messages can be recorded and later revealed.\nSelect a secret from the list below to record or reveal a secret's values:", descriptiveSecrets, secretsColors, customButtons = ["Add a new Secret"])
    if mode == 0: return ## cancel the dialog
    elif mode == -1: ## add new secret button
        secretName = None
        askStringText = "Choose a name for this secret:"
        while secretName == None:
            newName = askString(askStringText, "")
            if newName == None: return ## cancels the dialog
            if ';' in newName: ## can't use semicolon because it is used as a delimiter
                askStringText = "ERROR: Cannot use ; key in name.\nChoose a name for this secret:"
                continue
            if newName.lower() in [x.lower() for x in secretsList]:
                askStringText = "ERROR: This name is already in use.\nChoose a name for this secret:"
                continue
            secretName = newName
        askStringText = "Choose a value for '{0}':".format(secretName)
        secretValue = None
        while secretValue == None:
            newValue = askString(askStringText, "")
            if newValue == None: return ## cancels the dialog
            if ';' in newValue: ## can't use semicolon because it is used as a delimiter
                askStringText = "ERROR: Cannot use ; key in name.\nChoose a value for '{0}':".format(secretName)
                continue
            secretValue = newValue
        mySecrets[secretName] = secretValue
        me.setGlobalVariable("secrets", encodeSecrets(mySecrets))
        whisper("You set the '{0}' secret to '{1}'.".format(secretName, secretValue))
    elif mode >= 1: ## Selected one of the existing secrets
        selectedSecret = secretsList[mode - 1]
        mode = askChoice("Choose what you would like to do with the secret '{0}':".format(selectedSecret), ["Register a Value", "Reveal my Secret", "Reveal everyone's Secret"])
        if mode == 0: return ## cancels the dialog
        elif mode == 1: ## register a value
            askStringText = "Choose a value for '{0}':\n(leaving this blank will delete your existing value)".format(selectedSecret)
            secretValue = None
            while secretValue == None:
                newValue = askString(askStringText, mySecrets.get(selectedSecret, ""))
                if newValue == None: return #@ cancels the dialog
                if ';' in newValue:  
                    askStringText = "ERROR: Cannot use ; key in name.\nChoose a value for '{0}':\n(leaving this blank will delete your existing value)".format(selectedSecret), 
                    continue
                secretValue = newValue
            if not secretValue: ## if the string was blank, remove it
                if selectedSecret in mySecrets:
                    del mySecrets[selectedSecret]
                whisper("You deleted your secret value for '{0}'.".format(selectedSecret))
            else:
                mySecrets[selectedSecret] = secretValue
                whisper("You set your '{0}' secret to '{1}'.".format(selectedSecret, secretValue))
            me.setGlobalVariable("secrets", encodeSecrets(mySecrets))
        elif mode == 2: ## reveal my secret
            remoteCall(me, "revealSecret", [selectedSecret])
        elif mode == 3: ## reveal everybody's secret
            for player in getPlayers():
                remoteCall(player, "revealSecret", [selectedSecret])
        
def revealSecret(secretName):
    mute()
    mySecrets = decodeSecrets(me.getGlobalVariable("secrets"))
    if secretName in mySecrets:
        notify("{0} revealed their secret '{1}' as '{2}'.".format(me, secretName, mySecrets[secretName]))


def createDungeon(group, x = 0, y = 0):
    mute()
    guid, quantity = askCard({"Type":"Dungeon"}, "And")
    if quantity == 0:
        return
    token = table.create(guid, x, y, 1)
    notify("{} creates the dungeon {}".format(me, token))

#--------------------------------
# Autoscript-Linked Card functions
#--------------------------------

def scry(group = me.Library, x = 0, y = 0, count = None):
    mute()
    if count == None:
        count = askInteger("Scry how many cards?", 1)
    if count == None or count == 0:
        return
    topCards = []
    for c in group.top(count):
        topCards.append(c)
        c.peek()
    dlg = cardDlg(topCards, [])
    dlg.max = count
    dlg.title = "Scry"
    dlg.label = "Top of Library"
    dlg.bottomLabel = "Bottom of Library"
    dlg.text = "Reorder scryed cards to the top or bottom.\n\n(Close window to cancel scry.)"
    if dlg.show() == None:
        notify("{} has cancelled a scry for {}.".format(me, count))
        return ## closing the dialog window will cancel the scry, not moving any cards, but peek status will stay on to prevent cheating.
    for c in reversed(dlg.list):
        c.moveTo(group)
    for c in dlg.bottomList:
        c.moveToBottom(group)
    notify("{} scryed for {}, {} on top, {} on bottom.".format(me, count, len(dlg.list), len(dlg.bottomList)))
    group.visibility = "none"

def takeFromLibraryTopXShuffleRest(_group = None, _x = None, _y = None, count = None):
    """Allows a player to take card(s) from the top X cards of their library and shuffles the rest to the bottom.
    The taken cards are put into player's hand and can be automatically revealed to opponents, if desired."""
    mute()
    if count == None:
        count = askInteger("Take from how many top cards?", 5)
    if count == None or count == 0:
        return
    dlg = cardDlg(list=[], bottomList=me.Library.top(count))
    dlg.title = "Take card(s) from top {}, shuffle rest to bottom".format(count)
    dlg.label = "To hand"
    dlg.bottomLabel = "To the bottom of library in a random order"
    dlg.text = "Select card(s) to put into your hand. The rest will be put on the bottom of your library in a random order." \
               "You'll be asked if you want to reveal selected cards."
    if dlg.show() is None:
        notify("{} has cancelled taking cards from top {} of their library.".format(me, count))
        return

    if len(dlg.list) > 0:
        shouldReveal = confirm("Do you want to reveal taken cards to all your opponents?")
    else:
        shouldReveal = False
    if shouldReveal is None:
        shouldReveal = False ## If user closes the window, we treat it as if they said "don't reveal".

    if shouldReveal:
        for c in dlg.list:
            c.isFaceUp = True
        cardInfo = ', '.join("{}".format(c) for c in dlg.list)
    else:
        cardInfo = "{} card(s)".format(len(dlg.list))
    notify("{} puts {} from top {} of their library to hand and the rest to the bottom of library in a random order.".format(me, cardInfo, count))
    ## We notify after turning cards face up but before moving them because cards are turned face down again when moved.

    for c in dlg.list:
        c.moveTo(me.Hand)
    libraryBottomAllShuffle(cards=dlg.bottomList, verbose=False)

def play(card, x = 0, y = 0):
    mute()
    text = ''
    if autoscriptCheck():
        src = card.group
        if src == me.hand:
            srcText = ""
        else:
            srcText = " from {}".format(card.group.name)
        ## Deal with Split cards
        if 'splitA' in card.alternates:
            splitRules = [card.alternateProperty('splitA', 'Rules'),
                          card.alternateProperty('splitB', 'Rules')]
            splitFlags = ['A','B']
            ## splitC is the fused split card
            if re.search("Fuse", card.Rules) and src == me.hand:
                splitRules.append('Fuse both sides')
                splitFlags.append('C')
            choice = askChoice('Cast which side of {}?'.format(card.name), splitRules)
            if choice == 0: ## closing the window will cancel the Cast
                return
            stackData = autoCast(card, alt = splitFlags[choice - 1])
        elif 'adventure' in card.alternates and counters['adventure'] not in card.markers:
            choice = askChoice('Casting adventure card:', ["Cast {})".format(card.alternateProperty("", 'Name')), "Cast Adventure ({})".format(card.alternateProperty("adventure", 'Name'))])
            if choice == 0:
                return
            if choice == 2:
                card.alternate = "adventure"
                stackData = autoCast(card)
                stackDict[card]['moveto'] = 'exile'
            else:
                stackData = autoCast(card)
        elif 'modal_dfc' in card.alternates:
            choice = askChoice('Cast which side of {}?'.format(card.name), ["Spell side - {}".format(card.alternateProperty("", "Name")), "Land side - {}".format(card.alternateProperty("modal_dfc", "Name"))])
            if choice == 0:
                return
            if choice == 2:
                card.alternate = "modal_dfc"
            stackData = autoCast(card)
        else:
            stackData = autoCast(card)
        if stackData != "BREAK":
            text += stackData['text']
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
            ## If its a land, automatically resolve it
            if re.search('Land', card.Type):
                resData = autoResolve(card)
                if resData != "BREAK":
                    text += resData['text']
                notify("{} plays {}{}.".format(me, card, text))
                etbData = autoTrigger(card, 'etb', cost = resData['cost'], x = resData['x'])
            else:
                modeTuple = stackDict[card]['mode']
                if modeTuple[0] == 0:
                    notify("{} casts {}{}{}.".format(me, card, srcText, text))
                else:
                    notify("{} casts {} (mode #{}){}{}.".format(me, card, modeTuple[0], srcText, text))
    else:
        src = card.group.name
        if re.search("Instant", card.Type) or re.search("Sorcery", card.Type):
            card.moveTo(card.owner.Graveyard)
        else:
            card.moveToTable(defaultX, defaultY)
        notify("{} plays {} from their {}.".format(me, card, src))
    cardalign()

def playCommander(card, x = 0, y = 0):
    play(card, x, y)
    if card in table:
        card.markers[counters['general']] = 1
        notify("{} makes {} their Commander.".format(me, card))

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

def resolve(card):
    mute()
    global stackDict
    if autoscriptCheck():
        ## double-clicking a suspended card
        if counters['suspend'] in card.markers:
            ## Remove a time counter
            if counters['time'] in card.markers:
                card.markers[counters['time']] -= 1
            ## Check if there's still any time counters left on the card
            if counters['time'] in card.markers:
                notify("{} removed a time counter from suspended {}.".format(me, card))
            else:
                ## Cast the suspended card
                stackData = autoCast(card)
                if stackData != "BREAK":
                    card.markers[counters['suspend']] = 0
                    notify("{} casts suspended {}{}.".format(me, card, stackData['text']))
        ## double-clicking cards on the stack will resolve them
        elif card in stackDict:
            alt = card.alternate
            stackData = autoResolve(card)
            if stackData == "BREAK": return
            if stackData['class'] == 'miracle':
                if stackData['src'] in me.hand:
                    play(stackData['src'])
                else:
                    notify("{}'s {} Miracle trigger is countered (no longer in hand.)".format(me, card))
            else:
                notify("{} resolves {} ({}){}.".format(me, card, stackData['class'], stackData['text']))
            if alt == "adventure":
                card.markers[counters['adventure']] = 1
            if stackData['class'] == 'cast':
                etbData = autoTrigger(stackData['src'], 'etb', cost = stackData['cost'], x = stackData['x'])
        ## double-clicking a card in play just taps it
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
    src = card.group
    if autoscriptCheck() and src == table:
        global stackDict
        if card in stackDict: #Destroying a card on a stack is considered countering that spell
            if stackDict[card]['moveto'] == 'exile':
                card.moveTo(card.owner.piles['Exiled Zone'])
            else:
                card.moveTo(card.owner.Graveyard)
            del stackDict[card]
            notify("{}'s {} was countered.".format(me, card))
        else:
            stackData = autoTrigger(card, 'destroy')
            if stackData != "BREAK":
                card.moveTo(card.owner.Graveyard)
                notify("{} destroys {}{}.".format(me, card, stackData['text']))
    else:
        card.moveTo(card.owner.Graveyard)
        notify("{} destroys {}.".format(me, card))

def discard(card, x = 0, y = 0):
    mute()
    src = card.group
    if autoscriptCheck():
        if src == me.hand:  ## Only run discard scripts if the card is discarded from hand
            card.moveTo(card.owner.Graveyard)
            stackData = autoTrigger(card, 'discard')
            text = ""
            if stackData != "BREAK":
                text = stackData['text']
            notify("{} discards {} from hand{}.".format(me, card, text))
            cardalign()
        else:
            card.moveTo(card.owner.Graveyard)
            notify("{} discards {} from {}.".format(me, card, src))
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
    if autoscriptCheck() and src == table:
        stackData = autoTrigger(card, 'exile')
        if stackData != "BREAK":
            card.moveTo(card.owner.piles['Exiled Zone'])
            notify("{} exiles {}{}.".format(me, card, stackData['text']))
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
    if autoscriptCheck():
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
        stackData = autoTrigger(card, 'attack')
        if stackData != "BREAK":
            notify("{} attacks with {}{}.".format(me, card, stackData['text']))
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
    if autoscriptCheck():
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
        stackData = autoTrigger(card, 'attack')
        if stackData != "BREAK":
            notify("{} attacks without tapping with {}{}.".format(me, card, stackData['text']))
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
    if autoscriptCheck():
        if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
            card.highlight = BlockDoesntUntapColor
        else:
            card.highlight = BlockColor
        stackData = autoTrigger(card, 'block')
        if stackData != "BREAK":
            notify("{} blocks with {}{}.".format(me, card, stackData['text']))
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
    if autoscriptCheck():
        stackData = autoTrigger(card, 'acti')
        if stackData != "BREAK":
            if card.Type == "Dungeon":
                roomName = stackData['acti'][1].split(" — ")[0]
                notify("{} ventures into {}'s {}{}.".format(me, card, roomName, stackData['text']))
            else:
                notify("{} activates {}'s ability #{}{}.".format(me, card, stackData['acti'][0], stackData['text']))
    else:
        notify("{} uses {}'s ability.".format(me, card))

def morph(card, x = 0, y = 0):
    mute()
    if autoscriptCheck():
        card.isFaceUp = False
        stackData = autoCast(card, morph = True)
        notify("{} casts a card face-down.".format(me))
        card.peek()
    else:
        notify("{} casts a card face-down from their {}.".format(me, card.group.name))
        card.moveToTable(defaultX, defaultY, True)
        card.peek()
    cardalign()

def manifest(card, x = 0, y = 0):
    mute()
    if card.group == table:
        notify("{} manifests {} from the battlefield.".format(me, card))
        card.isFaceUp = False
    else:
        if card.index == 0:
            notify("{} manifests the top card of their {}.".format(me, card.group.name))
        else:
            notify("{} manifests the card {} from the top of their {}.".format(me, card.index, card.group.name))
    card.moveToTable(defaultX, defaultY, True)
    card.markers[counters['manifest']] = 1
    card.peek()
    cardalign()

def transform(card, x = 0, y = 0):
    mute()
    if 'transform' in card.alternates:
        notify("{} transforms {}.".format(me, card))
        if card.alternate == '':
            card.alternate = 'transform'
        else:
            card.alternate = ''
    elif 'modal_dfc' in card.alternates:
        notify("{} transforms {}.".format(me, card))
        if card.alternate == '':
            card.alternate = 'modal_dfc'
        else:
            card.alternate = ''
    elif 'meld' in card.alternates:
        notify("{} transforms {}.".format(me, card))
        if card.alternate == '':
            card.alternate = 'meld'
        else:
            card.alternate = ''
    elif 'flip' in card.alternates:
        notify("{} flips {}.".format(me, card))
        if card.alternate == '':
            card.alternate = 'flip'
        else:
            card.alternate = ''
    else:
        if card.isFaceUp == True:
            notify("{} morphs {} face down.".format(me, card))
            card.isFaceUp = False
        else:
            if autoscriptCheck():
                card.peek()
                rnd(1,10)
                card.isFaceUp = True
                stackData = autoTrigger(card, 'morph') ## The card will flip up in the autoParser
                card.markers[counters['manifest']] = 0
                if stackData != "BREAK":
                    notify("{} morphs {} face up{}.".format(me, card, stackData['text']))
            else:
                card.isFaceUp = True
                card.markers[counters['manifest']] = 0
                notify("{} morphs {} face up.".format(me, card))
    cardalign()

def suspend(card, x = 0, y = 0):
    mute()
    num = askInteger("Suspending {}, what is X?)".format(card.Name), 0)
    if num != 0 and num != None:
        card.moveToTable(defaultX, defaultY)
        card.markers[counters['suspend']] = 1
        card.markers[counters['time']] = num
        notify("{} suspends {} for {}.".format(me, card, num))
        cardalign()

def blink(card, x = 0, y = 0):
    mute()
    src = card.group
    if src == table:
        if autoscriptCheck():
            exileData = autoTrigger(card, 'exile')
            if exileData == "BREAK":
                return
            card.moveTo(card.owner.piles['Exiled Zone'])
            card.moveToTable(defaultX, defaultY)
            notify("{} blinks {}.".format(me, card))
        else:
            clear(card)
            notify("{} blinks {}.".format(me, card))
        cardalign()

#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def rulings(card, x = 0, y = 0):
    mute()
    if not card.MultiverseId == None:
        openUrl('http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid={}'.format(card.MultiverseId))

def commanderToggle(card, x = 0, y = 0):
    mute()
    if counters['general'] in card.markers:
        card.markers[counters['general']] = 0
    else:
        card.markers[counters['general']] = 1
        notify("{}  marks  {} as their Commander.".format(me, card))

def exert(card, x = 0, y = 0):
    mute()
    if card.markers[counters['exert']] == 0:
        card.markers[counters['exert']] = 1
        notify("{} exerts {} (will not untap on next upkeep).".format(me, card))

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
        card.markers[counters['manifest']] = 0
        notify("{} flips {} face up.".format(me, card))

def clear(card, x = 0, y = 0):
    notify("{} clears {}.".format(me, card))
    card.highlight = None
    card.target(False)

def clone(cards, x = 0, y = 0):
    for card in cards:
        isInverted = y < card.height / 2
        copy = table.create(card.model, x, y, 1)
        if card.alternate != '':
            copy.alternate = card.alternate
        offset = min(card.width, card.height) / 5
        delta = offset if not isInverted else -offset
        x = x + delta
        y = y + delta

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

def libraryBottomAllShuffle(cards, x = 0, y = 0, verbose = True):
    mute()
    count = len(cards)
    rng = Random()
    for i in range(count - 1, 0, -1):
        ## shuffle pile using fisher-yates algorithm
        j = rng.Next(0, i + 1)
        cards[i], cards[j] = cards[j], cards[i]
    for card in cards:
        card.moveToBottom(card.owner.piles['Library'])
    if verbose:
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
    card.moveTo(card.owner.Graveyard)
    notify("{} randomly discards {}.".format(me, card))

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
    newCount = len(group)
    if newCount < 0:
        return
    if not confirm("Take a Mulligan?"):
        return
    notify("{} mulligans.".format(me))
    for card in group:
        card.moveTo(card.owner.Library)
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
            if autoscriptCheck():
                stackData = autoTrigger(card, 'miracle', forceCreate = True)
                card.highlight = MiracleColor
                notify("{} draws a miracle {}{}.".format(me, card, stackData['text']))
                cardalign()
            else:
                miracletrig = card
                miracletrig.moveToTable(defaultX, defaultY)
                notify("{} draws a miracle {}.".format(me, card))
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

def sideboardAll(group, x = 0, y = 0):
    mute()
    for card in group:
        card.moveTo(card.owner.piles['Sideboard'])
    notify("{} moves all cards from their {} to Sideboard.".format(me, group.name))

def planesTopAll(group, x = 0, y = 0):
    mute()
    for card in group:
        card.moveTo(card.owner.piles['Planes/Schemes'])
    notify("{} moves all cards from their {} to top of Planes/Schemes Deck.".format(me, group.name))

def planesBottomAll(group, x = 0, y = 0):
    mute()
    for card in group:
        card.moveToBottom(card.owner.piles['Planes/Schemes'])
    notify("{} moves all cards from their {} to bottom of Planes/Schemes Deck.".format(me, group.name))  
    
def commandAll(group, x = 0, y = 0):
    mute()
    for card in group:
        card.moveTo(card.owner.piles['Command Zone'])
    notify("{} moves all cards from their {} to Command Zone.".format(me, group.name))
    
#-------------------------------------------------------------
# Misc. Functions
#-------------------------------------------------------------

def loadJumpstart(group, x = 0, y = 0):
    mute()    
    if len(group) > 0:
        if not confirm("WARNING: You are about to load a Jumpstart deck into a library that already contains cards.\r\nContinue?"): return
    deck = []
    for n in [1, 2]:
        choice = askChoice("Choose a Jumpstart set for pack #{}".format(n), ["Jumpstart", "Jumpstart 2022", "Random"])
        if choice == 0 or choice == None:
            return
        if choice == 3:
            choice = rnd(1,2)
        if choice == 1:
            contents = JumpstartDecks.keys()[rnd(0,120)]
            for card in JumpstartDecks[contents]:
                deck.append(card)
        if choice == 2:
            contents = Jumpstart2022Decks.keys()[rnd(0,120)]
            for card in Jumpstart2022Decks[contents]:
                deck.append(card)
    for c in deck:
        group.create(c["id"], c["count"])
    notify("{} loaded a Jumpstart Deck".format(me))

def shuffle(group, x = 0, y = 0, silence = False):
    mute()
    for card in group:
        if card.isFaceUp:
            card.isFaceUp = False
    group.shuffle()
    if silence == False:
        notify("{} shuffled their {}".format(me, group.name))