import re
import time
import clr
from System import Convert
from System import Text

playerside = None
sideflip = None
offlinedisable = False
savedtags = { }

def clearCache(group, x = 0, y = 0):
    if confirm("Reset the Autoscript Tag cache?"):
        global savedtags
        savedtags = { }
        notify("{} reset the global tag cache.".format(me))
    if confirm("Reset the Attachment Dictionary?\nNote: Cards will no longer be attached."):
        setGlobalVariable('cattach', "{ }")
        notify("{} reset the global attachment dictionary.".format(me))

def autoDisable(group, x = 0, y = 0):
    mute()
    if autoscriptCheck() == "True":
        setSetting("autoscripts", "False")
        notify("{} disables autoscripts.".format(me))
        passPriority(group,0,0,True) ## Remove the player from the priority list since they hate autoscripts so much
    else:
        setSetting("autoscripts", "True")
        notify("{} enables autoscripts.".format(me))
    ## Now we have to update the active players to let others know you're a big quitter
    playersDict = eval(getGlobalVariable('activePlayers'))
    if me._id in playersDict:
        playersDict[me._id] = autoscriptCheck()
        setGlobalVariable('activePlayers', str(playersDict))

def autoscriptCheck():
    return getSetting("autoscripts", "True")

def alignDisable(group, x = 0, y = 0):
    mute()
    if alignCheck() == "True":
        setSetting("alignment", "False")
        notify("{} disables alignment.".format(me))
    else:
        setSetting("alignment", "True")
        notify("{} enables alignment.".format(me))

def alignCheck():
    return getSetting("alignment", "True")

def attachDisable(group, x = 0, y = 0):
    mute()
    if attachCheck() == "True":
        setSetting("attachments", "False")
        notify("{} disables attachments.".format(me))
    else:
        setSetting("attachments", "True")
        notify("{} enables attachments.".format(me))

def attachCheck():
    return getSetting("attachments", "True")

def getTags(card, key = None):
    mute()
    global savedtags, offlinedisable
    cardname = card.Name
    encodedcardname = Convert.ToBase64String(Text.Encoding.UTF8.GetBytes(cardname)) #encodes the card name so the website can parse it safely
    if not cardname in savedtags:
#### Create a bunch of identifier tags for the card's rules, so I can sort the tag requests online
        rules = card.Rules
        if re.search(r'creature token', rules):
            encodedcardname += '&token'
        if re.search(r'counter', rules):
            encodedcardname += "&counter"
        if re.search(r'{} enters the battlefield'.format(card.name), rules):
            encodedcardname += '&etb'
        if re.search(r'{} dies'.format(card.name), rules):
            encodedcardname += '&destroy'
        if re.search(r'{} attacks'.format(card.name), rules):
            encodedcardname += '&attack'
        if re.search(r'{} blocks'.format(card.name), rules):
            encodedcardname += '&block'
#### Fetch card tags from the online database
        if offlinedisable == False:
            (fulltag, code) = webRead('http://octgn.gamersjudgement.com/forum/tags2.php?id={}'.format(encodedcardname), 7000)
            if code == 204: ## if the card tag doesn't exist on the site.
                fulltag = ""
            elif code != 200: ## Handles cases where the site is unavailable
                whisper('tag database is currently unavailable, using offline tag cache')
                offlinedisable = True
        if offlinedisable == True: ## Access the tags cache in the game def if the website can't be accessed
                if cardname in offlineTags:
                    fulltag = offlineTags[cardname]
                else:
                    fulltag = ""
#### Parse the raw tags into an autoscripts-readable format
        tagdict = { }
        classpieces = fulltag.split('; ')
        for classes in classpieces:
            if classes != "":
                actionlist = classes.split('.')
                actiondict = { }
                for actionpieces in actionlist[1:]:
                    actionname = actionpieces[:actionpieces.find("[")]
                    actionparam = actionpieces[actionpieces.find("[")+1:actionpieces.find("]")]
                    if actionname == 'token':
                        if not 'autotoken' in tagdict:
                            tagdict['autotoken'] = [ ]
                        tokenname = actionparam[:actionparam.find(",")]
                        if not tokenname in tagdict['autotoken']:
                            tagdict['autotoken'].append(tokenname)
                    if actionname == 'marker':
                        if not 'automarker' in tagdict:
                            tagdict['automarker'] = [ ]
                        markername = actionparam[:actionparam.find(",")]
                        if not markername in tagdict['automarker']:
                            tagdict['automarker'].append(markername)
                    if not actionname in actiondict:
                        actiondict[actionname] = [ ]
                    actiondict[actionname].append(actionparam)
                tagdict[actionlist[0]] = actiondict
        savedtags[cardname] = tagdict
#### Fetch and return the card tags to previous functions
    if key in savedtags[cardname]:
        returnTags = savedtags[cardname][key]
        if returnTags == None:
            return ""
        else:
            return returnTags
    return None

def tagConstructor(card, key, modeModifier = ''):
    mute()
    cattach = eval(getGlobalVariable('cattach'))
    attachments = [k for (k,v) in cattach.iteritems() if v == card._id]
    returnTags = []
    returnActiChoice = (0, '')
    returnModeChoice = (0, '')
#### deal with activated abilities as a specific case
    if key == 'acti':
        count = 0
        rulesList = card.Rules.splitlines()
        tagsList = []
        colorList = []
        for lines in rulesList:
            count += 1
            color = '#545454'
            activateList = []
            for tagPrefix in ['init', '', 'cost', 'initres', 'res', 'costres']:
                tags = getTags(card, modeModifier + tagPrefix + key + str(count))
                if tags != None:
                    color = '#0000ff'
                activateList.append(tags)
            colorList.append(color)
            tagsList.append(activateList)
        for attachment in attachments:
            attachCard = Card(attachment)
            attachRulesList = attachCard.Rules.splitlines()
            attachCount = 0
            for attachLines in attachRulesList:
                attachCount += 1
                color = '#545454'
                activateList = []
                for tagPrefix in ['init', '', 'cost', 'initres', 'res', 'costres']:
                    tags = getTags(attachCard, 'attach' + tagPrefix + key + str(attachCount))
                    if tags != None:
                        color = '#0000ff'
                    activateList.append(tags)
                if color == '#0000ff':
                    colorList.append(color)
                    tagsList.append(activateList)
                    rulesList.append(attachLines)
        actiChoice = askChoice("{}\nActivate which ability?".format(card.Name), rulesList, colorList)
        if actiChoice == 0:
            return "BREAK"
        returnActiChoice = (actiChoice, rulesList[actiChoice - 1])
        returnTags = tagsList[actiChoice - 1]
## deal with regular cards
    else:
        for tagPrefix in ['init', '', 'cost', 'initres', 'res', 'costres']:
            tags = getTags(card, modeModifier + tagPrefix + key)
            for attachment in attachments:
                attachTags = getTags(Card(attachment), 'attach' + tagPrefix + key)
                if attachTags != None:
                    if tags == None:
                        tags = attachTags
                    else:
                        tags += attachTags
            returnTags.append(tags)
### Handle the 'choose one' style abilities
    if returnTags[0] != None and 'choice' in returnTags[0]:
        for choice in returnTags[0]['choice']:
            modeLine, modeType = choice.split(', ')
            modeRule = (card.Rules.splitlines())[int(modeLine) - 1] ## we want just the one rules line with the modes in it
            modesText = modeRule.split(u'\u2014 ')[1] ## parse out the 'choose one - ' part
            modeList = modesText.split("; or ") ## convert the mode options to a proper list
            modeChoice = askChoice("Choose a mode for {}:".format(card.Name), modeList)
            if modeChoice == 0:
                return "BREAK"
            if returnActiChoice != (0, ''):  ## if the mode choice was from an activated ability
                newTags = tagConstructor(card, key + str(returnActiChoice[0]), str(modeChoice))[0]
            else:
                newTags = tagConstructor(card, key, str(modeChoice))[0]
            returnTags[3] = newTags[3]
            returnTags[4] = newTags[4]
            returnTags[5] = newTags[5]
            returnModeChoice = (modeChoice, modeList[modeChoice - 1])
    return (returnTags, returnActiChoice, returnModeChoice)

def submitTags(card, x = 0, y = 0):
    cardname = card.Name
    encodedcardname = Convert.ToBase64String(Text.Encoding.UTF8.GetBytes(cardname))
    (url, code) = webRead('http://octgn.gamersjudgement.com/forum/tags2.php?id={}'.format(encodedcardname))
    if code == 200 or code == 204:
        if code == 200:
            if not confirm("Submit an edit?\n{}".format(url)):
              return
        openUrl('http://octgn.gamersjudgement.com/forum/submit2.php?id={}'.format(encodedcardname))
    else:
        whisper("cannot connect to online database.")

def cardcount(card, stackcard, search):
    multiplier = 1
    if re.search(r'-', search):
        search = search.replace('-', '')
        multiplier = multiplier * (0 - 1)
    if re.search(r'\*', search):
        intval = int(search[:search.find("*")])
        search = search[search.find("*")+1:]
        multiplier = multiplier * intval
    if search == "x":
        qty = stackcard.markers[scriptMarkers['x']]
        stackcard.markers[scriptMarkers['x']] -= qty
    elif search == "cost":
        qty = stackcard.markers[scriptMarkers['cost']]
        stackcard.markers[scriptMarkers['cost']] -= qty
    elif re.search(r'marker', search):
        marker = search[search.find("marker")+7:]
        addmarker = counters[marker]
        qty = card.markers[addmarker]
    elif search == "ask":
        qty = askInteger("What is X?", 0)
        if qty == None:
            qty = 0
    else:
        qty = int(search)
    return qty * multiplier

def passControl(card, player):  ## Remote call for taking control of cards you don't yet control
    mute()
    card.setController(player)

##################################
#Card Functions -- Autoscripted  
##################################

stackDict = {} ## Needs to move to a global variable for game reconnects
costMemory = (0,0)

def autoParser(card, tagclass, morph = False):
    mute()
    text = ''
    global stackDict, costMemory
    if not tagclass == 'etb': ## we don't care about costMemory if its not an ETB trigger.
        costMemory = (0,0)
#####create/fetch the stack instance#####
    if tagclass == 'resolve': ## fetch instance
        stackType = 'res'
        if card in stackDict:
            stackData = stackDict[card]
        else:
            whisper("ERROR: this card was not properly registered in the stackDict")
            return "BREAK"
    else: ## create instance
        stackType = 'trig'
        if card.flags == 'split' and re.search('//', card.name) and tagclass == 'cast':
            splitRules = card.Rules.split('//')
            splitFlags = ['A','B']
            if 'splitC' in card.alternates and card in me.hand:
                splitRules.append('Fuse both sides')
                splitFlags.append('C')
            choice = askChoice('cast which side of {}?'.format(card.name), splitRules)
            if choice == 0:
                return "BREAK"
            tagTuple = tagConstructor(card, tagclass, splitFlags[choice - 1])
            splitAlt = 'split' + splitFlags[choice - 1]
        else:
            splitAlt = card.alternate
            tagTuple = tagConstructor(card, tagclass)
        if tagTuple == "BREAK":
            return "BREAK"
        fullTags, actiTuple, modeTuple = tagTuple
        stackData = {
            'src': card,
            'alt': splitAlt,
            'acti': actiTuple,
            'mode': modeTuple,
            'class': tagclass,
            'inittrig': fullTags[0],
            'trig': fullTags[1],
            'costtrig': fullTags[2],
            'initres': fullTags[3],
            'res': fullTags[4],
            'costres': fullTags[5],
            'cost': costMemory[0],
            'x': costMemory[1],
            'moveto': None
            }
#####Prepare the parser variables#####
    srcCard = stackData['src'] ## identifies the originating card
    stackCard = card
    stackAlt = stackData['alt']
    stackClass = stackData['class']
    initTags = 'init' + stackType
    normTags = stackType
    costTags = 'cost' + stackType
#####Init Checks#####
    if stackData[initTags] != None:
        if 'tapped' in stackData[initTags] and srcCard.orientation == Rot90:
            if not confirm("{} is already tapped!\nContinue?".format(srcCard.Name)):
                return "BREAK"
        if 'untapped' in stackData[initTags] and srcCard.orientation == Rot0:
            if not confirm("{} is already untapped!\nContinue?".format(srcCard.Name)):
                return "BREAK"
        if 'cost' in stackData[initTags]:
            for ctag in stackData[initTags]['cost']:
                (cost, type) = ctag.split(', ')
                if cost == 'x':
                    costMarker = 'x'
                else:
                    costMarker = 'cost'
                if type == "ask":
                    confirmValue = confirm("{}'s {}: Pay additional/alternate cost?".format(srcCard.Name, cost))
                    if confirmValue == None:
                        return "BREAK"
                    if confirmValue:
                        stackData[costMarker] = 1
                        text += ", paying {} cost".format(cost.title())
                elif type == "num":
                    qty = askInteger("{}'s {}: Paying how many times?".format(srcCard.Name, cost), 0)
                    if qty == None:
                        return "BREAK"
                    if qty != 0:
                        stackData[costMarker] = qty
                    if qty == 1:
                        text += ", paying {} once".format(cost.title())
                    else:
                        text += ", paying {} {} times".format(cost.title(), qty)
                else:
                    qty = cardcount(srcCard, stackCard, type)
                    if qty != 0:
                        stackData[costMarker] = qty
        if 'marker' in stackData[initTags]:
            for markerTag in stackData[initTags]['marker']:
                (markerName, qty) = markerTag.split(', ')
                markerCount = srcCard.markers[counters[markerName]]
                if markerCount + cardcount(srcCard, stackCard, qty) < 0:
                    if not confirm("Not enough {} counters to remove!\nContinue?".format(markerName)):
                        return "BREAK"
#### toggle between normal tags and cost tags ####
    if stackData['cost'] > 0:
        tagList = [stackData[initTags], stackData[costTags]]
    else:
        tagList = [stackData[initTags], stackData[normTags]]
#### autoscript functions ####
    moveTo = None  ## We need to delay the autoMoveTo autoscript until the very end
    for tags in tagList:
        if tags != None:
            if 'copy' in tags:
                for tag in tags['copy']:
                    text += autocopy(srcCard, stackCard, tag, stackData)
            if 'clone' in tags:
                for tag in tags['clone']:
                    text += autoclone(srcCard, stackCard, tag)
            if 'persist' in tags:
                for tag in tags['persist']:
                    text += autopersist(srcCard, stackCard, tag)
            if 'undying' in tags:
                for tag in tags['undying']:
                    text += autoundying(srcCard, stackCard, tag)
            if 'attach' in tags:
                for tag in tags['attach']:
                    target = [cards for cards in table if cards.targetedBy]
                    if len(target) == 1:
                        text = ", " + autoattach(srcCard, target[0])
            if 'life' in tags:
                for tag in tags['life']:
                    text += autolife(srcCard, stackCard, tag)
            if 'token' in tags:
                for tag in tags['token']:
                    text += autotoken(srcCard, stackCard, tag)
            if 'marker' in tags:
                for tag in tags['marker']:
                    text += automarker(srcCard, stackCard, tag)
            if 'smartmarker' in tags:
                for tag in tags['smartmarker']:
                    text += autosmartmarker(srcCard, tag)
            if 'highlight' in tags:
                for tag in tags['highlight']:
                    text += autohighlight(srcCard, tag)
            if 'tapped' in tags:
                for tag in tags['tapped']:
                    text += autotapped(srcCard, tag)
            if 'untapped' in tags:
                for tag in tags['untapped']:
                    text += autountapped(srcCard, tag)
            if 'transform' in tags:
                for tag in tags['transform']:
                    text += autotransform(srcCard, tag)
            if 'moveto' in tags:
                for tag in tags['moveto']:
                    moveTo = tag ## multiple moveto's shouldn't happen, but we'll keep overwriting previous ones just in case.
#####Move Card/Create Trigger#####
    ## This covers trigger resolving, for ALL trigger classes ##
    if tagclass == 'resolve': ## Handle all cases where the card is on the stack (resolving)
        stackCard.markers[scriptMarkers[stackClass]] = 0
        stackCard.markers[scriptMarkers['cost']] = 0
        stackCard.markers[scriptMarkers['x']] = 0
        del stackDict[stackCard]
    ## This will cover all trigger initiations and activations ##
    else: ## Handle all cases where the card or ability might need to go on the stack
        if stackClass == 'cast': ## If the card is being cast, move it to the table so the stack markers can be added
            srcCard.moveToTable(defaultX, defaultY, morph)
            stackCard = srcCard
            stackCard.switchTo(stackAlt)
            stackCard.markers[scriptMarkers[stackClass]] = 1
            stackCard.markers[scriptMarkers['acti']] = actiTuple[0]
            stackCard.markers[scriptMarkers['choice']] = modeTuple[0]
            stackCard.markers[scriptMarkers['cost']] = stackData['cost']
            stackCard.markers[scriptMarkers['x']] = stackData['x']
            stackDict[stackCard] = stackData  ## Save the final status of the stack instance
        else: ## All other stack triggers need to be checked if the stack trigger card should be created
            if stackClass == 'morph':
                srcCard.isFaceUp = True ## we need to flip the card now to see it's model/GUID
            if stackClass == 'miracle' or (stackData['cost'] > 0 and stackData['costres'] != None) or (stackData['cost'] == 0 and stackData['res'] != None):
                stackCard = table.create(srcCard.model, 0, 0, 1)
                stackCard.switchTo(stackAlt)
                stackCard.markers[scriptMarkers[stackClass]] = 1
                stackCard.markers[scriptMarkers['acti']] = actiTuple[0]
                stackCard.markers[scriptMarkers['choice']] = modeTuple[0]
                stackCard.markers[scriptMarkers['cost']] = stackData['cost']
                stackCard.markers[scriptMarkers['x']] = stackData['x']
                stackDict[stackCard] = stackData  ## Save the final status of the stack instance
    costMemory = (stackData['cost'], stackData['x']) ## stores the cost values for ETB triggers
    if moveTo and stackData['moveto'] == None: ##stuff like flashback's exiling takes precedence over normal moveto's
        text += automoveto(srcCard, moveTo) #deal with automoveto triggers right at the very end.
    ## Reload the priority list
    priorityList = []
    activePlayers = eval(getGlobalVariable('activePlayers'))
    for playerId in activePlayers:
        p = Player(playerId)
        if p not in getPlayers(): #If the player has left the game, they need to be removed from the dictionary
            del activePlayers[playerId]
            setGlobalVariable('activePlayers', str(activePlayers))
        elif activePlayers[playerId] == True: ## Only select the players who have their autoscripts enabled.
            priorityList.append(playerId)
    setGlobalVariable('priority', str(priorityList))
    if tagclass == 'acti': ##acti needs to return the number of the activated ability
        return (actiTuple[0], text)
    else:
        return text


############################
#Autoscript functions
############################

def autocopy(card, stackcard, tag, stackData):
    mute()
    qty = cardcount(card, stackcard, tag)
    for x in range(0, qty):
        copy = table.create(card.model, 0, 0, 1)
        stackDict[copy] = stackData
        copy.markers[scriptMarkers['cast']] = 1
    if qty == 1:
        return ", copied once"
    else:
        return ", copied {} times".format(qty)

def autoclone(card, stackcard, tag):
    mute()
    qty = cardcount(card, stackcard, tag)
    for x in range(0, qty):
        copy = table.create(card.model, 0, 0, 1)
    if qty == 1:
        return ", cloned once"
    else:
        return ", cloned {} times".format(qty)

def autoattach(card, targetcard):
    mute()
    if isStack(targetcard):
        whisper("WARNING: Cannot attach to cards on the stack.")
        return ""
    cattach = eval(getGlobalVariable('cattach'))
    if targetcard._id in cattach:  ## Catch cases where you try to attach to another attachment
        whisper("WARNING: Cannot attach to other attachments.")
        return ""
    if card._id in dict([(v, k) for k, v in cattach.iteritems()]):  ## Catch cases where the attachment has its own attachments
        whisper("WARNING: Cannot attach cards with attachments to other cards. Detach all cards from {} first.".format(card))
        return ""
    if targetcard._id in cattach and cattach[targetcard._id] == card._id:  ## This may be unnecessary code
        del cattach[targetcard._id]
    cattach[card._id] = targetcard._id
    targetcard.target(False)
    setGlobalVariable('cattach', str(cattach))
    if targetcard.controller != me:  ## Pass control of the attachment to the player who controls the target card.
        card.setController(targetcard.controller)
        remoteCall(targetcard.controller, 'alignAttachments', [targetcard])
    return "attaches {} to {}".format(card, targetcard)

def autodetach(card):
    mute()
    cattach = eval(getGlobalVariable('cattach'))
    card.target(False)
    if card._id in dict([(v, k) for k, v in cattach.iteritems()]):  # if this card has stuff attached to it
        attachments = [k for k, v in cattach.iteritems() if v == card._id]
        for attachment in attachments:
            del cattach[attachment]
            text = "{} detaches {} from {}".format(me, Card(attachment), card)
            attachment = Card(attachment)
            if attachment.owner != attachment.controller:  # return this card to it's controller.
                if attachment.controller == me:
                    attachment.setController(attachment.owner)
                else:
                    remoteCall(attachment.controller, 'passControl', [attachment, attachment.owner])
    elif card._id in cattach:  ## if this card is attached to something
        targetCard = cattach[card._id]
        del cattach[card._id]
        text = "detaches {} from {}".format(card, Card(targetCard))
        if card.owner != card.controller:  # return this card to it's controller.
            if card.controller == me:
                card.setController(card.owner)
            else:
                remoteCall(card.controller, 'passControl', [card, card.owner])
    else: #skip detachment since the card is not involved in attachments
        return ""
    setGlobalVariable('cattach', str(cattach))
    return text

def autopersist(card, stackcard, persist):
    if card.group.name == "Graveyard":
        autoParser(card, 'cast')
        autoParser(card, 'resolve')
        autoParser(card, 'etb')
        card.markers[counters['minusoneminusone']] += 1
        return ", persisting"
    else:
        return ""

def autoundying(card, stackcard, undying):
    if card.group.name == "Graveyard":
        autoParser(card, 'cast')
        autoParser(card, 'resolve')
        autoParser(card, 'etb')
        card.markers[counters['plusoneplusone']] += 1
        return ", undying"
    else:
        return ""

def automoveto(card, pile):
    n = rnd(0, len(card.owner.Library)) #we need to delay scripts here, might as well find n for shuffle
    try:
        pos = int(pile)
        card.moveTo(card.owner.Library, pos)
        if pos == 0:
            text = "top of Library"
        else:
            text = "{} from top of Library".format(pos)
    except:
        if re.search(r'bottom', pile):
            card.moveToBottom(card.owner.Library)
            text = "bottom of library"
        elif re.search(r'shuffle', pile):
            card.moveTo(card.owner.Library, n)
            shuffle(card.owner.Library, silence = True)
            text = "shuffled into Library"
        elif re.search(r'exile', pile):
            text = autoParser(card, 'exile')
            if text == "BREAK":
                return ''
            card.moveTo(card.owner.piles['Exiled Zone'])
            text = "exile" + text
        elif re.search(r'hand', pile):
            text = autoParser(card, 'hand')
            if text == "BREAK":
                return ''
            card.moveTo(card.owner.hand)
            text = "hand" + text
        elif re.search(r'graveyard', pile):
            text = autoParser(card, 'destroy')
            if text == "BREAK":
                return ''
            card.moveTo(card.owner.Graveyard)
            text = "graveyard" + text
        elif re.search(r'stack', pile):
            text = autoParser(card, 'cast')
            if text == "BREAK":
                return ''
            text = "stack" + text
    return ", moving to {}".format(text)

def autolife(card, stackcard, tag):
    qty = cardcount(card, stackcard, tag)
    me.Life += qty
    if qty >= 0:
        return ", {} life".format(qty)
    else:
        return ", {} life".format(qty)

def autotransform(card, tag):
    if tag == "no":
        return ""
    if tag == "ask":
        if not confirm("Transform {}?".format(card.Name)):
            return ""
    if 'transform' in card.alternates:
        if card.alternate == '':
            card.switchTo('transform')
        else:
            card.switchTo()
    else:
        whisper("Oops, transform cards aren't ready yet!")
    return ", transforming to {}".format(card)

def autotoken(card, stackcard, tag):
    splitList = tag.split(', ')
    name = splitList[0]
    qty = splitList[1]
    if len(splitList) > 2: #since the modifiers are optional
        modifiers = splitList[2:]
    else:
        modifiers = []
    quantity = cardcount(card, stackcard, qty)
    if quantity > 0:
        for x in range(0, quantity):
            token = tokenArtSelector(name)
            for modtag in modifiers:
                if modtag == 'attack':
                    token.highlight = AttackColor
                elif modtag == 'tap':
                    token.orientation = Rot90
                elif re.search(r'marker', modtag):
                    (marker, type, qty) = modtag.split('_', 2)
                    token.markers[counters[type]] += cardcount(token, stackcard, qty)
                elif modtag == 'attach':
                    autoattach(card, token)
        cardalign()
        return ", creating {} {}/{} {} {} token{}.".format(quantity, token.Power, token.Toughness, token.Color, token.name, "" if quantity == 1 else "s")
    else:
        return ""

def automarker(card, stackcard, tag):
    (markername, qty) = tag.split(', ')
    quantity = cardcount(card, stackcard, qty)
    originalquantity = quantity
    addmarker = counters[markername]
    while markername == "plusoneplusone" and counters["minusoneminusone"] in card.markers and quantity > 0:
        card.markers[counters["minusoneminusone"]] -= 1
        quantity -= 1
    while markername == "minusoneminusone" and counters["plusoneplusone"] in card.markers and quantity > 0:
        card.markers[counters["plusoneplusone"]] -= 1
        quantity -= 1
    card.markers[addmarker] += quantity
    if originalquantity > 0:
        sign = "+"
    else:
        sign = ""
    return ", {}{} {}{}".format(sign, originalquantity, addmarker[0], "" if quantity == 1 else "s")

def autohighlight(card, color):
    if color == "nountap":
        if card.highlight == AttackColor:
            card.highlight = AttackDoesntUntapColor
        elif card.highlight == BlockColor:
            card.highlight = BlockDoesntUntapColor
        else:
            card.highlight = DoesntUntapColor
        text = "does not untap"
    elif color == "attack":
        if card.highlight == DoesntUntapColor:
            card.highlight = AttackDoesntUntapColor
        else:
            card.highlight = AttackColor
        text = "attacking"
    elif color == "block":
        if card.highlight == DoesntUntapColor:
            card.highlight = BlockDoesntUntapColor
        else:
            card.highlight = BlockColor
        text = "blocking"
    else:
        text = ""
    return ", {}".format(text)

def autotapped(card, tapped):
    card.orientation = Rot90
    return ", tapped"

def autountapped(card, untapped):
    card.orientation = Rot0
    return ", untapped"

def autosmartmarker(card, marker):
    if marker in counters:
        setGlobalVariable("smartmarker", marker)
        notify("{} sets the Smart Counter to {}.".format(me, counters[marker][0]))
    return ""

############################
# Alignment Stuff
############################

def attach(card, x = 0, y = 0):
    mute()
    if autoscriptCheck():
        target = [cards for cards in table if cards.targetedBy]
        if len(target) == 0 or (len(target) == 1 and card in target):
            text = autodetach(card)
        elif len(target) == 1:
            text = autoattach(card, target[0])
        else:
            whisper("Incorrect targets, select up to 1 target.")
            return
        if text == "":
            return
        notify("{} {}.".format(me, text))
        cardalign()
    else:
        whisper("Autoscripts must be enabled to use this feature")

def align(group, x = 0, y = 0):  ## This is for the menu action for alignment.
    mute()
    if cardalign() != "BREAK":  ## Don't show the notify message if cardalign fails
        notify("{} re-aligns his cards on the table".format(me))

def isStack(card):  ## Checks to see if the card is on the stack
    mute()
    if (scriptMarkers['cast'] in card.markers
            or scriptMarkers['acti'] in card.markers
            or scriptMarkers['attack'] in card.markers
            or scriptMarkers['block'] in card.markers
            or scriptMarkers['destroy'] in card.markers
            or scriptMarkers['exile'] in card.markers
            or scriptMarkers['etb'] in card.markers
            or scriptMarkers['cost'] in card.markers
            or scriptMarkers['x'] in card.markers
            or scriptMarkers['discard'] in card.markers
            or scriptMarkers['miracle'] in card.markers
            or scriptMarkers['choice'] in card.markers
            or scriptMarkers['morph'] in card.markers):
        return True
    else:
        return False

def playerSide():  ## Initializes the player's top/bottom side of table variables
    mute()
    global playerside
    if playerside == None:  ## script skips this if playerside has already been determined
        if Table.isTwoSided():
            if me.hasInvertedTable():
                playerside = -1  # inverted (negative) side of the table
            else:
                playerside = 1
        else:  ## If two-sided table is disabled, assume the player is on the normal side.
            playerside = 1
    return playerside

def sideFlip():  ## Initializes the player's left/right side of table variables
    mute()
    global sideflip
    if sideflip == None:    ##Initialize sideflip
        playersort = sorted(getPlayers(), key=lambda player: player._id)    ##makes a sorted players list so its consistent between all players
        playercount = [p for p in playersort if me.hasInvertedTable() == p.hasInvertedTable()]    ##counts the number of players on your side of the table
        if len(playercount) > 2:    ##since alignment only works with a maximum of two players on each side
            whisper("Cannot set sideflip: Too many players on your side of the table.")
            sideflip = 0    ##disables alignment for the rest of the play session
        elif playercount[0] == me:    ##if you're the 'first' player on this side, you go on the positive (right) side
            sideflip = 1
        else:
            sideflip = -1
    return sideflip

def cardalign():
    mute()
    side = playerSide()    ## Stores the Y-axis multiplier to determine which side of the table to align to
    flip = sideFlip()    ## Stores the X-axis multiplier to determine if cards align on the left or right half
    if flip == 0:    ## the 'disabled' state for alignment so the alignment positioning doesn't have to process each time
        return "BREAK"
    if not Table.isTwoSided():  ## the case where two-sided table is disabled
        whisper("Cannot align: Two-sided table is required for card alignment.")
        global sideflip
        sideflip = 0    ## disables alignment for the rest of the play session
        return "BREAK"
    alignQueue = {}
    ## align the stack
    stackcount = 0
    lastCard = None  ## Contains the last card to be aligned, so remoteCall knows which card to tuck the aligned cards behind
    for card in table:
        if isStack(card):  ## check to see if the card is on the stack
            if card.controller == me:  ## It's safe to move your own cards on the stack
                card.moveToTable(0, 10 * stackcount)
                card.setIndex(stackcount)
            else:  ## you must send a remoteCall to the other players to align their stack cards
                position = (card._id, 0, 10 * stackcount, lastCard)
                controller = card.controller
                if controller not in alignQueue:
                    alignQueue[controller] = []
                alignQueue[controller].append(position)
            lastCard = card._id
            stackcount += 1
    ## deal with the remote movements of other player's cards in the alignQueue
    for p in alignQueue:
        if p in getPlayers():
            remoteCall(p, 'remoteAlign', str(alignQueue[p]))
    ## Cleans up and updates the global attachment dict
    cattach = eval(getGlobalVariable('cattach'))    ##converts attachment dict to a real dictionary
    group1 = [cardid for cardid in cattach if Card(cattach[cardid]) not in table]    ##selects attachment cards missing their original targets
    for cardid in group1:
        c = Card(cardid)
        if c.Subtype != None and re.search(r'Aura', c.Subtype):    ##if the attachment is an aura, run the destroy scripts since aura's need targets
            if c.controller == me:
                destroy(c)
            else:
                remoteCall(c.controller, 'destroy', [c])
        del cattach[cardid]    ##cleans up the attachment dict when the targeted card is no longer on the battlefield
    group2 = [cardid for cardid in cattach if Card(cardid) not in table]    ##selects targeted cards whose attachment cards are now missing
    for cardid in group2:
        del cattach[cardid]    ##clean up attachment dict
    if cattach != eval(getGlobalVariable('cattach')): ##checks to see if we changed the attached cards, because Kelly whined that we were updating global variables too often
        setGlobalVariable('cattach', str(cattach))    ##updates the global attachment dictionary with our changes
    ## invert the attachment dict so keys are the target cards
    attachDict = {}
    for attachment in cattach:
        targetCard = cattach[attachment]
        if targetCard not in attachDict: ## Add the key if it doesn't exist
            attachDict[targetCard] = []
        attachDict[targetCard].append(Card(attachment))
    ##determine coordinates for cards
    carddict = { } ## This groups cards based on similar properties
    cardorder = [[],[],[],[],[],[],[],[]]
    attachHeight = [0,0,0,0,0,0,0,0] ## This part counts the total number of attachments on each card in each row, to optimize the vertical spacing between rows
    for card in table:
        if (not counters['general'] in card.markers  ## Cards with General markers ignore alignment
                    and not isStack(card)  ## cards on the stack have already been aligned so ignore them
                    and card.controller == me  ## don't align other player's cards
                    and not card._id in cattach):  ## don't align attachments yet
            dictname = card.Name
            height = 0
            for marker in card.markers:
                dictname += marker[0]
                dictname += str(card.markers[marker])
            if card._id in attachDict:  ## for cards that have stuff attached to them
                dictname += str(card._id)
                height = len(attachDict[card._id])
            if not dictname in carddict:
                carddict[dictname] = []
                if scriptMarkers["suspend"] in card.markers:
                    index = 6
                elif re.search(r"Land", card.Type):
                    index = 3
                elif re.search(r"Planeswalker", card.Type):
                    index = 4
                elif re.search(r"Emblem", card.Type):
                    index = 5
                elif re.search(r"Creature", card.Type) or not card.isFaceUp:
                    index = 0
                elif re.search(r"Artifact", card.Type):
                    index = 1
                elif re.search(r"Enchantment", card.Type):
                    index = 2
                else:
                    index = 7
                cardorder[index].append(dictname)
            if height > attachHeight[index]:  ## Make sure the largest height
                attachHeight[index] = height
            carddict[dictname].append(card)
    xpos = 80
    ypos = 5 + 10*max([attachHeight[0], attachHeight[1], attachHeight[2]])
    allowAlign = alignCheck()
    for cardtype in cardorder:
        if cardorder.index(cardtype) == 3:
            xpos = 80
            ypos += 93 + 10*max([attachHeight[3], attachHeight[4], attachHeight[5]])
        elif cardorder.index(cardtype) == 6:
            xpos = 80
            ypos += 93 + 10*max([attachHeight[6], attachHeight[7]])
        for cardname in cardtype:
            for card in carddict[cardname]:
                if allowAlign:
                    card.moveToTable(flip * xpos, side * ypos + (44*side - 44))
                xpos += 9
                if card._id in attachDict:
                    alignAttachments(card, attachDict[card._id])
            xpos += 70

def alignAttachments(card, attachments = None):  ## Aligns all attachments on the card
    mute()
    side = playerSide()
    if attachments == None:
        cattach = eval(getGlobalVariable('cattach'))
        attachments = [Card(key) for (key,value) in cattach.iteritems() if value == card._id]
    if attachments == []:
        return
    lastCard = card
    x, y = card.position
    count = 1
    if side*y < 0:  ## A position modifier that has to take into account the vertical orientation of the card
        yyy = -1
    else:
        yyy = 1
    for c in attachments:
        if not isStack(c):  ## Ignore attachments that have yet to resolve off the stack
            attachY = y - 9 * yyy * side * count ## the equation to identify the y coordinate of the new card
            c.moveToTable(x, attachY)
            c.setIndex(lastCard.getIndex)
            lastCard = c
            count += 1

def remoteAlign(cards):  ## Remote alignment function for the stack
    mute()
    cards = eval(cards)
    for alignData in cards:
        card, x, y, lastCard = alignData
        card = Card(card)
        if lastCard == None:
            z = 0
        else:
            z = Card(lastCard).getIndex + 1
        card.moveToTable(x, y)
        card.setIndex(z)

############################
#Smart Token/Markers
############################

def autoCreateToken(card, x = 0, y = 0):
    mute()
    text = ""
    tokens = getTags(card, 'autotoken')
    if tokens != "":
        for token in tokens:
            tokencard = tokenArtSelector(token)
            card.moveToTable(x,y)
            x, y = table.offset(x, y)
            text += "{}/{} {} {}, ".format(tokencard.Power, tokencard.Toughness, tokencard.Color, tokencard.Name)
        if autoscriptCheck():
            cardalign()
        notify("{} creates {}.".format(me, text[0:-2]))

def tokenArtSelector(tokenName):
    mute()
    token = table.create(tokenTypes[tokenName][1], 0, 0, 1, persist = False)
    artDict = getSetting('tokenArts', convertToString({}))
    artDict = eval(artDict)
    if token.model in artDict:
        token.switchTo(artDict[token.model])
    return token

def nextTokenArt(card, x = 0, y = 0):
    mute()
    if card.Rarity != 'Token':
        return
    currentArt = card.alternate
    artList = card.alternates
    if currentArt == '':
        artIndex = 0
    else:
        artIndex = int(currentArt)
    artIndex = str(artIndex + 1)
    if not artIndex in artList:
        artIndex = ''
    card.switchTo(artIndex)
    artDict = getSetting('tokenArts', convertToString({}))
    artDict = eval(artDict)
    artDict[card.model] = artIndex
    setSetting('tokenArts', convertToString(artDict))

def autoAddMarker(card, x = 0, y = 0):
    mute()
    text = ""
    markers = getTags(card, 'automarker')
    if markers != None:
        for marker in markers:
            addmarker = counters[marker]
            if marker == "minusoneminusone" and counters["plusoneplusone"] in card.markers:
                card.markers[counters["plusoneplusone"]] -= 1
            elif marker == "plusoneplusone" and counters["minusoneminusone"] in card.markers:
                card.markers[counters["minusoneminusone"]] -= 1
            else:
                card.markers[addmarker] += 1
            text += "one {}, ".format(addmarker[0])
        notify("{} adds {} to {}.".format(me, text[0:-2], card))

def autoRemoveMarker(card, x = 0, y = 0, marker = None):
    mute()
    autoMarkerList = getTags(card, 'automarker') ## check for autoMarkers first
    if autoMarkerList != None: ## getTags returns None if there's no autoMarkers
        for autoMarker in autoMarkerList: ## Since a card may have multiple markers mentioned in its rules text, getTags returns all markers as a List, so we must loop them
            if autoMarker in counters:
                autoMarker = counters[autoMarker]
                if autoMarker in card.markers:
                    marker = autoMarker
    smartMarker = getGlobalVariable("smartmarker") ## check for smartMarkers next (higher priority)
    if smartMarker in counters:
        smartMarker = counters[smartMarker]
        if smartMarker in card.markers:
            marker = smartMarker
    if len(card.markers) == 1: #@ if there's only one marker on the card, it's obvious which one to remove
        for m in card.markers:
            marker = m
    if marker != None: ## It'll be None if none of the previous attempts were able to identify a marker
        card.markers[marker] -= 1
        notify("{} removes 1 {} counter from {}.".format(me, marker[0], card))

def smartMarker(card, x = 0, y = 0):
    mute()
    marker = getGlobalVariable("smartmarker")
    if marker == "":
        whisper("No counters available")
        return
    if marker == "minusoneminusone" and counters["plusoneplusone"] in card.markers:
        card.markers[counters["plusoneplusone"]] -= 1
        notify("{} adds one -1/-1 counter to {}.".format(me, card))
    elif marker == "plusoneplusone" and counters["minusoneminusone"] in card.markers:
        card.markers[counters["minusoneminusone"]] -= 1
        notify("{} adds one -1/-1 counter to {}.".format(me, card))
    else:
        addmarker = counters[marker]
        card.markers[addmarker] += 1
        notify("{} adds one {} to {}.".format(me, addmarker[0], card))
