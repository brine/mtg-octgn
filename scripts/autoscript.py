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
    setGlobalVariable('globaltags', "{ }")
    notify("{} reset the global tag cache.".format(me))
  if confirm("Reset the Attachment Dictionary?"):
    setGlobalVariable('cattach', "{ }")
    notify("{} reset the global attachment dictionary.".format(me))

def shuffle(group, x = 0, y = 0):
    global versioncheck
    if versioncheck == None:
      (url, code) = webRead('http://octgn.gamersjudgement.com/OCTGN/game.txt')
      if code == 200:
        if not url == gameVersion:
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

def getTags(card, key):
  mute()
  while getGlobalVariable('globaltags') == 'CHECKOUT':
    whisper("Global card tag dictionary is currently in use, please wait.")
    return CRASH
  savedtags = eval(getGlobalVariable('globaltags'))
  setGlobalVariable('globaltags', 'CHECKOUT')
  if re.search(r"//", card.name):
    if card.isAlternateImage == True or card.orientation & Rot180 == Rot180:
      cardname = (card.name)[(card.name).find("/")+2:]
    else:
      cardname = (card.name)[:(card.name).find("/")]
  else:
    cardname = card.name
  encodedcardname = Convert.ToBase64String(Text.Encoding.UTF8.GetBytes(cardname))
  if not cardname in savedtags:
    (fulltag, code) = webRead('http://octgn.gamersjudgement.com/tags.php?id={}'.format(encodedcardname))
    if not code == 200:
      whisper('tag database is currently unavailable.')
      fulltag = tags[cardname]
    tagpieces = fulltag.split('; ')
    tagdict = { }
    for t in tagpieces:
     if not t == "":
       t2 = t.split('.')
       tagdict[t2[0]] = t2[1:]
    savedtags[cardname] = tagdict
  setGlobalVariable('globaltags', str(savedtags))
  if key == 'allactivate':
    st = savedtags[cardname]
    if 'activateinit1' in st: text11 = st['activateinit1']
    else: text11 = ''
    if 'activate1' in st: text12 = st['activate1']
    else: text12 = ''
    if 'activateinit2' in st: text21 = st['activateinit2']
    else: text21 = ''
    if 'activate2' in st: text22 = st['activate2']
    else: text22 = ''
    if 'activateinit3' in st: text31 = st['activateinit3']
    else: text31 = ''
    if 'activate3' in st: text32 = st['activate3']
    else: text32 = ''
    if 'activateinit4' in st: text41 = st['activateinit4']
    else: text41 = ''
    if 'activate4' in st: text42 = st['activate4']
    else: text42 = ''
    if 'activateinit5' in st: text51 = st['activateinit5']
    else: text51 = ''
    if 'activate5' in st: text52 = st['activate5']
    else: text52 = ''
    return "1) {}\n  --> {}\n2) {}\n  --> {}\n3) {}\n  --> {}\n4) {}\n  --> {}\n5) {}\n  --> {}".format(text11, text12, text21, text22, text31, text32, text41, text42, text51, text52)
  if key in savedtags[cardname]:
    return savedtags[cardname][key]
  else:
    return ""

def submitTags(card, x = 0, y = 0):
  if re.search(r"//", card.name):
    if card.isAlternateImage == True or card.orientation & Rot180 == Rot180:
      cardname = (card.name)[(card.name).find("/")+2:]
    else:
      cardname = (card.name)[:(card.name).find("/")]
  else:
    cardname = card.name
  encodedcardname = Convert.ToBase64String(Text.Encoding.UTF8.GetBytes(cardname))
  (url, code) = webRead('http://octgn.gamersjudgement.com/tags.php?id={}'.format(encodedcardname))
  if code == 200:
    if not url == "":
      if not confirm("Submit an edit?\n{}".format(url)): return()
    openUrl('http://octgn.gamersjudgement.com/submit.php?id={}'.format(encodedcardname))
  else:
      whisper("cannot connect to online database.")

def morph(card, x = 0, y = 0):
    mute()
    if card.isAlternateImage == True or re.search(r'DFC', card.Rarity):
      card.switchImage
      notify("{} transforms {}.".format(me, card))
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

def stackPlay(card):
  mute()
  castinittext = autoscript(card, getTags(card, 'castinit'))
  if castinittext == None: return
  card.moveToTable(0,0)
  card.markers[scriptMarkers['cast']] += 1
  casttext = autoscript(card, getTags(card, 'cast'))
  notify("{} casts {}{}{}.".format(me, card, castinittext, casttext))
  if not card.Type == None and re.search(r'Land', card.Type):
    stackResolve(card)
  cardalign()

def stackResolve(card):
  mute()
  if card in cstack:
    stackcard = cstack[card]
  if scriptMarkers['cast'] in card.markers:
    resolvecost = getTags(card, 'resolvecost')
    if scriptMarkers['cost'] in card.markers and not resolvecost == '':
      resolvetext = autoscript(card, resolvecost)
    else:
      resolvetext = autoscript(card, getTags(card, 'resolve'))
    if scriptMarkers['cost'] in card.markers and not getTags(card, 'etbcost') == '':
      newcard = table.create(card.model, 0, 0, 1)
      newcard.markers[scriptMarkers['etb']] += 1
      newcard.markers[scriptMarkers['cost']] += card.markers[scriptMarkers['cost']]
      cstack[newcard] = card
    elif not scriptMarkers['cost'] in card.markers and not getTags(card, 'etb') == '':
      newcard = table.create(card.model, 0, 0, 1)
      newcard.markers[scriptMarkers['etb']] += 1
      cstack[newcard] = card
    card.markers[scriptMarkers['cast']] = 0
    card.markers[scriptMarkers['cost']] = 0
    card.markers[scriptMarkers['x']] = 0
    trigtype = ""
  elif scriptMarkers['attack'] in card.markers:
    attackcost = getTags(card, 'attackcost')
    if scriptMarkers['cost'] in card.markers and not attackcost == '':
      resolvetext = autoscript(stackcard, attackcost)
    else:
      resolvetext = autoscript(stackcard, getTags(card, 'attack'))
    trigtype = "'s attack trigger"
  elif scriptMarkers['block'] in card.markers:
    blockcost = getTags(card, 'blockcost')
    if scriptMarkers['cost'] in card.markers and not blockcost == '':
      resolvetext = autoscript(stackcard, blockcost)
    else:
      resolvetext = autoscript(stackcard, getTags(card, 'block'))
    trigtype = "'s block trigger"
  elif scriptMarkers['etb'] in card.markers:
    etbcost = getTags(card, 'etbcost')
    if scriptMarkers['cost'] in card.markers and not etbcost == '':
      resolvetext = autoscript(stackcard, etbcost)
    else:
      resolvetext = autoscript(stackcard, getTags(card, 'etb'))
    trigtype = "'s enters-play trigger"
  elif scriptMarkers['destroy'] in card.markers:
    destroycost = getTags(card, 'destroycost')
    if scriptMarkers['cost'] in card.markers and not destroycost == '':
      resolvetext = autoscript(stackcard, destroycost)
    else:
      resolvetext = autoscript(stackcard, getTags(card, 'destroy'))    
    trigtype = "'s destroy trigger"
  elif scriptMarkers['exile'] in card.markers:
    exilecost = getTags(card, 'exilecost')
    if scriptMarkers['cost'] in card.markers and not exilecost == '':
      resolvetext = autoscript(card, exilecost)
    else:
      resolvetext = autoscript(card, getTags(card, 'exile'))
    trigtype = "'s exile trigger"
  elif scriptMarkers['activate'] in card.markers:
    markercount = card.markers[scriptMarkers['activate']]
    activatecost = getTags(card, 'activatecost{}',format(markercount))
    if scriptMarkers['cost'] in card.markers and not activatecost == '':
      resolvetext = autoscript(stackcard, activatecost)
    else:
      resolvetext = autoscript(stackcard, getTags(card, 'activatecost{}'.format(markercount)))
    trigtype = "'s ability {} trigger".format(markercount)
  if card in cstack or re.search(r'Instant', card.Type) or re.search(r'Sorcery', card.Type):
    card.moveTo(me.Graveyard)
  notify("{} resolves {}{}{}.".format(me, card, trigtype, resolvetext))
  cardalign()

def stackAttack(card, tap):
  mute()
  attackinittext = autoscript(card, getTags(card, 'attackinit'))
  if attackinittext == None: return
  if card.orientation == Rot90:
    if not confirm("Cannot attack: {} is already tapped. Continue?".format(card.name)): return
  if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
    card.highlight = AttackDoesntUntapColor
  else:
    card.highlight = AttackColor
  if tap == True:
    card.orientation |= Rot90
  if not getTags(card, 'attack') == '':
    newcard = table.create(card.model, 0, 0, 1)
    newcard.markers[scriptMarkers['attack']] += 1
    cstack[newcard] = card
  notify("{} attacks with {}{}.".format(me, card, attackinittext))
    
def stackBlock(card):
  mute()
  blockinittext = autoscript(card, getTags(card, 'blockinit'))
  if blockinittext == None: return
  if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
    card.highlight = BlockDoesntUntapColor
  else:
    card.highlight = BlockColor
  if not getTags(card, 'block') == '':
    newcard = table.create(card.model, 0, 0, 1)
    newcard.markers[scriptMarkers['block']] += 1
    cstack[newcard] = card
  notify("{} blocks with {}{}.".format(me, card, blockinittext))

def stackDestroy(card):
  mute()
  destroyinittext = autoscript(card, getTags(card, 'destroyinit'))
  if destroyinittext == None: return
  card.moveTo(me.Graveyard)
  if not getTags(card, 'destroy') == '':
    newcard = table.create(card.model, 0, 0, 1)
    newcard.markers[scriptMarkers['destroy']] += 1
    cstack[newcard] = card
  notify("{} destroys {}{}.".format(me, card, destroyinittext))
 
def stackExile(card):
  mute()
  exileinittext = autoscript(card, getTags(card, 'exileinit'))
  if exileinittext == None: return
  card.moveTo(me.piles['Exiled Zone'])
  if not getTags(card, 'exile') == '':
    newcard = table.create(card.model, 0, 0, 1)
    newcard.markers[scriptMarkers['exile']] += 1
    cstack[newcard] = card
  notify("{} exiles {}{}.".format(me, card, exileinittext))
 
def stackActivate(card):
  mute()
  num = askInteger("Activate which ability?\n{}".format(getTags(card, 'allactivate')), 1)
  if num == None: return
  activateinittext = autoscript(card, getTags(card, 'activateinit{}'.format(num)))
  if activateinittext == None: return
  newcard = table.create(card.model, 0, 0, 1)
  newcard.markers[scriptMarkers['activate']] += num
  cstack[newcard] = card
  notify("{} activates {}'s {} ability{}.".format(me, card, num, activateinittext))

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
  cardalign()
  notify("{} re-aligns his cards on the table".format(me))

def resetvar(group, x = 0, y = 0):
  mute()
  global sideflip
  if Table.isTwoSided():
    if me.hasInvertedTable():
      playerside = -1
    else:
      playerside = 1
    if len(players) > 2 and len(players) < 5:
      if confirm("Are you on the right side?"):
        sideflip = playerside * 1
      else:
        sideflip = playerside * -1
    else:
      sideflip = 1
  else:
    playerside = 1
    sideflip = 1

def cardalign():
  mute()
  while getGlobalVariable('cattach') == 'CHECKOUT':
    whisper("Global card attachment dictionary is currently in use, please wait.")
    return CRASH
  cattach = eval(getGlobalVariable('cattach'))
  setGlobalVariable('cattach', 'CHECKOUT')
  group1 = [cardid for cardid in cattach if not Card(cattach[cardid]).group.name == "Table"]
  for cardid in group1:
    if not Card(cardid).subtype == None and re.search(r'Aura', Card(cardid).Subtype):
      Card(cardid).moveTo(me.Graveyard)
      notify("{}'s {} was destroyed".format(me, Card(cardid)))
    del cattach[card]
  group2 = [cardid for cardid in cattach if not Card(cardid).group.name == "Table"]
  for cardid in group2:
    del cattach[cardid]
  global playerside
  global sideflip
  if Table.isTwoSided():
    if playerside == None:
      if me.hasInvertedTable():
        playerside = -1
      else:
        playerside = 1
    if sideflip == None:
      if len(players) > 2 and len(players) < 5:
        playersort = sorted(players, key=lambda player: player._id)
        if playersort[0] == me or playersort[1] == me:
          sideflip = 1
        else:
          sideflip = -1
      else:
        sideflip = 1
  else:
    playerside = 1
    sideflip = 1
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
        or scriptMarkers['x'] in card.markers)
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
        and not counters['general'] in card.markers
        and not card._id in cattach]
  cardsort = sorted(tablecards, key=lambda card:(card.Type, card.name))
  for card in cardsort:
      if re.search(r'Land', card.Type) or re.search(r'Planeswalker', card.Type):
        if len(card.markers) == 0 and not card._id in dict([(v, k) for k, v in cattach.iteritems()]):
          if not card.name in landdict or landdict[card.name] == 0:
            landdict[card.name] = 1
            landorder.append(card.name)
            xpos = len(landorder)
            ypos = 1
          elif landdict[card.name] >= 3:
            landdict[card.name] = 0
            xpos = landorder.index(card.name) + 1
            landorder[landorder.index(card.name)] = ['BLANK']
            ypos = 4
          else:
            landdict[card.name] += 1
            xpos = landorder.index(card.name) + 1
            ypos = landdict[card.name]
        else:
          landorder.append('BLANK')
          xpos = len(landorder)
          ypos = 4
        card.moveToTable(sideflip * xpos * 80, playerside * 170 - 44 + playerside * 9 * ypos)
      else:
        if len(card.markers) == 0 and not card._id in dict([(v, k) for k, v in cattach.iteritems()]):
          if not card.name in carddict or carddict[card.name] == 0:
            carddict[card.name] = 1
            cardorder.append(card.name)
            xpos = len(cardorder)
            ypos = 1
          elif carddict[card.name] >= 3:
            carddict[card.name] = 0
            xpos = cardorder.index(card.name) + 1
            cardorder[cardorder.index(card.name)] = ['BLANK']
            ypos = 4
          else:
            carddict[card.name] += 1
            xpos = cardorder.index(card.name) + 1
            ypos = carddict[card.name]
        else:
          cardorder.append('BLANK')
          xpos = len(cardorder)
          ypos = 4
        card.moveToTable(sideflip * xpos * 80, playerside * 45- 44 + playerside * 9 * ypos)
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
  setGlobalVariable('cattach', str(cattach))

def stackcount(card):
    castcount = sum(1 for card in table if card.markers[scriptMarkers['cast']] >= 1)
    etbcount = sum(1 for card in table if card.markers[scriptMarkers['etb']] >= 1)
    activatedcount = sum(1 for card in table if card.markers[scriptMarkers['activate']] >= 1)
    destroycount = sum(1 for card in table if card.markers[scriptMarkers['destroy']] >= 1)
    attackcount = sum(1 for card in table if card.markers[scriptMarkers['attack']] >= 1)
    return ((castcount + etbcount + activatedcount + destroycount + attackcount) * 10)

def cardcount(search, card):
  multiplier = 1
  if re.search(r'-', search):
    search = search.replace('-', '')
    multiplier = multiplier * (0 - 1)
  if re.search(r'2x', search):
    search = search.replace('2x', '')
    multiplier = multiplier * 2 
  if search == "x":
    qty = card.markers[scriptMarkers['x']]
    card.markers[scriptMarkers['x']] -= qty 
  elif search == "cost":
    qty = card.markers[scriptMarkers['cost']]
    card.markers[scriptMarkers['cost']] -= qty 
  elif re.search(r'marker\.', search):
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

def autoscript(card, taglist):
  autotext = ""
  for tags in taglist:
    p1 = tags[:tags.find("[")]
    p2 = tags[tags.find("[")+1:tags.find("]")]
    if p1 == "marker":
      (markername, qty) = p2.split(', ')
      count = card.markers[counters[markername]]
      if count + cardcount(qty, card) < 0:
        whisper("not enough {} counters to remove!".format(markername))
        return
    elif p1 == "tapped" and card.orientation == Rot90:
      whisper("{} is already tapped!".format(card))
      return
    elif p1 == "untapped" and card.orientation == Rot0:
      whisper("{} is already untapped!".format(card))
      return
  for tags in taglist:
    text = ""
    p1 = tags[:tags.find("[")]
    p2 = tags[tags.find("[")+1:tags.find("]")]
    if p1 == "cost":
      text = autocost(card, p2)
    elif p1 == "token":
      text = autotoken(card, p2)
    elif p1 == "marker":
      text = automarker(card, p2)
    elif p1 == "highlight":
      text = autohighlight(card, p2)
    elif p1 == "tapped":
      text = autotapped(card, p2)
    elif p1 == "untapped":
      text = autountapped(card, p2)
    elif p1 == "moveto":
      text = automoveto(card, p2)
    elif p1 == "transform":
      text = autotransform(card, p2)
    else:
      text = ""
    if text == None:
      return
    autotext += text
  return autotext

def autocost(card, tag):
    (type, qty) = tag.split(', ')
    if type == 'x':
      marker = scriptMarkers['x']
    else:
      marker = scriptMarkers['cost']
    if qty == "1":
      if confirm("{}'s {}: Pay additional/alternate cost?".format(card.name, type)):
        card.markers[marker] = 1
        cost = ", paying {} cost".format(type.title())
      else:
        cost = ""
    else:
      amount = askInteger("{}'s {}: Paying how many times?".format(card.name, type), 0)
      if amount == None: amount = 0
      card.markers[marker] = amount
      cost = ", paying {} {} times".format(type.title(), amount)
    return cost

def autotransform(card, tag):
  if tag == "no": return ""
  if tag == "ask":
    if not confirm("Transform {}?".format(card.name)): return ""
  card.switchImage
  return ", transforming to {}".format(card)

def autotoken(card, tag):
  tag2 = tag.split(', ')
  name = tag2[0]
  qty = tag2[1]
  if len(tag2) > 2:
    modifiers = tag2[2:]
  else:
    modifiers = ""
  quantity = cardcount(qty, card)
  if quantity == 1:
    quant = ""
  else:
    quant = "s"
  if not quantity == 0:
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
          (marker, type, quant) = modtag.split('.')
          token.markers[counters[type]] += cardcount(qty, token)
    tokentext = "{} {}/{} {} {}".format(quantity, token.Power, token.Toughness, token.Color, token.name)
    cardalign()
    return ", creating {} token{}".format(tokentext, quant)
  else:
    return ""

def automarker(card, tag):
  (markername, qty) = tag.split(', ')
  quantity = cardcount(qty, card)
  if quantity == 1:
    quant = ""
  else:
    quant = "s"
  addmarker = counters[markername]
  card.markers[addmarker] += quantity
  if quantity > 0:
      sign = "+"
  elif quantity < 0:
      sign = "-"
  else:
      sign = ""
  return ", {}{} {}{}".format(sign, quantity, addmarker[0], quant)

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

def automoveto(card, pile):
    cardowner = card.owner
    cards = card
    position = re.sub("[^0-9]", "", pile)
    if not position == "":
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
      stackExile(card)
      text = "exile"
    elif re.search(r'hand', pile):
      cards.moveTo(cardowner.hand)
      text = "hand"
    elif re.search(r'graveyard', pile):
      stackDestroy(card)
      text = "graveyard"
    elif re.search(r'stack', pile):
      stackPlay(card)
      text = "stack"
    elif re.search(r'table', pile):
      stackResolve(card)
      text = "table"
    return ", moving to {}".format(text)

############################
#Smart Token/Markers
############################