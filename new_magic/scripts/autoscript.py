#coding: utf-8

import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer

def clearCache(group, x = 0, y = 0):
    if confirm("Reset the Autoscript Tag cache?"):
        global savedtags
        savedtags = { }
        notify("{} reset the global tag cache.".format(me))
    if confirm("Reset the Attachment Dictionary?\nNote: Cards will no longer be attached."):
        setGlobalVariable('cattach', "{ }")
        notify("{} reset the global attachment dictionary.".format(me))

def autoscriptCheck():
    return getSetting("autoscripts", True)

def alignCheck():
    return getSetting("alignment", True)

def anchorCheck():
    return getSetting("anchor", True)

def debugCheck():
    return getSetting("debugTimer", False)

def autoscriptMenu(group, x = 0, y = 0):
    mute()
    options = {1: ("autoscripts", "Autoscripts", autoscriptCheck()),
               2: ("alignment", "Automatic Alignment", alignCheck()),
               3: ("anchor", "Alignment Anchoring", anchorCheck()),
               4: ("debugTimer", "Debug Message", debugCheck()) }
    ret = 1
    while ret > 0:
        names = []
        colors = []
        for x in options:
            names.append(options[x][1])
            colors.append("#666666" if options[x][2] == False else "#000077")
        ret = askChoice("Toggle Automation Settings:", names, colors)
        if ret > 0:
            options[ret] = (options[ret][0], options[ret][1], not options[ret][2])
    if options[1][2] != autoscriptCheck():
        setSetting(options[1][0], options[1][2])
    if options[2][2] != alignCheck():
        setSetting(options[2][0], options[2][2])
        if options[2][0]:
            cardalign()
    if options[3][2] != anchorCheck():
        setSetting(options[4][0], options[3][2])
        if not options[3][2]:
            global alignIgnore
            alignIgnore = []
    if options[4][2] != debugCheck():
        setSetting(options[4][0], options[4][2])

def debugWhisper(text, timer):
    if debugCheck():
        elapsedTime = time.clock() - timer
        whisper("DEBUG({}: {})".format(text, elapsedTime))
    return time.clock()

def getTags(card, key = None):
    mute()
    return None
    #skips the rest of this old code
    timer = time.clock()
    global savedtags, offlinedisable
    cardname = card.Name
    encodedcardname = Convert.ToBase64String(Text.Encoding.UTF8.GetBytes(cardname)) #encodes the card name so the website can parse it safely
    if not cardname in savedtags:
    #### Create a bunch of identifier tags for the card's rules, so I can sort the tag requests online
        rules = card.Rules
        if re.search(r'token', rules):
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
            (fulltag, code) = webRead('http://www.octgngames.com/forum/tags.php?id={}'.format(encodedcardname), 7000)
            if code == 204: ## if the card tag doesn't exist on the site.
                fulltag = ""
            elif code != 200: ## Handles cases where the site is unavailable
                whisper('tag database is currently unavailable, using offline tag cache')
                offlinedisable = True
        if offlinedisable == True: ## Access the tags cache in the game def if the website can't be accessed
                fulltag = offlineTags.get(cardname, "")
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
                    actionparam = [x.strip() for x in actionparam.split(',')]
                    ## add autotoken tags
                    if actionname == 'token':
                        tokenname = actionparam[0]
                        if not 'autotoken' in tagdict:
                            tagdict['autotoken'] = [ ]
                        if not tokenname in tagdict['autotoken']:
                            tagdict['autotoken'].append(tokenname)
                    ## add automarker tags
                    if actionname == 'marker':
                        markername = actionparam[0]
                        if not 'automarker' in tagdict:
                            tagdict['automarker'] = [ ]
                        if not markername in tagdict['automarker']:
                            tagdict['automarker'].append(markername)
                    if not actionname in actiondict:
                        actiondict[actionname] = [ ]
                    actiondict[actionname].append(actionparam)
                tagdict[actionlist[0]] = actiondict
        savedtags[cardname] = tagdict
    debugWhisper("getTags {} {}".format(card, key), timer)
    #### Fetch and return the card tags to previous functions
    if key in savedtags[cardname]:
        returnTags = savedtags[cardname][key]
        if returnTags == None:
            return ""
        else:
            return returnTags
    return None

def tagConstructor(card, key, modeModifier = ''):
    #### this function modifies a card's base tags depending on its particular game-state or modal choices
    mute()
    returnTags = []
    returnActiChoice = (0, '')
    returnModeChoice = (0, '')
    if key != 'morph' and not card.isFaceUp: ## Skip fetching tags for facedown/morph cards
        return ([None, None, None, None, None, None], returnActiChoice, returnModeChoice)
    #### look to see if an attachment is adding effects to the card tag
    cattach = eval(getGlobalVariable('cattach'))
    attachments = [Card(k) for (k,v) in cattach.iteritems() if v == card._id]
    #### activated abilities require a specific case because of cards having more than one potential ability to choose from
    #### this will split apart the card's rules text to predict potential abilities and ask the player to choose one
    if key == 'acti':
        count = 0
        rulesList = card.Rules.splitlines() ## splits up the rules text
        tagsList = []
        colorList = []
        for lines in rulesList:
            count += 1
            color = '#545454'  ## grey, default color for no ability
            activateList = []
            for tagPrefix in ['init', '', 'cost', 'initres', 'res', 'costres']:
                tags = getTags(card, modeModifier + tagPrefix + key + str(count)) ## ('1' + 'init' + 'acti' + '3')
                if tags != None: ## change the color to blue if the card has a autoscript tag for this ability
                    color = '#0000ff'
                activateList.append(tags)
            colorList.append(color)
            tagsList.append(activateList)
        ## check to see if any attachments will grant additional abilities to the card
        for attachment in attachments:
            attachRulesList = attachment.Rules.splitlines()
            attachCount = 0
            for attachLines in attachRulesList:
                attachCount += 1
                color = '#545454'
                activateList = []
                for tagPrefix in ['init', '', 'cost', 'initres', 'res', 'costres']:
                    tags = getTags(attachment, 'attach' + tagPrefix + key + str(attachCount))
                    if tags != None:
                        color = '#0000ff'
                    activateList.append(tags)
                if color == '#0000ff':  ## we need to filter out rules text lines that weren't involved in the granted ability
                    colorList.append(color)
                    tagsList.append(activateList)
                    rulesList.append(attachLines)
        if len(rulesList) == 0:
            return ([None, None, None, None, None, None], (1, ''), returnModeChoice)
        else:
            actiChoice = askChoice("{}\nActivate which ability?".format(card.Name), rulesList, colorList)
            if actiChoice == 0: ## exiting the window
                return "BREAK" ## cancels the autoscript resolution if the player closes the window without selecting a mode
            returnActiChoice = (actiChoice, rulesList[actiChoice - 1])
            returnTags = tagsList[actiChoice - 1]
    else:
        for tagPrefix in ['init', '', 'cost', 'initres', 'res', 'costres']:
            tags = getTags(card, modeModifier + tagPrefix + key)
            for attachment in attachments:
                attachTags = getTags(attachment, 'attach' + tagPrefix + key)
                if attachTags != None:
                    if tags == None:
                        tags = attachTags
                    else:
                        tags += attachTags
            returnTags.append(tags)
    ### Handle the 'choose one' style abilities, these will add the modal tags to the main ones.
    if returnTags[0] != None:
        for choice in returnTags[0].get('choice', []):
            min = int(choice[0])
            max = int(choice[1])
            modeList = [x.split(u'\u2022 ')[1] for x in card.Rules.splitlines() if u"\u2022" in x] ## split the rules text into lines and keep the ones with the modal bullet point
            ## fix out of range issues
            if max > len(modeList):
                max = len(modeList)
            if min > max:
                min = max
            choiceList = []
            while len(choiceList) < int(max):
                if len(choiceList) >= min:
                    choicesRemaining = max - len(choiceList)
                else:
                    choicesRemaining = min - len(choiceList)
                text = "Choose{} {}{} mode{} for {}:".format(
                              " up to" if len(choiceList) >= min else "",
                                  choicesRemaining,
                                   "" if len(choiceList) == 0 else " more",
                                             "s" if choicesRemaining > 1 else "",
                                                    card.Name)
                modeChoice = askChoice(text, modeList, ['#ffaa00' if modeList.index(x) + 1 in choiceList else '#999999' for x in modeList], customButtons = [] if len(choiceList) == 0 else ["OK"] )
                if modeChoice <= 0:
                    if len(choiceList) >= min:
                        break
                    else:
                        continue
                if modeChoice in choiceList:
                    choiceList.remove(modeChoice)
                    continue
                choiceList.append(modeChoice)
            choiceList.sort()
            for mode in choiceList:
                if returnActiChoice != (0, ''):  ## if the mode choice was from an activated ability
                    newTags = tagConstructor(card, key + str(returnActiChoice[0]), str(mode))[0]
                else:
                    newTags = tagConstructor(card, key, str(mode))[0]
                for tagIndex in [1,2,3,4,5]:
                    if returnTags[tagIndex] == None:
                        returnTags[tagIndex] = newTags[tagIndex]
                    else:
                        if newTags[tagIndex] != None:
                            returnTags[tagIndex] += newTags[tagIndex]
            returnModeChoice = (int("".join([str(x) for x in choiceList])), ", ".join([modeList[x - 1] for x in choiceList]))
    return (returnTags, returnActiChoice, returnModeChoice)

def submitTags(card, x = 0, y = 0):
    mute()
    encodedcardname = Convert.ToBase64String(Text.Encoding.UTF8.GetBytes(card.Name))
    (url, code) = webRead('http://www.octgngames.com/forum/tags.php?id={}'.format(encodedcardname))
    if code == 200 or code == 204:
        if code == 200:
            if not confirm("Submit an edit?\n{}".format(url)):
              return
        openUrl('http://www.octgngames.com/forum/submit.php?id={}'.format(encodedcardname))
    else:
        whisper("cannot connect to online database.")

def cardcount(card, stackData, search):
    multiplier = 1
    if re.search(r'-', search):
        search = search.replace('-', '')
        multiplier = multiplier * (0 - 1)
    if re.search(r'\*', search):
        intval = int(search[:search.find("*")])
        search = search[search.find("*")+1:]
        multiplier = multiplier * intval
    if search == "x":
        qty = stackData['x']
    elif search == "cost":
        qty = stackData['cost']
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
    card.controller = player

##################################
#Card Functions -- Autoscripted  
##################################

def autoCast(card, morph = False, alt = ''):
    mute()
    stackData = initializeStackItem(card, 'cast', alt)
    if stackData != "BREAK":
        card.moveToTable(0,0, morph)
        card.alternate = stackData['alt']
        global stackDict
        stackDict[card] = stackData
        addStackMarkers(card)
        resetPriority()
    return stackData

def autoTrigger(card, tagClass, forceCreate = False, cost = 0, x = 0):
    mute()
    stackData = initializeStackItem(card, tagClass, cost = cost, x = x)
    if stackData == "BREAK":
        return "BREAK"
    if (forceCreate == True or stackData['initres'] != None
                           or (stackData['cost'] > 0 and stackData['costres'] != None)
                           or (stackData['cost'] == 0 and stackData['res'] != None)
                           or (tagClass == "acti" and stackData['inittrig'] == None 
                                                  and stackData['trig'] == None
                                                  and stackData['costtrig'] == None
                                                  and stackData['initres'] == None
                                                  and stackData['res'] == None
                                                  and stackData['costres'] == None)):
        global stackDict
        stackCard = table.create(stackData['src'].model, 0, 0)
        stackCard.alternate = stackData['src'].alternate
        stackDict[stackCard] = stackData
        addStackMarkers(stackCard)
        resetPriority()
    return stackData

def autoResolve(card):
    mute()
    stackData = stackDict[card]
    stackData['text'] = ''
    stackData = checkCosts(card, stackData)
    if stackData == "BREAK":
        return "BREAK"
    parseScripts(card, stackData)
    card.markers[scriptMarkers[stackData['class']]] = 0
    card.markers[counters['cost']] = 0
    card.markers[counters['x']] = 0
    del stackDict[card]
    if stackData['class'] != 'cast':
        card.moveTo(me.Graveyard) ## removes copied stack items (non-cast triggers)
    elif card.isFaceUp and card in table and (re.search('Instant', card.Type) or re.search('Sorcery', card.Type)):
        card.moveTo(card.owner.Graveyard)   #instants/sorceries go to graveyard once resolved, unless already in another zone
    resetPriority()
    return stackData

def initializeStackItem(card, tagClass, alt = '', cost = 0, x = 0):
    mute()
    tagTuple = tagConstructor(card, tagClass, alt)
    if tagTuple == "BREAK":
        return "BREAK"
    if alt == '':
        splitAlt = card.alternate
    else:
        splitAlt = 'split' + alt
    ## stores all the relevant data for the card on the stack
    stackData = {
        'src': card,
        'alt': splitAlt,
        'acti': tagTuple[1],
        'mode': tagTuple[2],
        'class': tagClass,
        'type': 'trig',
        'inittrig': tagTuple[0][0],
        'trig': tagTuple[0][1],
        'costtrig': tagTuple[0][2],
        'initres': tagTuple[0][3],
        'res': tagTuple[0][4],
        'costres': tagTuple[0][5],
        'cost': cost,
        'x': x,
        'text': '',
        'moveto': None
        }
    stackData = checkCosts(card, stackData)
    if stackData == "BREAK":
        return "BREAK"
    parseScripts(card, stackData)
    stackData['type'] = 'res'
    return stackData

def addStackMarkers(card):
    mute()
    stackData = stackDict[card]
    card.markers[scriptMarkers[stackData['class']]] = 1
    card.markers[scriptMarkers['acti']] = stackData['acti'][0]
    card.markers[counters['choice']] = stackData['mode'][0]
    card.markers[counters['cost']] = stackData['cost']
    card.markers[counters['x']] = stackData['x']

def checkCosts(card, stackData):
    mute()
    stackType = 'init' + stackData['type']
    if stackData.get(stackType):
        if stackData['class'] == 'acti': ## checks src of activate tag
            for src in stackData[stackType].get('src', ['table']):
                if card.group.name.lower() not in src:
                    return "BREAK"
        if stackData[stackType].get('tapped') and stackData['src'].orientation == Rot90:
            if not confirm("{} is already tapped!\nContinue?".format(stackData['src'].Name)):
                return "BREAK"
        if stackData[stackType].get('untapped') and stackData['src'].orientation == Rot0:
            if not confirm("{} is already untapped!\nContinue?".format(stackData['src'].Name)):
                return "BREAK"
        for (cost, type) in stackData[stackType].get('cost', []):
            if cost == 'tribute' and len(getPlayers()) > 1:
                otherPlayers = getPlayers()[1:]
                if len(otherPlayers) > 1:
                    tributeChoice = askChoice("Choose a player to pay tribute:\n(Check chat log for opponent's decision)", [p.name for p in otherPlayers])
                    tributePlayer = otherPlayers[tributeChoice - 1]
                else:
                    tributePlayer = otherPlayers[0]
                remoteCall(tributePlayer, 'autotribute', [stackData['src']])
            costMarker = 'x' if cost == 'x' else 'cost'
            if type == "ask":
                confirmValue = confirm("{}'s {}: Pay additional/alternate cost?".format(stackData['src'].Name, cost))
                if confirmValue == None:
                    return "BREAK"
                elif confirmValue == True:
                    stackData[costMarker] = 1
                    stackData['text'] += ", paying {} cost".format(cost.title())
                else:
                    stackData[costMarker] = 0
            elif type == "num":
                qty = askInteger("{}'s {}: Paying how many times?".format(stackData['src'].Name, cost), 0)
                if qty == None:
                    return "BREAK"
                elif qty != 0:
                    stackData[costMarker] = qty
                if qty == 1:
                    stackData['text'] += ", paying {} once".format(cost.title())
                else:
                    stackData['text'] += ", paying {} {} times".format(cost.title(), qty)
            else:
                qty = cardcount(stackData['src'], stackData, type)
                if qty != 0:
                    stackData[costMarker] = qty
        for splitList in stackData[stackType].get('marker', []):
            markerName = splitList[0]
            if len(splitList) > 1:
                qty = splitList[1]
            else:
                qty = 1
            markerCount = stackData['src'].markers[counters[markerName]]
            if markerCount + cardcount(stackData['src'], stackData, qty) < 0:
                if not confirm("Not enough {} counters to remove!\nContinue?".format(markerName)):
                    return "BREAK"
        for splitList in stackData[stackType].get('counter', []):
            counterName = splitList[0]
            if len(splitList) > 1:
                qty = cardcount(stackData['src'], stackData, splitList[1])
            else:
                qty = 1
            if qty != 0 and me.counters[counterName].value + qty < 0:
                if not confirm("Not enough {} to reduce!\nContinue?".format(counterName)):
                    return "BREAK"
    return stackData

def parseScripts(card, stackData):
    mute()
    #### toggle between normal tags and cost tags ####
    type = stackData['type']
    if stackData['cost'] > 0:
        tagList = [stackData['init' + type], stackData['cost' + type]]
    else:
        tagList = [stackData['init' + type], stackData[type]]
     #### autoscript functions ####
    moveTo = None  ## We need to delay the autoMoveTo autoscript until the very end
    for tags in tagList:
        if tags != None:
            for tag in tags.get('copy', []):
                stackData['text'] += autocopy(stackData['src'], stackData, tag[0])
            for tag in tags.get('clone', []):
                stackData['text'] += autoclone(stackData['src'], stackData, tag[0])
            for tag in tags.get('persist', []):
                stackData['text'] += autopersist(stackData['src'])
            for tag in tags.get('undying', []):
                stackData['text'] += autoundying(stackData['src'])
            for tag in tags.get('attach', []):
                target = [cards for cards in table if cards.targetedBy]
                if len(target) == 1:
                    stackData['text'] = ", " + autoattach(stackData['src'], target[0])
            for tag in tags.get('counter', []):
                stackData['text'] += autocounter(stackData['src'], stackData, tag)
            for tag in tags.get('token', []):
                stackData['text'] += autotoken(stackData['src'], stackData, tag)
            for tag in tags.get('marker', []):
                stackData['text'] += automarker(stackData['src'], stackData, tag)
            for tag in tags.get('smartmarker', []):
                stackData['text'] += autosmartmarker(stackData['src'], tag[0])
            for tag in tags.get('highlight', []):
                stackData['text'] += autohighlight(stackData['src'], tag[0])
            for tag in tags.get('tapped', []):
                stackData['text'] += autotapped(stackData['src'])
            for tag in tags.get('untapped', []):
                stackData['text'] += autountapped(stackData['src'])
            for tag in tags.get('transform', []):
                stackData['text'] += autotransform(stackData['src'], tag[0])
            for tag in tags.get('moveto', []):
                moveTo = tag[0] ## multiple moveto's shouldn't happen, but we'll keep overwriting previous ones just in case.
    if stackData['moveto'] != None:
        moveTo = stackData['moveto'] ##stuff like flashback's exiling takes precedence over normal moveto's
    if moveTo:
        stackData['text'] += automoveto(stackData['src'], moveTo) #deal with automoveto triggers right at the very end.
                
def resetPriority():
    mute()
    priorityList = [] ## lists the players who still have priority
    for player in getPlayers():
        if player.getGlobalVariable("f6") == "False":
            priorityList.append(player._id)
        else:
            notify('{} auto-passes priority.'.format(player))
    setGlobalVariable("priority", str(priorityList))

############################
#Autoscript functions
############################

def autotribute(card):
    mute()
    if confirm("Would you like to pay {}'s Tribute?\n\n{}".format(card.name, card.rules)):
        notify("{} pays {}'s tribute.".format(me, card))
    else:
        notify("{} does not pay {}'s tribute.".format(me, card))

def autocopy(card, stackData, tag):
    mute()
    global stackDict
    qty = cardcount(card, stackData, tag)
    for x in range(0, qty):
        copy = table.create(card.model, 0, 0, 1)
        stackDict[copy] = dict(stackData)
        stackDict[copy]['type'] = 'res'
        addStackMarkers(copy)
    if qty == 1:
        return ", copied once"
    else:
        return ", copied {} times".format(qty)

def autoclone(card, stackData, tag):
    mute()
    qty = cardcount(card, stackData, tag)
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
        card.controller = targetcard.controller
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
                    attachment.controller = attachment.owner
                else:
                    remoteCall(attachment.controller, 'passControl', [attachment, attachment.owner])
    elif card._id in cattach:  ## if this card is attached to something
        targetCard = cattach[card._id]
        del cattach[card._id]
        text = "detaches {} from {}".format(card, Card(targetCard))
        if card.owner != card.controller:  # return this card to it's controller.
            if card.controller == me:
                card.controller = card.owner
            else:
                remoteCall(card.controller, 'passControl', [card, card.owner])
    else: #skip detachment since the card is not involved in attachments
        return ""
    setGlobalVariable('cattach', str(cattach))
    return text

def autopersist(card):
    if card.group.name == "Graveyard":
        stackData = autoCast(card)
        resolveData = autoResolve(card)
        etbData = autoTrigger(card, 'etb', cost = resolveData['cost'], x = resolveData['x'])
        card.markers[counters['m1m1']] += 1
        return ", persisting"
    else:
        return ""

def autoundying(card):
    if card.group.name == "Graveyard":
        stackData = autoCast(card)
        resolveData = autoResolve(card)
        etbData = autoTrigger(card, 'etb', cost = resolveData['cost'], x = resolveData['x'])
        card.markers[counters['p1p1']] += 1
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
            stackData = autoTrigger(card, 'exile')
            if stackData == "BREAK":
                return ''
            card.moveTo(card.owner.piles['Exiled Zone'])
            text = "exile" + stackData['text']
        elif re.search(r'hand', pile):
            stackData = autoTrigger(card, 'hand')
            if stackData == "BREAK":
                return ''
            card.moveTo(card.owner.hand)
            text = "hand" + stackData['text']
        elif re.search(r'graveyard', pile):
            stackData = autoTrigger(card, 'destroy')
            if stackData == "BREAK":
                return ''
            card.moveTo(card.owner.Graveyard)
            text = "graveyard" + stackData['text']
        elif re.search(r'stack', pile):
            stackData = autoCast(card)
            if stackData == "BREAK":
                return ''
            text = "stack" + stackData['text']
        elif re.search(r'table', pile):
            text = 'battlefield'
            alternate = card.alternate
            stackData = autoCast(card)
            if stackData == "BREAK":
                return ''
            text += stackData['text']
            card.alternate = alternate
            resolveData = autoResolve(card)
            if resolveData == "BREAK":
                return ''
            text += resolveData['text']
            etbData = autoTrigger(card, 'etb', cost = resolveData['cost'], x = resolveData['x'])
    return ", moving to {}".format(text)

def autocounter(card, stackData, tag):
    name = tag[0]
    if name not in me.counters:
        return
    if len(tag) > 1:
        qty = tag[1]
    else:
        qty = 1
    quantity = cardcount(card, stackData, qty)
    if quantity == 0: return ""
    me.counters[name].value += quantity
    return ", {} {}".format(quantity, name)

def autotransform(card, tag):
    if tag == "no":
        return ""
    if tag == "ask":
        if not confirm("Transform {}?".format(card.Name)):
            return ""
    if 'transform' in card.alternates:
        if card.alternate == '':
            card.alternate = 'transform'
        else:
            card.alternate = ''
    elif 'meld' in card.alternates:
        if card.alternate == '':
            card.alternate = 'meld'
        else:
            card.alternate = ''
    elif 'modal_dfc' in card.alternates:
        if card.alternate == '':
            card.alternate = 'modal_dfc'
        else:
            card.alternate = ''
    else:
        whisper("Oops, transform cards aren't ready yet!")
    return ", transforming to {}".format(card)

def autotoken(card, stackData, tag):
    name = tag[0]
    if len(tag) > 1:
        qty = tag[1]
    else:
        qty = 1
    if len(tag) > 2: #since the modifiers are optional
        modifiers = tag[2:]
    else:
        modifiers = []
    quantity = cardcount(card, stackData, qty)
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
                    token.markers[counters[type]] += cardcount(token, stackData, qty)
                elif modtag == 'attach':
                    autoattach(card, token)
        return ", creating {} {}/{} {} {} token{}".format(quantity, token.Power, token.Toughness, token.Color, token.name, "" if quantity == 1 else "s")
    else:
        return ""

def automarker(card, stackData, tag):
    markername = tag[0]
    if len(tag) > 1:
        qty = tag[1]
    else:
        qty = 1
    quantity = cardcount(card, stackData, qty)
    originalquantity = int(str(quantity))
    if markername not in counters: ## make sure the marker exists in the dict
        addmarker = (markername, "d9eb829e-55ad-4376-b109-884b0dad3d4b")
    else:
        addmarker = counters[markername]
    while markername == "p1p1" and counters["m1m1"] in card.markers and quantity > 0:
        card.markers[counters["m1m1"]] -= 1
        quantity -= 1
    while markername == "m1m1" and counters["p1p1"] in card.markers and quantity > 0:
        card.markers[counters["p1p1"]] -= 1
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

def autotapped(card):
    card.orientation = Rot90
    return ", tapped"

def autountapped(card):
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

def align(group, x = 0, y = 0):  ## This is the menu groupaction for aligning ALL your cards.
    mute()
    global alignIgnore
    alignIgnore = []  ## forces all cards to realign, even ones previously anchored to the board
    if cardalign(force = True) != "BREAK":  ## Don't show the notify message if cardalign fails
        notify("{} re-aligns his cards on the table".format(me))

def alignCard(cards, x = 0, y = 0):  ##This is the menu cardaction for reactivating alignment on a card
    mute()
    if not alignCheck():
        whisper("Cannot align card: You must enable auto-alignment.")
        return
    global alignIgnore
    for card in cards:
        if card in alignIgnore:
            alignIgnore.remove(card)
    cardalign()

def isStack(card):  ## Checks to see if the card is on the stack
    mute()
    for marker in scriptMarkers.values():
        if marker in card.markers:
            return True
    return False

def playerSide():  ## Initializes the player's top/bottom side of table variables
    mute()
    global playerside
    if playerside == None:  ## script skips this if playerside has already been determined
        if Table.isTwoSided():
            if me.isInverted:
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
        playercount = [p for p in playersort if me.isInverted == p.isInverted]    ##counts the number of players on your side of the table
        if len(playercount) > 2:    ##since alignment only works with a maximum of two players on each side
            whisper("Cannot set sideflip: Too many players on your side of the table.")
            sideflip = 0    ##disables alignment for the rest of the play session
        elif playercount[0] == me:    ##if you're the 'first' player on this side, you go on the positive (right) side
            sideflip = 1
        else:
            sideflip = -1
    return sideflip

def cardalign(force = False):
    mute()
    timer = time.clock()
    if sideFlip() == 0:    ## the 'disabled' state for alignment so the alignment positioning doesn't have to process each time
        return
    if not Table.isTwoSided():  ## the case where two-sided table is disabled
        whisper("Cannot align: Two-sided table is required for card alignment.")
        global sideflip
        sideflip = 0    ## disables alignment for the rest of the play session
        return
    alignQueue = {}
    ## align the stack
    stackcount = 0
    lastCard = None  ## Contains the last card to be aligned, so remoteCall knows which card to tuck the aligned cards behind
    for card in table:
        if isStack(card):  ## check to see if the card is on the stack
            if card.controller == me:  ## It's safe to move your own cards on the stack
                card.moveToTable(0, 10 * stackcount)
                card.index = stackcount
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
    ## cleans up the alignment ignore list
    global alignIgnore
    for x in alignIgnore:
        if x not in table:
            alignIgnore.remove(x)
    ## Cleans up and updates the global attachment dict
    cattach = eval(getGlobalVariable('cattach'))    ##converts attachment dict to a real dictionary
    cattachchanged = False
    auraRemovalQueue = []
    for k,v in cattach.items():
        attachment = Card(k)
        target = Card(v)
        if attachment not in table:
            del cattach[k]
            cattachchanged = True
        elif target not in table:
            if attachment.Subtype and "Aura" in attachment.Subtype:
                auraRemovalQueue.append(attachment)
            del cattach[k]
            cattachchanged = True
    if cattachchanged:
        setGlobalVariable('cattach', str(cattach)) ##updates the global attachment dictionary with our changes
    for aura in auraRemovalQueue:
        if aura.controller == me:
            destroy(aura) ##TODO: Fix looping crash when rancor is destroyed
        else:
            remoteCall(aura.controller, "destroy", [aura])
    ## invert the attachment dict so keys are the target cards
    attachDict = {}
    for attachId in cattach:
        attachment = Card(attachId)
        targetCard = Card(cattach[attachId])
        if attachment in alignIgnore:
            continue
        if targetCard not in attachDict: ## Add the key if it doesn't exist
            attachDict[targetCard] = []
        attachDict[targetCard].append(attachment)
    ##determine coordinates for cards
    carddict = { } ## This groups cards based on similar properties
    cardorder = [[],[],[],[],[],[],[],[]]
    attachHeight = [0,0,0,0,0,0,0,0] ## This part counts the total number of attachments on each card in each row, to optimize the vertical spacing between rows
    for card in sorted([c for c in table], key=lambda c: sideFlip() * c.position[0]):
        if (not counters['general'] in card.markers  ## Cards with General markers ignore alignment
                    and card.anchor == False
                    and not card in alignIgnore
                    and not isStack(card)  ## cards on the stack have already been aligned so ignore them
                    and card.controller == me  ## don't align other player's cards
                    ):  
            if (card._id in cattach):
                continue ## attachments have a special alignment if that mode is enabled
            height = 0
            dictname = card.Name if card.isFaceUp else "Card"
            if card.highlight in [AttackColor, AttackDoesntUntapColor, BlockColor, BlockDoesntUntapColor]:
                dictname += str(card._id) ##uniquely separates any card designated as an attacker or blocker
            for marker in card.markers:
                dictname += marker[0] ## adds the name of the marker
                dictname += str(card.markers[marker]) ## adds the qty of marker
            if card in attachDict:  ## for cards that have stuff attached to them
                dictname += str(card._id)
                height = len(attachDict[card])
            orientationdictname = dictname + str(card.orientation)
            if not orientationdictname in carddict:
                carddict[dictname + "0"] = []
                carddict[dictname + "1"] = []
                carddict[dictname + "2"] = []
                carddict[dictname + "3"] = []
                if not card.isFaceUp:
                    index = 0
                elif counters["suspend"] in card.markers:
                    index = 6
                elif "Planeswalker" in card.Type:
                    index = 4
                elif "Emblem" in card.Type:
                    index = 5
                elif "Creature" in card.Type:
                    index = 0
                elif "Artifact" in card.Type:
                    index = 1
                elif "Enchantment" in card.Type:
                    index = 2
                elif "Land" in card.Type:
                    index = 3
                else:
                    index = 7
                cardorder[index].append(dictname + "0")
                cardorder[index].append(dictname + "1")
                cardorder[index].append(dictname + "2")
                cardorder[index].append(dictname + "3")
            if height > attachHeight[index]:  ## Tracks the largest height in each section
                attachHeight[index] = height
            carddict[orientationdictname].append(card)
    xpos = 80 if playerSide()*sideFlip() == 1 else 25
    ypos = 5 + 10*max([attachHeight[0], attachHeight[1], attachHeight[2]])
    index = 0
    if alignCheck() or force:
        for groupsection in cardorder:
            if index == 3: ## start of second row
                xpos = 80 if playerSide()*sideFlip() == 1 else 25
                ypos += 93 + 10*max([attachHeight[3], attachHeight[4], attachHeight[5]])
            elif index == 6: ## start of third row
                xpos = 80 if playerSide()*sideFlip() == 1 else 25
                ypos += 93 + 10*max([attachHeight[6], attachHeight[7]])
            for cardgroup in groupsection:
                lastCard = None
                for card in carddict[cardgroup]:
                    if playerSide()*sideFlip() == -1 and not lastCard:
                        xpos += 80 if card.orientation == Rot90 else 55
                    newx = sideFlip() * xpos
                    newy = playerSide() * ypos + (44*playerSide() - 44)
                    if card.position != (newx, newy):
                        card.moveToTable(newx, newy)
                    elif lastCard and lastCard.index > card.index:
                        card.index = lastCard.index
                    xpos += 10
                    lastCard = card
                if lastCard and sideFlip()*playerSide() == 1:
                    xpos += 80 if lastCard.orientation == Rot90 else 55
            index += 1
    for card, attachments in attachDict.items():
        alignAttachments(card, attachments)
    debugWhisper("Alignment", timer)

def alignAttachments(card, attachments):  ## Aligns all attachments on the card
    mute()
    if len(attachments) < 1:
        return
    lastCard = card
    x, y = card.position
    count = 1
    if playerSide() * y < 0:  ## A position modifier that has to take into account the vertical orientation of the card
        yyy = -1
    else:
        yyy = 1
    for c in attachments:
        if not isStack(c):  ## Ignore attachments that have yet to resolve off the stack
            attachY = y - 9 * yyy * playerSide() * count ## the equation to identify the y coordinate of the new card
            if c.position != (x, attachY):
                c.moveToTable(x, attachY)
                c.index = lastCard.index
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
            z = Card(lastCard).index + 1
        card.moveToTable(x, y)
        card.index = z

############################
#Smart Token/Markers
############################

CardColors = {"G": "Green", "R": "Red", "W": "White", "U": "Blue", "B": "Black"}

def getSavedTokenData():
    mute()
    ret = {}
    ## repair the string-safe stored token data in the game settings
    tokendata = JavaScriptSerializer().DeserializeObject(getSetting("savedTokens", "{}"))
    for kvpair in tokendata:
        ret[kvpair.Key] = [id for id in kvpair.Value]
    return ret
    
def autoFindToken(card, x = 0, y = 0):
    mute()
    savedTokens = getSavedTokenData()
    if card.name in savedTokens:
        tokenIds = savedTokens[card.name]
    else:
        ## check to see if the rules text mentions tokens
        if "token" and "create" not in card.Rules.lower():
            whisper("{}'s rules text does not mention creating a token.".format(card))
            return
        data = readWebUrl("https://api.scryfall.com/cards/" + card.model)
        if (data == None):
            return
        json = dict(JavaScriptSerializer().DeserializeObject(data))
        if "all_parts" not in json:
            whisper("{}'s data does not include token references.".format(card))
            return
        parts = [p for p in json["all_parts"]
                    if p["object"] == "related_card" 
                    and p["component"] == "token" 
                    and p["name"] != "Copy" 
                    ]
        if len(parts) == 0:
            whisper("{}'s data does not include token references.".format(card))
            return
        tokenIds = []
        for part in parts:
            tokenData = readWebUrl(part["uri"])
            if (tokenData != None):
                tokenJson = dict(JavaScriptSerializer().DeserializeObject(tokenData))
                query = { }
                query["Rarity"] = "token"
                query["Name"] = tokenJson["name"]
                if "power" in tokenJson:
                    query["Power"] = tokenJson["power"]
                if "toughness" in tokenJson:
                    query["Toughness"] = tokenJson["toughness"]               
                if "colors" in tokenJson:
                    jsonColors = tokenJson["colors"]
                    colors = []
                    if len(jsonColors) == 0:
                        colors.append("Colorless")
                    else:
                        if len(jsonColors) > 1:
                            colors.append("Multicolor")
                        for color in jsonColors:
                            colors.append(CardColors[color])                
                    query["Color"] = " ".join(colors)
                
                typeline = tokenJson["type_line"].split(' — ')
                query["Type"] = typeline[0].replace("Token ", "").replace("Token", "")
                if len(typeline) > 1:
                    query["Subtype"] = typeline[1]
                
                if "oracle_text" in tokenJson:
                    if tokenJson["oracle_text"] == "":
                        query["Rules"] = None
                    else:
                        query["Rules"] = tokenJson["oracle_text"]
                
                results = queryCard(query, True)
                ## complex rules text may not be parsed correctly, check to see if the token is already unique by ignoring the rules text completely.  
                if len(results) == 0:
                    if "Rules" in query:
                        del query["Rules"]
                    results = queryCard(query, True)
                ## no tokens found, either there's a typo in the token set data or the token doesn't exist.
                if len(results) == 0:
                    whisper("Cannot identify a token for {}.".format(card))
                ## complex rules text may not be parsed correctly, check keywords instead.
                if len(results) > 1:
                    if "keywords" in tokenJson:
                        keywords = tokenJson["keywords"]
                        for keyword in keywords:
                            query["Rules"] = keyword
                            keywordResult = queryCard(query, False)
                            results = set(results).intersection(keywordResult)
                ## if the script was able to identify a single token
                if len(results) == 1:
                    results = results[0]
                    tokenIds.append(results)
                ## if there's still multiple possible tokens, have the player manually choose one
                else:
                    (results, count) = askCard({"Model": results}, "or", "Multiple possible tokens found!.")
                    if results != None:
                        tokenIds.append(results)
                
        savedTokens[card.name] = tokenIds
        setSetting("savedTokens", str(savedTokens))
    tokencount = 0
    for id in tokenIds:
        token = table.create(id, x + 10*tokencount, y + 10*tokencount, 1)
        tokencount += 1
        notify("{}'s {} created a {} token.".format(me, card, token))
        
def manualAssignToken(card, x = 0, y = 0):
    mute()
    choices = []
    qty = askInteger("How many different tokens does {} make?\nEnter 0 to reset the card's tokens.\n\n{}".format(card.name, card.Rules), 1)
    if qty == None or qty < 0: return
    while len(choices) < qty:
        (choice, dummy) = askCard({"Rarity": "token"}, "and", "Assign token #{} for {}".format(len(choices) + 1, card.name))
        if choice == None:
            return
        choices.append(choice)
    savedTokens = getSavedTokenData()
    if len(choices) == 0:
        if card.name in savedTokens:
            del savedTokens[card.name]
    else:
        savedTokens[card.name] = choices
    setSetting("savedTokens", str(savedTokens))
        
    
def readWebUrl(url, timeout = 5000):
    mute()
    (data, code) = webRead(url, timeout)
    if code == 200:
        return data
    else:
        whisper("ERROR: Could not read URL (error code {})".format(code))

def getSavedTokenArts():
    mute()
    ret = {}
    ## repair the string-safe stored token data in the game settings
    tokendata = JavaScriptSerializer().DeserializeObject(getSetting("tokenArts", "{}"))
    for kvpair in tokendata:
        ret[kvpair.Key] = kvpair.Value
    return ret
    
def tokenArtSelector(tokenName):
    mute()
    token = table.create(tokenTypes[tokenName][1], 0, 0, 1, persist = False)
    artDict = getSavedTokenArts()
    if token.model in artDict:
        token.alternate = artDict[token.model]
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
    card.alternate = artIndex
    artDict = getSavedTokenArts()
    artDict[card.model] = artIndex
    setSetting('tokenArts', str(artDict))

def getSavedMarkerData():
    mute()
    ret = {}
    ## repair the string-safe stored token data in the game settings
    data = JavaScriptSerializer().DeserializeObject(getSetting("savedMarkers", "{}"))
    for kvpair in data:
        ret[kvpair.Key] = [id for id in kvpair.Value]
    return ret

def findMarkers(card):
    mute()
    savedMarkers = getSavedMarkerData()
    if card.name in savedMarkers:
        markers = savedMarkers[card.name]
    else:
        markers = []
        rules = [line.lower() for line in card.rules.splitlines()]
        for line in rules:
            idxs = [n for n in xrange(len(line)) 
                if line.find(" counter on", n) == n
                or line.find(" counter among", n) == n
                or line.find(" counter and", n) == n
                or line.find(" counters on", n) == n
                or line.find(" counters among", n) == n
                or line.find(" counters and", n) == n
                ]
            if len(idxs) == 0: continue
            for index in idxs:
                text = line[:index]
                if any(keyword in text for keyword in ['put', 'distribute', 'with']):
                    marker = text.split(" ")[-1]
                    if marker not in markers:
                        markers.append(marker)
    return markers

def autoAddMarker(card, x = 0, y = 0):
    mute()
    markers = findMarkers(card)
    if len(markers) == 0:
        ## no markers were found
        return
    elif len(markers) > 1:
        ## todo: handle multiple possible markers
        colors = ["#666666" for v in markers]
        while (True):
            choice = askChoice("Multiple possible counters detected, please choose the counters to add.\n\n(Tip: If there are incorrect counters, then select the correct ones and click 'Save Choices' to ignore those options in the future.", markers, colors, ["Save Choices and Continue", "Continue Without Saving"])
            if choice == 0: return
            elif choice > 0:
                if colors[choice - 1] == "#666666":
                    colors[choice - 1] = "#8888FF"
                else:
                    colors[choice - 1] = "#666666"
            else:
                ret = []
                for i in range(len(colors)):
                    if colors[i] == "#8888FF":
                        ret.append(markers[i])
                markers = ret
                if choice == -1:
                    savedMarkers = getSavedMarkerData()
                    savedMarkers[card.name] = markers
                    setSetting("savedMarkers", str(savedMarkers))
                break
    for selectedMarker in markers:
        card.markers[(selectedMarker + " counter" , selectedMarker)] += 1
        notify("{} adds a {} counter to {}.".format(me, selectedMarker, card))

def manualAssignMarker(card, x = 0, y = 0):
    mute()
    savedMarkers = getSavedMarkerData()
    markers = findMarkers(card)
    while (True):
        choice = askChoice("Assign all possible counters for {}.  Click on a counter label to remove it.\n\n{}.".format(card.Name, card.Rules), markers, customButtons = ["New Counter...", "Reset Card", "Confirm and Save"])
        if choice == 0:
            return
        elif choice > 0:
            del markers[choice - 1]
        elif choice == -1:
            newMarker = askString("Enter the name of the counter", "+1/+1")
            markers.append(newMarker)
            continue
        else:
            if choice == -2:
                if card.name in savedMarkers:
                    del savedMarkers[card.name]
                    whisper("Reset saved counter data for {}".format(card))
            else:
                savedMarkers[card.name] = markers
                for m in markers:
                    whisper("Registered {} counters for {}.".format(m, card.name))
            setSetting("savedMarkers", str(savedMarkers))
            break

def smartCopyMarker(card, x = 0, y = 0):
    mute()
    markers = findMarkers(card)
    if len(markers) == 0: return
    marker = markers[0]
    if len(markers) > 1:
        markerClipboard = getGlobalVariable("smartmarker")
        if markerClipboard in markers:
            n = markers.index(markerClipboard) + 1
            marker = markers[n % len(markers)]
    whisper("Copied {} counter to clipboard".format(marker))
    setGlobalVariable("smartmarker", marker)
    
def smartPasteMarker(card, x = 0, y = 0):
    mute()
    markerClipboard = getGlobalVariable("smartmarker")
    if markerClipboard != "":
        card.markers[(markerClipboard + " counter", markerClipboard)] += 1
        notify("{} adds one {} counter to {}.".format(me, markerClipboard, card))