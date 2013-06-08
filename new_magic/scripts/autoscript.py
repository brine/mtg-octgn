import re
import time
import clr
from System import Convert
from System import Text

playerside = None
sideflip = None
cstack = { }

versioncheck = None
offlinedisable = False

def clearCache(group, x = 0, y = 0):
  if confirm("Reset the Autoscript Tag cache?"):
    global savedtags
    savedtags = { }
    notify("{} reset the global tag cache.".format(me))
  if confirm("Reset the Attachment Dictionary?\nNote: Cards will no longer be attached."):
    setGlobalVariable('cattach', "{ }")
    notify("{} reset the global attachment dictionary.".format(me))

def versionCheck():
    global versioncheck
    if versioncheck == None:
      (url, code) = webRead('http://octgn.gamersjudgement.com/OCTGN/game.txt', 7000)
      if code != 200 or url == "":
        whisper("Newest game definition version is unavailable at the moment")
        versioncheck = False
        return
      versioncheck = True
      currentVers = url.split('.')
      installedVers = gameVersion.split('.')
      if len(installedVers) < 3:
        whisper("Your game definition does not follow the correct version conventions.  It is most likely outdated or modified from its official release.")
        return
      if int(currentVers[0]) < int(installedVers[0]):
        return
      if int(currentVers[1]) < int(installedVers[1]):
        return
      if int(currentVers[2]) <= int(installedVers[2]):
        return
      notify("{}'s game definition ({}) is out-of!-date!".format(me, gameVersion))
      if confirm("There is a new game definition available! Your version {}. Current version {}.\nClicking yes will open your browser to the location of the most recent version.".format(gameVersion, url)):
        openUrl('http://octgn.gamersjudgement.com/forum/viewtopic.php?f=8&t=195')


def shuffle(group, x = 0, y = 0):
    mute()
#    versionCheck()
    for card in group:
      if card.isFaceUp:
        card.isFaceUp = False
    group.shuffle()
    notify("{} shuffled their {}".format(me, group.name))

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

def getTags(cardname, cardrules, key, rulesline = None):
  mute()
  global savedtags, offlinedisable
  encodedcardname = Convert.ToBase64String(Text.Encoding.UTF8.GetBytes(cardname))
  if not cardname in savedtags:
    if re.search(r'creature token', cardrules):
      encodedcardname += '&token'
    if re.search(r'counter', cardrules):
      encodedcardname += "&counter"
    if re.search(r'{} enters the battlefield'.format(cardname), cardrules):
      encodedcardname += '&etb'
    if re.search(r'{} dies'.format(cardname), cardrules):
      encodedcardname += '&destroy'
    if re.search(r'{} attacks'.format(cardname), cardrules):
      encodedcardname += '&attack'
    if re.search(r'{} blocks'.format(cardname), cardrules):
      encodedcardname += '&block'
    if offlinedisable == False:
      (fulltag, code) = webRead('http://octgn.gamersjudgement.com/forum/tags2.php?id={}'.format(encodedcardname), 7000)
      if code == 204:
        fulltag = ""
      elif code != 200:
        whisper('tag database is currently unavailable, using offline tag cache')
        offlinedisable = True
    if offlinedisable == True:
        if cardname in offlineTags:
          fulltag = offlineTags[cardname]
        else:
          fulltag = ""
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
    tagstring = ''
    for st in savedtags[cardname]: tagstring += st
    count = 0
    returntext = []
    ruleslist = cardrules.splitlines()
    for lines in cardrules.splitlines():
      count += 1
      if re.search('acti{}'.format(str(count)), tagstring):
        returntext.append((True, '{}\n'.format(lines)))
      else:
        returntext.append((False, '{}\n'.format(lines)))
    return (savedtags[cardname], returntext)
  if key == 'allmodes':
    tagstring = ''
    for st in savedtags[cardname]: tagstring += ";{}".format(st)
    splitrules = cardrules.splitlines()[int(rulesline) - 1]
    count = 0
    modelist = []
    for mode in splitrules.split("; or "):
      count += 1
      if re.search(';{}'.format(str(count)), tagstring):
        modelist.append((True, '{}\n'.format(mode)))
      else:
        modelist.append((False, '{}\n'.format(mode)))
    return modelist
  if key in savedtags[cardname]:
    return savedtags[cardname][key]
  else:
    return ""

def submitTags(card, x = 0, y = 0):
  cardname = card.Name
  encodedcardname = Convert.ToBase64String(Text.Encoding.UTF8.GetBytes(cardname))
  (url, code) = webRead('http://octgn.gamersjudgement.com/forum/tags2.php?id={}'.format(encodedcardname))
  if code == 200 or code == 204:
    if code == 200:
      if not confirm("Submit an edit?\n{}".format(url)): return()
    openUrl('http://octgn.gamersjudgement.com/forum/submit2.php?id={}'.format(encodedcardname))
  else:
      whisper("cannot connect to online database.")

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
        card.isFaceUp = True
        notify("{} morphs {} face up.".format(me, card))

def suspend(card, x = 0, y = 0):
  mute()
  num = askInteger("Suspending {}, what is X?\n(To cancel, choose 0.)".format(card.Name), 0)
  if num != 0 and num != None:
    card.moveToTable(0,0)
    card.markers[scriptMarkers['suspend']] = 1
    card.markers[counters['time']] = num
    cardalign()
    notify("{} suspends {} for {}.".format(me, card, num))

def blink(card, x = 0, y = 0):
    mute()
    src = card.group
    if autoscripts == True and src == table:
        text = autoParser(card, 'exile')
        if text == "BREAK": return
        card.moveTo(card.owner.piles['Exiled Zone'])
        cardalign()
        card.moveToTable(0,0)
        autoParser(card, 'cast', True)
        cardalign()
        notify("{} blinks {}.".format(me, card))

##################################
#Card Functions -- Autoscripted  
##################################
import time

def autoParser(c, tagclass, res = False):
  mute()
  markerdict = { }
  text = ""
  restag = ""
  stackcard = c
  card = c
  if res == True:
    restag = "res"
    if not tagclass == "cast":
      if c in cstack:
        stackcard = c
        card = cstack[c]
      else:
        notify("ERROR: {}'s source cannot be identified! Can't be resolved.".format(c))
        return "BREAK"
#####SPLIT CARD CHECK#####
  if tagclass == 'cast' and res == False and card.Flags == 'split' and re.search('//', card.Name):
    splitnames = card.Name.split('//')
    if re.search('Fuse', card.Rules):
      splitnames.append('Fuse both sides')
    choice = askChoice('Cast which side?', splitnames)
    if choice == None or choice == 3:
      cardname = card.Name
    else:
      cardname = splitnames[choice - 1]
  else:
    choice = None
    cardname = card.Name
#####INITCHECKS######
  inittag = getTags(cardname, card.Rules, 'init{}{}'.format(restag, tagclass))
  if 'tapped' in inittag and card.orientation == Rot90:
    if not confirm("{} is already tapped!\nContinue?".format(cardname)):
      return "BREAK"
  if 'untapped' in inittag and card.orientation == Rot0:
    if not confirm("{} is already untapped!\nContinue?".format(cardname)):
      return "BREAK"
  if 'choice' in inittag:
    for choice in inittag['choice']:
      (rulesline, type) = choice.split(', ') ##the tag contains data for the rules line number and modes type
      rule = card.Rules.splitlines()[int(rulesline) - 1]  ##we want just the one rules line with the modes in it
      modes = rule.split(u'\u2014 ')[1] ##parse out the 'choose one - ' part
      modelist = modes.split("; or ")
      num = askChoice("Choose a mode for {}".format(cardname), modelist)
      markerdict['choice'] = num
      text += ", choosing mode #{}".format(num)
  if 'cost' in inittag:
    for ctag in inittag['cost']:
      (cost, type) = ctag.split(', ')
      if cost in scriptMarkers:
        marker = cost
      else:
        marker = 'cost'
      if type == "ask":
        if confirm("{}'s {}: Pay additional/alternate cost?".format(cardname, cost)):
          markerdict[marker] = 1
          text += ", paying {} cost".format(cost.title())
      elif type == "num":
        qty = askInteger("{}'s {}: Paying how many times?".format(cardname, cost), 0)
        if qty == None: qty = 0
        if qty != 0: markerdict[marker] = qty
        if qty == 1: text += ", paying {} once".format(cost.title())
        else: text += ", paying {} {} times".format(cost.title(), qty)
      else:
        qty = cardcount(card, stackcard, type)
        if qty != 0: markerdict[marker] = qty
  if 'marker' in inittag:
    for markertag in inittag['marker']:
      (markername, qty) = markertag.split(', ')
      count = card.markers[counters[markername]]
      if count + cardcount(card, stackcard, qty) < 0:
        if not confirm("Not enough {} counters to remove!\nContinue?".format(markername)): return "BREAK"
#####Move Card/Create Trigger#####
  if 'cost' in markerdict or scriptMarkers['cost'] in stackcard.markers:
    costtag = "cost"
  else:
    costtag = ""
  if 'choice' in markerdict:
    choicetag = markerdict['choice']
  elif scriptMarkers['choice'] in stackcard.markers:
    choicetag = stackcard.markers[scriptMarkers['choice']]
  else:
    choicetag = ""
  if res == False:
    if tagclass == 'etb':
      markerdict['cost'] = card.markers[scriptMarkers['cost']]
      markerdict['x'] = card.markers[scriptMarkers['x']]
    if tagclass == 'cast':
      card.moveToTable(0,0)
      markerdict['cast'] = 1
      if choice == 1:
        card.switchTo('splitA')
      elif choice == 2:
        card.switchTo('splitB')
      elif choice == 3:
        card.switchTo('splitC')
    else:
      if tagclass == 'cycle' or getTags(card.Name, card.Rules, "{}{}res{}".format(choicetag, costtag, tagclass)) != '':
        stackcard = table.create(card.model, 0, 0, 1)
        if card.alternate != "":
          stackcard.switchTo()
        if re.search(r'acti', tagclass):
          markerdict['activate'] = int(tagclass[-1])
        else:
          markerdict[tagclass] = 1
      cstack[stackcard] = card
  for markers in markerdict:
    stackcard.markers[scriptMarkers[markers]] += markerdict[markers]
####autoscripts####
  taglist = [inittag, getTags(card.Name, card.Rules, "{}{}{}{}".format(choicetag, costtag, restag, tagclass))]
  for tags in taglist:
    if 'copy' in tags:
      for tag in tags['copy']:
        text += autoCopy(card, stackcard, tag, markerdict)
    if 'persist' in tags:
      for tag in tags['persist']:
        text += autopersist(card, stackcard, tag)
    if 'undying' in tags:
      for tag in tags['undying']:
        text += autoundying(card, stackcard, tag)
    if 'attach' in tags:
      for tag in tags['attach']:
        target = [cards for cards in table if cards.targetedBy]
        if len(target) == 1:
          text = ", " + autoAttach(card, target[0])
    if 'life' in tags:
      for tag in tags['life']:
        text += autolife(card, stackcard, tag)
    if 'token' in tags:
      for tag in tags['token']:
        text += autotoken(card, stackcard, tag)
    if 'marker' in tags:
      for tag in tags['marker']:
        text += automarker(card, stackcard, tag)
    if 'smartmarker' in tags:
      for tag in tags['smartmarker']:
        text += autosmartmarker(card, tag)
    if 'highlight' in tags:
      for tag in tags['highlight']:
        text += autohighlight(card, tag)
    if 'tapped' in tags:
      for tag in tags['tapped']:
        text += autotapped(card, tag)
    if 'untapped' in tags:
      for tag in tags['untapped']:
        text += autountapped(card, tag)
    if 'transform' in tags:
      for tag in tags['transform']:
        text += autotransform(card, tag)
    if 'moveto' in tags:
      for tag in tags['moveto']:
        text += automoveto(card, tag)
  if res == True:
    if tagclass == 'cast':
      stackcard.markers[scriptMarkers['cast']] = 0
      if getTags(stackcard.Name, stackcard.Rules, "{}resetb".format(costtag)):
        autoParser(card, 'etb')
      stackcard.markers[scriptMarkers['cost']] = 0
      stackcard.markers[scriptMarkers['x']] = 0
      if re.search('Instant', stackcard.Type) or re.search('Sorcery', stackcard.Type):
        stackcard.moveTo(stackcard.owner.Graveyard)
    else:
      stackcard.moveTo(stackcard.owner.Graveyard)
      del cstack[stackcard]
  return text

############################
#Modifiers
############################

def attach(card, x = 0, y = 0):
  mute()
  if autoscripts == True:
    target = [cards for cards in table if cards.targetedBy]
    if len(target) == 0 or (len(target) == 1 and card in target):
      text = autoDetach(card)
    elif len(target) == 1:
      text = autoAttach(card, target[0])
    else:
      whisper("Incorrect targets, select up to 1 target.")
      return
    if text == "":
      return
    notify("{} {}.".format(me, text))
    cardalign()
  else:
    whisper("Autoscripts must be enabled to use this feature")

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
  cattach = eval(getGlobalVariable('cattach'))  ##converts attachment dict to a real dictionary
  group1 = [cardid for cardid in cattach if Card(cattach[cardid]) not in table]  ##selects attachment cards missing their original targets
  for cardid in group1:
    c = Card(cardid)
    if c.Subtype != None and re.search(r'Aura', c.Subtype) and c.controller == me:  ##if the attachment is an aura you control
      text = autoParser(c, 'destroy')
      if text != "BREAK":
        c.moveTo(c.owner.Graveyard)
        notify("{}'s {} was destroyed{}.".format(me, c, text))
    del cattach[cardid]  ##cleans up the attachment dict when the targeted card is no longer on the battlefield
  group2 = [cardid for cardid in cattach if Card(cardid) not in table]  ##selects targeted cards whose attachment cards are now missing
  for cardid in group2:
    del cattach[cardid]  ##clean up attachment dict
  if cattach != eval(getGlobalVariable('cattach')): ##checks to see if we changed the attached cards, because Kelly whined that we were updating global variables too often
    setGlobalVariable('cattach', str(cattach))  ##updates the global attachment dictionary with our changes
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
    if not counters['general'] in card.markers:
      if card.controller == me and (scriptMarkers['cast'] in card.markers
        or scriptMarkers['activate'] in card.markers
        or scriptMarkers['attack'] in card.markers
        or scriptMarkers['block'] in card.markers
        or scriptMarkers['destroy'] in card.markers
        or scriptMarkers['exile'] in card.markers
        or scriptMarkers['etb'] in card.markers
        or scriptMarkers['cost'] in card.markers
        or scriptMarkers['x'] in card.markers
        or scriptMarkers['discard'] in card.markers
        or scriptMarkers['miracle'] in card.markers
        or scriptMarkers['choice'] in card.markers):
          card.moveToTable(0, 10 * stackcount)
          stackcount += 1
      elif card.controller == me and not card._id in cattach:
        dictname = card.Name
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
          elif re.search(r"Creature", card.Type) or not card.isFaceUp: cardorder[0].append(dictname)
          elif re.search(r"Artifact", card.Type): cardorder[1].append(dictname)
          elif re.search(r"Enchantment", card.Type): cardorder[2].append(dictname)
          else: cardorder[6].append(dictname)
        carddict[dictname].append(card)
      elif card._id in cattach:
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
    if qty == None: qty = 0
  else:
    qty = int(search)
  return qty * multiplier

############################
#Autoscript
############################

def autoCopy(card, stackcard, tag, markers):
  mute()
  qty = cardcount(card, stackcard, tag)
  for x in range(0, qty):
    copy = table.create(card.model, 0, 0, 1)
    for m in markers:
      copy.markers[scriptMarkers[m]] = markers[m]
  if qty == 1:
    return ", copied once"
  else:
    return ", copied {} times".format(qty)

def autoAttach(card, targetcard):
  mute()
  cattach = eval(getGlobalVariable('cattach'))
  if targetcard._id in cattach and cattach[targetcard._id] == card._id:
    del cattach[targetcard._id]
  cattach[card._id] = targetcard._id
  targetcard.target(False)
  setGlobalVariable('cattach', str(cattach))
  return "attaching {} to {}".format(card, targetcard)

def autoDetach(card):
  mute()
  cattach = eval(getGlobalVariable('cattach'))
  card.target(False)
  if card._id in dict([(v, k) for k, v in cattach.iteritems()]):
    card2 = [k for k, v in cattach.iteritems() if v == card._id]
    for card3 in card2:
      del cattach[card3]
      text = "{} unattaches {} from {}.".format(me, Card(card3), card)
  elif card._id in cattach:
    card2 = cattach[card._id]
    del cattach[card._id]
    text = "unattaching {} from {}".format(card, Card(card2))
  else:
    return ""
  setGlobalVariable('cattach', str(cattach))
  return text

def autopersist(card, stackcard, persist):
  if card.group.name == "Graveyard":
    card.moveToTable(0,0)
    autoParser(card, 'cast', True)
    card.markers[counters['minusoneminusone']] += 1
    return ", persisting"
  else:
    return ""

def autoundying(card, stackcard, undying):
  if card.group.name == "Graveyard":
    card.moveToTable(0,0)
    autoParser(card, 'cast', True)
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
      if autoParser(cards, 'exile') != "BREAK":
        cards.moveTo(card.owner.piles['Exiled Zone'])
        text = "exile"
    elif re.search(r'hand', pile):
      cards.moveTo(card.owner.hand)
      text = "hand"
    elif re.search(r'graveyard', pile):
      if autoParser(cards, 'destroy') != "BREAK":
        cards.moveTo(card.owner.Graveyard)
        text = "graveyard"
    elif re.search(r'stack', pile):
      if autoParser(cards, 'cast') != "BREAK":
        text = "stack"
    elif re.search(r'table', pile):
      card.moveToTable(0,0)
      autoParser(card, 'cast', True)
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
    if not confirm("Transform {}?".format(card.Name)): return ""
  if 'transform' in card.alternates:
    if card.alternate == '':
      card.switchTo('transform')
    else:
      card.switchTo()
  else:
    whisper("Oops, transform cards aren't ready yet!")
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
      confirm("Cannot create {}'s token -- your markers & tokens set definition is missing this token.".format(stackcard.Name))
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
          elif modtag == 'attach':
            autoAttach(card, token)
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
  tokens = getTags(card.Name, card.Rules, 'autotoken')
  if tokens != "":
    for token in tokens:
      addtoken = tokenTypes[token]
      tokencard = table.create(addtoken[1], x, y, 1, persist = False)
      if tokencard == None:
        confirm("Cannot create {}'s token -- your markers & tokens set definition is missing this token.".format(card))
        return
      x, y = table.offset(x, y)
      text += "{}/{} {} {}, ".format(tokencard.Power, tokencard.Toughness, tokencard.Color, tokencard.Name)
    if autoscripts == True: cardalign()
    notify("{} creates {}.".format(me, text[0:-2]))

def autoAddMarker(card, x = 0, y = 0):
  mute()
  text = ""
  markers = getTags(card.Name, card.Rules, 'automarker')
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
    