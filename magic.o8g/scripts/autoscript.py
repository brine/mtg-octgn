import re
import time
import clr
from System import Convert
from System import Text

playerside = None
sideflip = None
cstack = { }

versioncheck = None

def clearCache(group, x = 0, y = 0):
  if confirm("Reset the Autoscript Tag cache?"):
    global savedtags
    savedtags = { }
    notify("{} reset the global tag cache.".format(me))
  if confirm("Reset the Attachment Dictionary?"):
    setGlobalVariable('cattach', "{ }")
    notify("{} reset the global attachment dictionary.".format(me))

def shuffle(group, x = 0, y = 0):
    global versioncheck
    if versioncheck == None:
      (url, code) = webRead('http://octgn.gamersjudgement.com/OCTGN/game.txt')
      if code == 200:
        if url == gameVersion:
          whisper("Your game definition is up-to-date")
        else:
          notify("{}'s game definition is out-of-date!".format(me))
          if confirm("There is a new game definition available! Your version {}. Current version {}.\nClicking yes will open your browser to the location of the most recent version.".format(gameVersion, url)):
            openUrl('http://octgn.gamersjudgement.com/viewtopic.php?f=8&t=195')
      else:
          whisper("Newest game definition version is unavailable at the moment")
      versioncheck = True
    for card in group:
      if card.isFaceUp:
        card.isFaceUp = False
    group.shuffle()

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
    stackcard.moveTo(me.Graveyard)
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
  target = (card for card in table if card.targetedBy)
  targetcount = sum(1 for card in table if card.targetedBy)
  if targetcount == 0:
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
  elif targetcount == 1:
    for targetcard in target:
      if card == targetcard:
        del cattach[card._id]
        notify("{} unattaches {} from {}.".format(me, card, targetcard))
      else:
        cattach[card._id] = targetcard._id
        targetcard.target(False)
        notify("{} attaches {} to {}.".format(me, card, targetcard))
  else:
    whisper("Incorrect targets, select only 1 target.")
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
  global playerside
  global sideflip
  if sideflip == 0:
    return "BREAK"
  if Table.isTwoSided():
    if playerside == None:
      if me.hasInvertedTable():
        playerside = -1
      else:
        playerside = 1
    if sideflip == None:
      playersort = sorted(players, key=lambda player: player._id)
      playercount = [p for p in playersort if me.hasInvertedTable() == p.hasInvertedTable()]
      if len(playercount) > 2:
        whisper("Cannot align: Too many players on your side of the table.")
        sideflip = 0
        return "BREAK"
      if playercount[0] == me:
        sideflip = 1
      else:
        sideflip = -1
  else:
    whisper("Cannot align: Two-sided table is required for card alignment.")
    sideflip = 0
    return "BREAK"
  while getGlobalVariable('cattach') == 'CHECKOUT':
    whisper("Global card attachment dictionary is currently in use, please wait.")
    return "BREAK"
  cattach = eval(getGlobalVariable('cattach'))
  setGlobalVariable('cattach', 'CHECKOUT') not in table
  group1 = [cardid for cardid in cattach if Card(cattach[cardid]) not in table]
  for cardid in group1:
    if Card(cardid).Subtype != None and re.search(r'Aura', Card(cardid).Subtype) and Card(cardid).controller == me:
      Card(cardid).moveTo(me.Graveyard)
      notify("{}'s {} was destroyed".format(me, Card(cardid)))
    del cattach[cardid]
  group2 = [cardid for cardid in cattach if Card(cardid) not in table]
  for cardid in group2:
    del cattach[cardid]
  setGlobalVariable('cattach', str(cattach))
  stackcount = 0
  stackcards = (card for card in table
        if scriptMarkers['cast'] in card.markers
        or scriptMarkers['activate'] in card.markers
        or scriptMarkers['attack'] in card.markers
        or scriptMarkers['block'] in card.markers
        or scriptMarkers['destroy'] in card.markers
        or scriptMarkers['exile'] in card.markers
        or scriptMarkers['etb'] in card.markers
        or scriptMarkers['cost'] in card.markers
        or scriptMarkers['x'] in card.markers
        or scriptMarkers['cycle'] in card.markers
        or scriptMarkers['miracle'] in card.markers)
  for card in stackcards:
      if card.controller == me:
        card.moveToTable(0, 0 + 10 * stackcount)
      stackcount += 1
  cardorder = [ ]
  carddict = { }
  landorder = [ ]
  landdict = { }
  tablecards = [card for card in table
        if card.controller == me
        and not scriptMarkers['cast'] in card.markers
        and not scriptMarkers['activate'] in card.markers
        and not scriptMarkers['attack'] in card.markers
        and not scriptMarkers['block'] in card.markers
        and not scriptMarkers['destroy'] in card.markers
        and not scriptMarkers['exile'] in card.markers
        and not scriptMarkers['etb'] in card.markers
        and not scriptMarkers['cost'] in card.markers
        and not scriptMarkers['x'] in card.markers
        and not scriptMarkers['cycle'] in card.markers
        and not scriptMarkers['miracle'] in card.markers
        and not counters['general'] in card.markers
        and not card._id in cattach]
  cardsort = sorted(tablecards, key=lambda card:(sortlist(card), card.name))
  for card in cardsort:
      if re.search(r'Land', card.Type) or re.search(r'Planeswalker', card.Type) or re.search(r'Emblem', card.Type):
        vardict = landdict
        varorder = landorder
        yshift = 170
      else:
        vardict = carddict
        varorder = cardorder
        yshift = 45
      if len(card.markers) == 0 and not card._id in dict([(v, k) for k, v in cattach.iteritems()]):
          if not card.name in vardict or vardict[card.name] == 0:
            vardict[card.name] = 1
            varorder.append(card.name)
            xpos = len(varorder)
            ypos = 1
          elif vardict[card.name] >= 3:
            vardict[card.name] = 0
            xpos = varorder.index(card.name) + 1
            varorder[varorder.index(card.name)] = ['BLANK']
            ypos = 4
          else:
            vardict[card.name] += 1
            xpos = varorder.index(card.name) + 1
            ypos = vardict[card.name]
      else:
          varorder.append('BLANK')
          xpos = len(varorder)
          ypos = 4
      card.moveToTable(sideflip * xpos * 80, playerside * yshift - 44 + playerside * 9 * ypos)
  cattachcount = { }
  attachcardsgroup = [card for card in table
        if card.controller == me
        and not scriptMarkers['cast'] in card.markers
        and not scriptMarkers['activate'] in card.markers
        and not scriptMarkers['attack'] in card.markers
        and not scriptMarkers['block'] in card.markers
        and not scriptMarkers['destroy'] in card.markers
        and not scriptMarkers['exile'] in card.markers
        and not scriptMarkers['etb'] in card.markers
        and not scriptMarkers['cost'] in card.markers
        and not scriptMarkers['x'] in card.markers
        and not scriptMarkers['cycle'] in card.markers
        and not scriptMarkers['miracle'] in card.markers
        and not counters['general'] in card.markers
        and card._id in cattach]
  attachcards= sorted(attachcardsgroup, key=lambda card: card.name)
  for card in attachcards:
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

def sortlist(card):
  if re.search(r"Land", card.Type): return "A"
  elif re.search(r"Planeswalker", card.Type): return "B"
  elif re.search(r"Emblem", card.Type): return "C"
  elif re.search(r"Creature", card.Type): return "D"
  elif re.search(r"Artifact", card.Type): return "E"
  elif re.search(r"Enchantment", card.Type): return "F"
  else: return "G"

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
    cardowner = card.owner
    cards = card
    position = re.sub("[^0-9]", "", pile)
    if position != "":
      pos = int(position)
      cards.moveTo(cardowner.Library, pos)
      text = "{} from top of library".format(pos)
    if re.search(r'top', pile):
      cards.moveTo(cardowner.Library)
      text = "top of library"
    elif re.search(r'bottom', pile):
      cards.moveToBottom(cardowner.Library)
      text = "bottom of library"
    elif re.search(r'shuffle', pile):
      librarycount = len(cardowner.Library)
      n = rnd(0, librarycount)
      cards.moveTo(cardowner.Library, n)
      cardowner.Library.shuffle()
      text = "library and shuffled"
    elif re.search(r'exile', pile):
      if trigAbility(card, 'exile', 'Exiled Zone') != "BREAK":
        text = "exile"
    elif re.search(r'hand', pile):
      cards.moveTo(cardowner.hand)
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
    