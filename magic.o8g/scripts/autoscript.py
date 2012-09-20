import re
import time
import clr
from System import Convert
from System import Text

playerside = None
sideflip = None
cstack = { }

versioncheck = None
tokencheck = None

def clearCache(group, x = 0, y = 0):
  if confirm("Reset the Autoscript Tag cache?"):
    global savedtags
    savedtags = { }
    notify("{} reset the global tag cache.".format(me))
  if confirm("Reset the Attachment Dictionary?"):
    setGlobalVariable('cattach', "{ }")
    notify("{} reset the global attachment dictionary.".format(me))

def versionCheck():
    global versioncheck
    if versioncheck == None:
      (url, code) = webRead('http://octgn.gamersjudgement.com/OCTGN/game.txt')
      if code != 200:
        whisper("Newest game definition version is unavailable at the moment")
        return
      currentVers = url.split('.')
      installedVers = gameVersion.split('.')
      if len(installedVers) < 3:
        whisper("Your game definition does not follow the correct version conventions.  It is most likely outdated or modified from its official release.")
      elif int(currentVers[0]) > int(installedVers[0]) or int(currentVers[1]) > int(installedVers[1]) or int(currentVers[2]) > int(installedVers[2]):
        notify("{}'s game definition ({}) is out-of!-date!".format(me, gameVersion))
        if confirm("There is a new game definition available! Your version {}. Current version {}.\nClicking yes will open your browser to the location of the most recent version.".format(gameVersion, url)):
          openUrl('http://octgn.gamersjudgement.com/viewtopic.php?f=8&t=195')
      versioncheck = True

def tokenCheck():
  mute()
  global tokencheck
  if tokencheck == None:
    card = table.create('82d6958f-6103-497b-8691-7eb3bf71aa20', 0, 0, 1)

    if card == None:

      notify("{}'s markers & tokens set definition is out-of!-date!".format(me))
      if confirm("Your Markers & Tokens set is not the most recent version! Please download and install the newest version.\nClicking yes will open your browser to the location of the most recent version."):
        openUrl('http://octgn.gamersjudgement.com/viewtopic.php?f=8&t=195')
      tokencheck = False
    else:
      card.moveTo(me.Graveyard)
      tokencheck = True

def shuffle(group, x = 0, y = 0):
    versionCheck()
    tokenCheck()
    for card in group:
      if card.isFaceUp:
        card.isFaceUp = False
    group.shuffle()
    notify("{} shuffled their deck".format(me))

autoscripts = True

def disable(card, x = 0, y = 0):
  mute()
  global autoscripts
  if autoscripts == False:
    autoscripts = True
    notify("{} enables autoscripts".format(me))
  else:
    autoscripts = False
    notify("{} disables autoscripts".format(me))

savedtags = { }

def getTags(card, key):
  mute()
  global savedtags
  if re.search(r"//", card.name) and card.Type != None and not re.search(r"Instant", card.Type) and not re.search(r"Sorcery", card.Type):
    if card.isAlternateImage == True:
      cardname = (card.name)[(card.name).find("/")+3:]
    else:
      cardname = (card.name)[:(card.name).find("/")-1]
  else:
    cardname = card.name
  encodedcardname = Convert.ToBase64String(Text.Encoding.UTF8.GetBytes(cardname))
  if not cardname in savedtags:
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
    (fulltag, code) = webRead('http://octgn.gamersjudgement.com/tags.php?id={}'.format(encodedcardname))
    if code != 200:
      whisper('tag database is currently unavailable.')
      fulltag = tags[cardname]
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
  if key == 'allactivate':
    st = savedtags[cardname]
    if 'initactivate1' in st: text11 = st['initactivate1']
    else: text11 = ''
    if 'activate1' in st: text12 = st['activate1']
    else: text12 = ''
    if 'initactivate2' in st: text21 = st['initactivate2']
    else: text21 = ''
    if 'activate2' in st: text22 = st['activate2']
    else: text22 = ''
    if 'initactivate3' in st: text31 = st['initactivate3']
    else: text31 = ''
    if 'activate3' in st: text32 = st['activate3']
    else: text32 = ''
    if 'initactivate4' in st: text41 = st['initactivate4']
    else: text41 = ''
    if 'activate4' in st: text42 = st['activate4']
    else: text42 = ''
    if 'initactivate5' in st: text51 = st['initactivate5']
    else: text51 = ''
    if 'activate5' in st: text52 = st['activate5']
    else: text52 = ''
    return "1) {}\n  --> {}\n2) {}\n  --> {}\n3) {}\n  --> {}\n4) {}\n  --> {}\n5) {}\n  --> {}".format(text11, text12, text21, text22, text31, text32, text41, text42, text51, text52)
  if key in savedtags[cardname]:
    return savedtags[cardname][key]
  else:
    return ""

def submitTags(card, x = 0, y = 0):
  if re.search(r"//", card.name) and card.Type != None and not re.search(r"Instant", card.Type) and not re.search(r"Sorcery", card.Type):
    if card.isAlternateImage == True:
      cardname = (card.name)[(card.name).find("/")+3:]
    else:
      cardname = (card.name)[:(card.name).find("/")-1]
  else:
    cardname = card.name
  encodedcardname = Convert.ToBase64String(Text.Encoding.UTF8.GetBytes(cardname))
  (url, code) = webRead('http://octgn.gamersjudgement.com/tags.php?id={}'.format(encodedcardname))
  if code == 200:
    if url != "":
      if not confirm("Submit an edit?\n{}".format(url)): return()
    openUrl('http://octgn.gamersjudgement.com/submit.php?id={}'.format(encodedcardname))
  else:
      whisper("cannot connect to online database.")

def transform(card, x = 0, y = 0):
    mute()
    if re.search(r"//", card.name) and card.Type != None and not re.search(r"Instant", card.Type) and not re.search(r"Sorcery", card.Type):
      if re.search(r'DFC', card.Rarity):
        notify("{} transforms {}.".format(me, card))
      else:
        notify("{} flips {}.".format(me, card))
      card.switchImage
    else:
      if card.isFaceUp == True:
        notify("{} morphs {} face down.".format(me, card))
        card.isFaceUp = False
      else:
        card.isFaceUp = True
        notify("{} morphs {} face up.".format(me, card))

def suspend(card, x = 0, y = 0):
  mute()
  num = askInteger("Suspending {}, what is X?\n(To cancel, choose 0.)".format(card.name), 0)
  if num != 0 and num != None:
    card.moveToTable(0,0)
    card.markers[scriptMarkers['suspend']] = 1
    card.markers[counters['time']] = num
    cardalign()
    notify("{} suspends {} for {}.".format(me, card, num))

##################################
#Card Functions -- Autoscripted  
##################################

def trigAbility(card, tagclass, pile):
    mute()
    markerdict = { }
    text = ""
    inittag = getTags(card, 'init{}'.format(tagclass))
####aura attachment####
    if tagclass == 'cast' and card.Subtype != None and re.search(r'Aura', card.Subtype):
      target = (card for card in table if card.targetedBy)
      targetcount = sum(1 for card in table if card.targetedBy)
      if targetcount == 1:
        for targetcard in target:
          while getGlobalVariable('cattach') == 'CHECKOUT':
             whisper("Global card attachment dictionary is currently in use, please wait.")
             return CRASH
          cattach = eval(getGlobalVariable('cattach'))
          setGlobalVariable('cattach', 'CHECKOUT')
          cattach[card._id] = targetcard._id
          targetcard.target(False)
          setGlobalVariable('cattach', str(cattach))
          text += ", targeting {}".format(targetcard)
####init tag checking####
    if 'tapped' in inittag and card.orientation == Rot90:
        if not confirm("{} is already tapped!\nContinue?".format(card.name)): return "BREAK"
    if 'untapped' in inittag and card.orientation == Rot0:
        if not confirm("{} is already untapped!\nContinue?".format(card.name)): return "BREAK"
    if 'cost' in inittag:
        for costtag in inittag['cost']:
            (cost, type) = costtag.split(', ')
            if cost in scriptMarkers:
                marker = cost
            else:
                marker = 'cost'
            if type == "ask":
                if confirm("{}'s {}: Pay additional/alternate cost?".format(card.name, cost)):
                    markerdict[marker] = 1
                    text += ", paying {} cost".format(cost.title())
            elif type == "num":
                qty = askInteger("{}'s {}: Paying how many times?".format(card.name, cost), 0)
                if qty == None: qty = 0
                if qty != 0: markerdict[marker] = qty
                text += ", paying {} {} times".format(cost.title(), qty)
            else:
                qty = cardcount(card, card, type)
                if qty != 0: markerdict[marker] = qty
    if 'marker' in inittag:
        for markertag in inittag['marker']:
            (markername, qty) = markertag.split(', ')
            count = card.markers[counters[markername]]
            if count + cardcount(card, card, qty) < 0:
                if not confirm("Not enough {} counters to remove!\nContinue?".format(markername)): return "BREAK"
####cast moves card to table####
    if tagclass == 'cast':
        card.moveToTable(0,0)
        card.markers[scriptMarkers['cast']] = 1
        for markers in markerdict:
            card.markers[scriptMarkers[markers]] += markerdict[markers]
        if card.Type != None and re.search(r'Land', card.Type):
             text += stackResolve(card, 'resolve')
        cardalign()
        return text
####cost modifier####
    if 'cost' in markerdict:
        trigtype = "cost{}".format(tagclass)
    else:
        trigtype = tagclass
####create the triggered copy####
    if trigtype == 'cycle' or getTags(card, trigtype) != '':
        stackcard = table.create(card.model, 0, 0, 1)
        if card.isAlternateImage == True:
          stackcard.switchImage
        if re.search(r'activate', tagclass):
          stackcard.markers[scriptMarkers['activate']] += int(tagclass[-1])
        else:
            stackcard.markers[scriptMarkers[tagclass]] += 1
        cstack[stackcard] = card
        for markers in markerdict:
            stackcard.markers[scriptMarkers[markers]] += markerdict[markers]
    else:
        stackcard = card
####autoscripts####
    if 'life' in inittag:
      for tag in inittag['life']:
        text += autolife(card, stackcard, tag)
    if 'token' in inittag:
      for tag in inittag['token']:
        text += autotoken(card, stackcard, tag)
    if 'marker' in inittag:
      for tag in inittag['marker']:
        text += automarker(card, stackcard, tag)
    if 'smartmarker' in inittag:
      for tag in inittag['smartmarker']:
        text += autosmartmarker(card, tag)
    if 'highlight' in inittag:
      for tag in inittag['highlight']:
        text += autohighlight(card, tag)
    if 'tapped' in inittag:
      for tag in inittag['tapped']:
        text += autotapped(card, tag)
    if 'untapped' in inittag:
      for tag in inittag['untapped']:
        text += autountapped(card, tag)
    if 'transform' in inittag:
      for tag in inittag['transform']:
        text += autotransform(card, tag)
    if 'moveto' in inittag:
      for tag in inittag['moveto']:
        text += automoveto(card, tag)
    elif pile == "table":
        card.moveToTable(0,0)
    elif pile != '':
        cardowner = card.owner
        card.moveTo(cardowner.piles[pile])
    stackcard.sendToFront()
    cardalign()
    return text

def stackResolve(stackcard, type):
  mute()
  text = ''
  if stackcard in cstack:
    card = cstack[stackcard]
  else:
    card = stackcard
  cost = getTags(stackcard, 'cost{}'.format(type))
  if scriptMarkers['cost'] in stackcard.markers and cost != '':
    resolvetag = cost
  else:
    resolvetag = getTags(stackcard, type)
  if 'persist' in resolvetag:
    for tag in resolvetag['persist']:
      text += autopersist(card, stackcard, tag)
  if 'undying' in resolvetag:
    for tag in resolvetag['undying']:
      text += autoundying(card, stackcard, tag)
  if 'life' in resolvetag:
    for tag in resolvetag['life']:
      text += autolife(card, stackcard, tag)
  if 'token' in resolvetag:
    for tag in resolvetag['token']:
      text += autotoken(card, stackcard, tag)
  if 'marker' in resolvetag:
    for tag in resolvetag['marker']:
      text += automarker(card, stackcard, tag)
  if 'smartmarker' in resolvetag:
    for tag in resolvetag['smartmarker']:
      text += autosmartmarker(card, tag)
  if 'highlight' in resolvetag:
    for tag in resolvetag['highlight']:
      text += autohighlight(card, tag)
  if 'tapped' in resolvetag:
    for tag in resolvetag['tapped']:
      text += autotapped(card, tag)
  if 'untapped' in resolvetag:
    for tag in resolvetag['untapped']:
      text += autountapped(card, tag)
  if 'transform' in resolvetag:
    for tag in resolvetag['transform']:
      text += autotransform(card, tag)
  if 'moveto' in resolvetag:
    for tag in resolvetag['moveto']:
      text += automoveto(card, tag)
  if stackcard in cstack:
      del cstack[stackcard]
  if type == 'miracle':
    if card in me.hand:
      casttext = trigAbility(card, 'cast', 'table')
      text += ", casting{}".format(casttext)
    else:
      text += ", countered"
  if type == 'resolve' and stackcard.Type != None and not re.search(r'Instant', stackcard.Type) and not re.search(r'Sorcery', stackcard.Type):
    if scriptMarkers['cost'] in stackcard.markers and getTags(stackcard, 'costetb') != '':
      newcard = table.create(stackcard.model, 0, 0, 1)
      newcard.markers[scriptMarkers['etb']] += 1
      newcard.markers[scriptMarkers['cost']] += stackcard.markers[scriptMarkers['cost']]
      cstack[newcard] = stackcard
    elif not scriptMarkers['cost'] in stackcard.markers and getTags(stackcard, 'etb') != '':
      newcard = table.create(stackcard.model, 0, 0, 1)
      newcard.markers[scriptMarkers['etb']] += 1
      cstack[newcard] = stackcard
    for marker in scriptMarkers:
      stackcard.markers[scriptMarkers[marker]] = 0
  else:
    stackcard.moveTo(stackcard.owner.Graveyard)
  stackcard.sendToFront()
  cardalign()
  return text

############################
#Modifiers
############################

def attach(card, x = 0, y = 0):
 if autoscripts == True:
  stackAttach(card)
 else:
  whisper("Autoscripts must be enabled to use this feature")

def stackAttach(card):
  mute()
  align = True
  while getGlobalVariable('cattach') == 'CHECKOUT':
    whisper("Global card attachment dictionary is currently in use, please wait.")
    return CRASH
  cattach = eval(getGlobalVariable('cattach'))
  setGlobalVariable('cattach', 'CHECKOUT')
  target = [cards for cards in table if cards.targetedBy]
  if len(target) == 0 or (len(target) == 1 and card in target):
    card.target(False)
    if card._id in dict([(v, k) for k, v in cattach.iteritems()]):
      card2 = [k for k, v in cattach.iteritems() if v == card._id]
      for card3 in card2:
        del cattach[card3]
        notify("{} unattaches {} from {}.".format(me, Card(card3), card))
    elif card._id in cattach:
      card2 = cattach[card._id]
      del cattach[card._id]
      notify("{} unattaches {} from {}.".format(me, card, Card(card2)))
    else:
      align = False
  elif len(target) == 1:
    for targetcard in target:
      cattach[card._id] = targetcard._id
      targetcard.target(False)
      notify("{} attaches {} to {}.".format(me, card, targetcard))
  else:
    whisper("Incorrect targets, select up to 1 target.")
    align = False
  setGlobalVariable('cattach', str(cattach))
  if align == True:
    cardalign()

def align(group, x = 0, y = 0):
  mute()
  if autoscripts == True:
    if cardalign() != "BREAK":
      notify("{} re-aligns his cards on the table".format(me))

def cardalign():
  mute()
  global playerside  ##Stores the Y-axis multiplier to determine which side of the table to align to
  global sideflip  ##Stores the X-axis multiplier to determine if cards align on the left or right half
  if sideflip == 0:  ##the 'disabled' state for alignment so the alignment positioning doesn't have to process each time
    return "BREAK"
  if Table.isTwoSided():
    if playerside == None:  ##script skips this if playerside has already been determined
      if me.hasInvertedTable():
        playerside = -1  #inverted (negative) side of the table
      else:
        playerside = 1
    if sideflip == None:  ##script skips this if sideflip has already beend determined
      playersort = sorted(players, key=lambda player: player._id)  ##makes a sorted players list so its consistent between all players
      playercount = [p for p in playersort if me.hasInvertedTable() == p.hasInvertedTable()]  ##counts the number of players on your side of the table
      if len(playercount) > 2:  ##since alignment only works with a maximum of two players on each side
        whisper("Cannot align: Too many players on your side of the table.")
        sideflip = 0  ##disables alignment for the rest of the play session
        return "BREAK"
      if playercount[0] == me:  ##if you're the 'first' player on this side, you go on the positive (right) side
        sideflip = 1
      else:
        sideflip = -1
  else:  ##the case where two-sided table is disabled
    whisper("Cannot align: Two-sided table is required for card alignment.")
    sideflip = 0  ##disables alignment for the rest of the play session
    return "BREAK"
  while getGlobalVariable('cattach') == 'CHECKOUT':  ##prevents simultaneous manipulation of the attachment dictionary
    whisper("Global card attachment dictionary is currently in use, please wait.")
    return "BREAK"
  cattach = eval(getGlobalVariable('cattach'))  ##converts attachment dict to a real dictionary
  setGlobalVariable('cattach', 'CHECKOUT')  ##checks out the attachment dict to prevent others from simultaneously changing it
  group1 = [cardid for cardid in cattach if Card(cattach[cardid]) not in table]  ##selects attachment cards missing their original targets
  for cardid in group1:
    if Card(cardid).Subtype != None and re.search(r'Aura', Card(cardid).Subtype) and Card(cardid).controller == me:  ##if the attachment is an aura you control
      Card(cardid).moveTo(Card(cardid).owner.Graveyard)  ##destroy the aura
      notify("{}'s {} was destroyed".format(me, Card(cardid)))
    del cattach[cardid]  ##cleans up the attachment dict when the targeted card is no longer on the battlefield
  group2 = [cardid for cardid in cattach if Card(cardid) not in table]  ##selects targeted cards whose attachment cards are now missing
  for cardid in group2:
    del cattach[cardid]  ##clean up attachment dict
  setGlobalVariable('cattach', str(cattach))  ##returns the attachment dict to the global variable and checks it back in
  carddict = { }
  cardorder = [[],[],[],[],[],[],[]]
  attachlist = [ ]
  stackcount = 0
  yshift = [{'Blank1': 0},{'Blank2': 0},{'Blank3': 0}]
  for attachid in cattach:
    targetcard = Card(cattach[attachid])
    if scriptMarkers["suspend"] in targetcard.markers:
      yshift[2][targetcard] = yshift[2].get(targetcard, 0) + 1
    elif re.search(r"Land", targetcard.Type) or re.search(r"Planeswalker", targetcard.Type) or re.search(r"Emblem", targetcard.Type):
      yshift[1][targetcard] = yshift[1].get(targetcard, 0) + 1
    elif re.search(r"Creature", targetcard.Type) or re.search(r"Artifact", targetcard.Type) or re.search(r"Enchantment", targetcard.Type):
      yshift[0][targetcard] = yshift[0].get(targetcard, 0) + 1
    else:
      yshift[2][targetcard] = yshift[2].get(targetcard, 0) + 1
  for shiftdict in yshift:
    yshift[yshift.index(shiftdict)] = max(shiftdict.itervalues())
  for card in table:
    if card.controller == me and not counters['general'] in card.markers:
      if (scriptMarkers['cast'] in card.markers
        or scriptMarkers['activate'] in card.markers
        or scriptMarkers['attack'] in card.markers
        or scriptMarkers['block'] in card.markers
        or scriptMarkers['destroy'] in card.markers
        or scriptMarkers['exile'] in card.markers
        or scriptMarkers['etb'] in card.markers
        or scriptMarkers['cost'] in card.markers
        or scriptMarkers['x'] in card.markers
        or scriptMarkers['cycle'] in card.markers
        or scriptMarkers['miracle'] in card.markers):
          card.moveToTable(0, 10 * stackcount)
          stackcount += 1
      elif not card._id in cattach:
        dictname = card.name
        for marker in card.markers:
          dictname += marker[0]
          dictname += str(card.markers[marker])
        if card._id in dict([(v, k) for k, v in cattach.iteritems()]):
          dictname += str(card._id)
        if not dictname in carddict:
          carddict[dictname] = []
          if scriptMarkers["suspend"] in card.markers: cardorder[6].append(dictname)
          elif re.search(r"Land", card.Type): cardorder[3].append(dictname)
          elif re.search(r"Planeswalker", card.Type): cardorder[4].append(dictname)
          elif re.search(r"Emblem", card.Type): cardorder[5].append(dictname)
          elif re.search(r"Creature", card.Type): cardorder[0].append(dictname)
          elif re.search(r"Artifact", card.Type): cardorder[1].append(dictname)
          elif re.search(r"Enchantment", card.Type): cardorder[2].append(dictname)
          else: cardorder[6].append(dictname)
        carddict[dictname].append(card)
      else:
        attachlist.insert(0, card)
  xpos = 80
  ypos = 5 + 10*yshift[0]
  for cardtype in cardorder:
    if cardorder.index(cardtype) == 3:
      xpos = 80
      ypos += 93 + 10*yshift[1]
    elif cardorder.index(cardtype) == 6:
      xpos = 80
      ypos += 93 + 10*yshift[2]
    for cardname in cardtype:
      for card in carddict[cardname]:
        card.moveToTable(sideflip * xpos, playerside * ypos + (44*playerside - 44))
        xpos += 9
      xpos += 70
  cattachcount = { }
  for card in attachlist:
    origc = cattach[card._id]
    (x, y) = Card(origc).position
    if playerside*y < 0:
      yyy = -1
    else:
      yyy = 1
    if not Card(origc) in cattachcount:
      cattachcount[Card(origc)] = 1
      card.moveToTable(x, y - yyy*playerside*9)
      card.sendToBack()
    else:
      cattachcount[Card(origc)] += 1
      card.moveToTable(x, y - yyy*playerside*cattachcount[Card(origc)]*9)
      card.sendToBack()

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
    card.markers[scriptMarkers['x']] -= qty 
  elif search == "cost":
    qty = stackcard.markers[scriptMarkers['cost']]
    card.markers[scriptMarkers['cost']] -= qty 
  elif re.search(r'marker', search):
    marker = search[search.find("marker")+7:]
    addmarker = counters[marker]
    qty = card.markers[addmarker]
  elif search == "ask":
    qty = askInteger("What is X?", 0)
    if qty == None: qty = 0
  else:
    qty = int(search)
  return qty * multiplier

############################
#Autoscript
############################

def autopersist(card, stackcard, persist):
  if card.group.name == "Graveyard":
    card.moveToTable(0,0)
    stackResolve(card, 'resolve')
    card.markers[counters['minusoneminusone']] += 1
    return ", persisting"
  else:
    return ""

def autoundying(card, stackcard, undying):
  if card.group.name == "Graveyard":
    card.moveToTable(0,0)
    stackResolve(card, 'resolve')
    card.markers[counters['plusoneplusone']] += 1
    return ", undying"
  else:
    return ""

def automoveto(card, pile):
    rnd(100,1000)
    cards = card
    position = re.sub("[^0-9]", "", pile)
    if position != "":
      pos = int(position)
      cards.moveTo(card.owner.Library, pos)
      text = "{} from top of library".format(pos)
    if re.search(r'top', pile):
      cards.moveTo(card.owner.Library)
      text = "top of library"
    elif re.search(r'bottom', pile):
      cards.moveToBottom(card.owner.Library)
      text = "bottom of library"
    elif re.search(r'shuffle', pile):
      librarycount = len(card.owner.Library)
      n = rnd(0, librarycount)
      cards.moveTo(card.owner.Library, n)
      card.owner.Library.shuffle()
      text = "library and shuffled"
    elif re.search(r'exile', pile):
      if trigAbility(card, 'exile', 'Exiled Zone') != "BREAK":
        text = "exile"
    elif re.search(r'hand', pile):
      cards.moveTo(card.owner.hand)
      text = "hand"
    elif re.search(r'graveyard', pile):
      if trigAbility(card, 'destroy', 'Graveyard') != "BREAK":
        text = "graveyard"
    elif re.search(r'stack', pile):
      if trigAbility(card, 'cast', 'table') != "BREAK":
        text = "stack"
    elif re.search(r'table', pile):
      card.moveToTable(0,0)
      stackResolve(card, 'resolve')
      text = "table"
    return ", moving to {}".format(text)

def autolife(card, stackcard, tag):
  qty = cardcount(card, stackcard, tag)
  me.Life += qty
  if qty >= 0:
    return ", {} life".format(qty)
  else:
    return ", {} life".format(qty)

def autotransform(card, tag):
  if tag == "no": return ""
  if tag == "ask":
    if not confirm("Transform {}?".format(card.name)): return ""
  card.switchImage
  return ", transforming to {}".format(card)

def autotoken(card, stackcard, tag):
  tag2 = tag.split(', ')
  name = tag2[0]
  qty = tag2[1]
  if len(tag2) > 2:
    modifiers = tag2[2:]
  else:
    modifiers = ""
  quantity = cardcount(card, stackcard, qty)
  if quantity == 1:
    quant = ""
  else:
    quant = "s"
  if quantity != 0:
    addtoken = tokenTypes[name]
    tokens = table.create(addtoken[1], 0, 0, quantity, persist = False)
    if (quantity == 1 and tokens == None) or (quantity > 1 and len(tokens) == 0):
      confirm("Cannot create {}'s token -- your markers & tokens set definition is missing this token.".format(stackcard.name))
      return ""
    else:
      if quantity == 1:
        tokens = [tokens]
      for token in tokens:
        for modtag in modifiers:
          if modtag == 'attack':
            token.highlight = AttackColor
          elif modtag == 'tap':
            token.orientation = Rot90
          elif re.search(r'marker', modtag):
            (marker, type, quant) = modtag.split('_')
            token.markers[counters[type]] += cardcount(token, stackcard, qty)
      tokentext = "{} {}/{} {} {}".format(quantity, token.Power, token.Toughness, token.Color, token.name)
      cardalign()
      return ", creating {} token{}".format(tokentext, quant)
  else:
    return ""

def automarker(card, stackcard, tag):
  (markername, qty) = tag.split(', ')
  quantity = cardcount(card, stackcard, qty)
  originalquantity = quantity
  if quantity == 1:
    quant = ""
  else:
    quant = "s"
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
  return ", {}{} {}{}".format(sign, originalquantity, addmarker[0], quant)

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
#Smart Token/Markers
############################

def autoCreateToken(card, x = 0, y = 0):
  mute()
  text = ""
  tokens = getTags(card, 'autotoken')
  if tokens != "":
    for token in tokens:
      addtoken = tokenTypes[token]
      tokencard = table.create(addtoken[1], x, y, 1, persist = False)
      if tokencard == None:
        confirm("Cannot create {}'s token -- your markers & tokens set definition is missing this token.".format(card))
        return
      x, y = table.offset(x, y)
      text += "{}/{} {} {}, ".format(tokencard.Power, tokencard.Toughness, tokencard.Color, tokencard.name)
    if autoscripts == True: cardalign()
    notify("{} creates {}.".format(me, text[0:-2]))

def autoAddMarker(card, x = 0, y = 0):
  mute()
  text = ""
  markers = getTags(card, 'automarker')
  if markers != "":
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
    