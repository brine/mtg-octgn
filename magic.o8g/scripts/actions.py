#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------
import re

phases = [
    'It is currently in the Pre-game Setup Phase',
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

#---------------------------------------------------------------------------
# Global variables
#---------------------------------------------------------------------------

phaseIdx = 0

#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------
def respond(group, x = 0, y = 0):
    notify('{} RESPONDS!'.format(me))

def passPriority(group, x = 0, y = 0):
    notify('{} passes priority to an opponent.'.format(me))

def showCurrentPhase(group, x = 0, y = 0):
    notify(phases[phaseIdx].format(me))

def nextPhase(group, x = 0, y = 0):
    global phaseIdx
    if phaseIdx == 10:
      phaseIdx = 1
    else:
      phaseIdx += 1
    showCurrentPhase(group)

def goToUpkeep(group, x = 0, y = 0):
    global phaseIdx
    phaseIdx = 2
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
    notify("{} untaps and enters the UPKEEP Step.".format(me))

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
    if not confirm("Are you sure you want to scoop?"): return
    me.life = 20
    me.poison = 0
    me.white = 0
    me.blue = 0
    me.black = 0
    me.red = 0
    me.green = 0
    me.colorless = 0
    myCards = (card for card in table
                    if card.owner == me)
    for card in myCards: 
        card.moveTo(me.Library)
    Library = me.Library
    for c in me.Graveyard: c.moveTo(Library)
    for c in me.hand: c.moveTo(Library)
    exile = me.piles['Exiled Zone']
    for c in exile: c.moveTo(Library)
    uselessvar = rnd(10, 1000)
    Library.shuffle()
    notify("{} scoops.".format(me))

def clearAll(group, x = 0, y = 0):
    notify("{} clears all targets and highlights.".format(me))
    for card in group:
      card.target(False)
      if card.controller == me:
          card.highlight = None

diesides = 20

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
    card, quantity = askCard("[Rarity] = 'Token'")
    if quantity == 0: return
    table.create(card, x, y, quantity)

############################
#Card functions
############################

def play(card, x = 0, y = 0):
  mute()
  if autoscripts == True:
    text = trigAbility(card, 'cast', 'table')
    if text != "BREAK":
      notify("{} casts {}{}.".format(me, card, text))
  else:
    src = card.group
    card.moveToTable(0, 0)
    notify("{} plays {} from their {}.".format(me, card, src.name))
    
def resolve(card, x = 0, y = 0):
  mute()
  if autoscripts == True:
    if scriptMarkers['miracle'] in card.markers:
      text = stackResolve(card, 'miracle')
      notify("{}'s {} Miracle trigger resolves{}.".format(me, card, text))
    elif scriptMarkers['attack'] in card.markers:
      text = stackResolve(card, 'attack')
      notify("{}'s {} attack trigger resolves{}.".format(me, card, text))
    elif scriptMarkers ['block'] in card.markers:
      text = stackResolve(card, 'block')
      notify("{}'s {} block trigger resolves{}.".format(me, card, text))
    elif scriptMarkers ['destroy'] in card.markers:
      text = stackResolve(card, 'destroy')
      notify("{}'s {} destroy trigger resolves{}.".format(me, card, text))
    elif scriptMarkers ['exile'] in card.markers:
      text = stackResolve(card, 'exile')
      notify("{}'s {} exile trigger resolves{}.".format(me, card, text))
    elif scriptMarkers ['cast'] in card.markers:
      text = stackResolve(card, 'resolve')
      notify("{} resolves {}{}.".format(me, card, text))
    elif scriptMarkers ['etb'] in card.markers:
      text = stackResolve(card, 'etb')
      notify("{}'s {} enters-play trigger resolves{}.".format(me, card, text))
    elif scriptMarkers ['activate'] in card.markers:
      num = card.markers[scriptMarkers['activate']]
      text = stackResolve(card, 'activate{}'.format(num))
      notify("{}'s {} ability #{} trigger resolves{}.".format(me, card, num, text))
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

def destroy(card, x = 0, y = 0):
  mute()
  src = card.group
  if autoscripts == True and src == table:
    for marker in scriptMarkers:

      if scriptMarkers[marker] in card.markers:
        card.moveTo(me.Graveyard)
        notify("{}'s {} was countered.".format(me, card))
        return
    text = trigAbility(card, 'destroy', 'Graveyard')
    if text != "BREAK":
      notify("{} destroys {}{}.".format(me, card, text))
  else:
    card.moveTo(me.Graveyard)
    if src == table:
      notify("{} destroys {}.".format(me, card, fromText))
    else:
      notify("{} discards {} from {}.".format(me, card, src.name))

def exile(card, x = 0, y = 0):
  mute()
  src = card.group
  if autoscripts == True and src == table:
    text = trigAbility(card, 'exile', 'Exiled Zone')
    if text != "BREAK":
      notify("{} exiles {}{}.".format(me, card, text))
  else:
    fromText = " from the battlefield" if src == table else " from their " + src.name
    card.moveTo(me.piles['Exiled Zone'])
    notify("{} exiles {}{}.".format(me, card, fromText))

def attack(card, x = 0, y = 0):
  mute()
  if autoscripts == True:
    if card.orientation == Rot90:
      if confirm("Cannot attack: already tapped. Continue?") != True: return
    elif card.highlight == AttackColor or card.highlight == AttackDoesntUntapColor:
      if confirm("Cannot attack: already attacking. Continue?") != True: return
    card.orientation |= Rot90
    if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
      card.highlight = AttackDoesntUntapColor
    else:
      card.highlight = AttackColor
    text = trigAbility(card, 'attack', '')
    if text != "BREAK":
      notify("{} attacks with {}{}.".format(me, card, text))
  else:
    card.orientation |= Rot90
    if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
      card.highlight = AttackDoesntUntapColor
    else:
      card.highlight = AttackColor
    notify('{} attacks with {}'.format(me, card))

def attackWithoutTapping(card, x = 0, y = 0):
  mute()
  if autoscripts == True:
    if card.orientation == Rot90:
      if confirm("Cannot attack: {} is tapped. Continue?".format(card)) != True: return
    elif card.highlight == AttackColor or card.highlight == AttackDoesntUntapColor:
      if confirm("Cannot attack: already attacking. Continue?") != True: return
    if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
      card.highlight = AttackDoesntUntapColor
    else:
      card.highlight = AttackColor
    text = trigAbility(card, 'attack', '')
    if text != "BREAK":
      notify("{} attacks with {}{}.".format(me, card, text))
  else:
    if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
      card.highlight = AttackDoesntUntapColor
    else:
      card.highlight = AttackColor
    notify('{} attacks without tapping with {}'.format(me, card))

def block(card, x = 0, y = 0):
  mute()
  if autoscripts == True:
    if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
      card.highlight = BlockDoesntUntapColor
    else:
      card.highlight = BlockColor
    text = trigAbility(card, 'block', '')
    if text != "BREAK":
      notify("{} blocks with {}{}.".format(me, card, text))
  else:
    if card.highlight in [DoesntUntapColor, AttackDoesntUntapColor, BlockDoesntUntapColor]:
      card.highlight = BlockDoesntUntapColor
    else:
      card.highlight = BlockColor
    notify('{} blocks with {}'.format(me, card))

def activate(card, x = 0, y = 0):
  mute()
  if autoscripts == True:
    num = askInteger("Activate which ability?\n{}".format(getTags(card, 'allactivate')), 1)
    if num == None: return
    text = trigAbility(card, 'activate{}'.format(num), '')
    if text != "BREAK":
      notify("{} activates ability #{} on {}{}.".format(me, num, card, text))
  else:
    notify("{} uses {}'s ability.".format(me, card))

def rulings(card, x = 0, y = 0):
  mute()
  if not card.MultiverseId == None:
    openUrl('http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid={}'.format(card.MultiverseId))

#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def generaltoggle(card, x = 0, y = 0):
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
    for c in cards:
      copy = table.create(c.model, x, y, 1)
      if c.isAlternateImage == True:
        copy.switchImage
      x, y = table.offset(x, y)

def addMarker(cards, x = 0, y = 0):
    mute()
    marker, quantity = askMarker()
    if quantity == 0: return
    for c in cards:
        c.markers[marker] += quantity
        notify("{} adds {} {} counters to {}.".format(me, quantity, marker[0], c))

def addMinusOneMarker(card, x = 0, y = 0):
    mute()
    notify("{} adds a -1/-1 counter to {}.".format(me, card))
    if counters['plusoneplusone'] in card.markers:
        card.markers[counters['plusoneplusone']] -= 1
    else:
        card.markers[counters['minusoneminusone']] += 1

def addPlusOneMarker(card, x = 0, y = 0):
    mute()
    notify("{} adds a +1/+1 counter to {}.".format(me, card))
    if counters['minusoneminusone'] in card.markers:
        card.markers[counters['minusoneminusone']] -= 1
    else:
        card.markers[counters['plusoneplusone']] += 1

def addLoyaltyMarker(card, x = 0, y = 0):
    mute()
    notify("{} adds a Loyalty counter to {}.".format(me, card))
    card.markers[counters['loyalty']] += 1

def addChargeMarker(card, x = 0, y = 0):
    mute()
    notify("{} adds a Charge counter to {}.".format(me, card))
    card.markers[counters['charge']] += 1

def removePlusOneMarker(card, x = 0, y = 0):
    mute()
    addmarker = counters['plusoneplusone']
    if addmarker in card.markers:
      card.markers[addmarker] -= 1
      markername = addmarker[0]
      notify("{} removes a {} from {}".format(me, markername, card))

def removeMinusOneMarker(card, x = 0, y = 0):
    mute()
    addmarker = counters['minusoneminusone']
    if addmarker in card.markers:
      card.markers[addmarker] -= 1
      markername = addmarker[0]
      notify("{} removes a {} from {}".format(me, markername, card))

def removeLoyaltyMarker(card, x = 0, y = 0):
    mute()
    addmarker = counters['loyalty']
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
#movement actions
#---------------------------

def tolibrary(card, x = 0, y = 0):
    mute()
    src = card.group
    fromText = "Battlefield" if src == table else src.name
    notify("{} moves {} from {} to Library.".format(me, card, fromText))
    card.moveTo(me.Library)

def tolibraryposition(card, x = 0, y = 0):
    mute()
    pos = askInteger("Move to what position?\nNOTE: 0 is the top.", 0)
    fromText = "Battlefield" if src == table else src.name
    if pos == None: return
    if pos > len(me.Library):
      notify("{} moves {} from {} to Library (bottom).".format(me, card, fromText))
      card.moveToBottom(me.Library)
    elif pos == 0:
      notify("{} moves {} from {} to Library (top).".format(me, card, fromText))
      card.moveTo(me.Library)
    else:
      notify("{} moves {} from {} to Library ({} from top).".format(me, card, fromText, pos))
      card.moveTo(me.Library, pos)

def tohand(card, x = 0, y = 0):
    mute()
    src = card.group
    if src == table:
      notify("{} moves {} to their hand from the battlefield.".format(me, card))
    else:
      if card.isFaceUp == False:
        if confirm("Reveal {} to all players?".format(card.name)):
          card.isFaceUp = True
          rnd(10,100)
        else:
          card = "a card"
      notify("{} moves {} to their hand from their {}.".format(me, card, src.name))
    card.moveTo(me.hand)

def randomDiscard(group):
    mute()
    card = group.random()
    if card == None: return
    card.isFaceUp = True
    rnd(10,100)
    notify("{} randomly discards {}.".format(me, card))
    card.moveTo(me.Graveyard)

def randomPick(group):
    mute()
    card = group.random()
    if card == None: return
    rnd(10,100)
    notify("{} randomly picks {} from their {}.".format(me, card, group.name))

def mulligan(group):
    mute()
    newCount = len(group) - 1
    if newCount < 0: return
    if not confirm("Mulligan down to %i ?" % newCount): return
    notify("{} mulligans down to {}".format(me, newCount))
    for card in group:
        card.moveTo(me.Library)
    uselessvar = rnd(10, 1000)
    me.Library.shuffle()
    for card in me.Library.top(newCount):
        card.moveTo(me.hand)

def draw(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    card = group[0]
    card.moveTo(me.hand)
    rnd(10,100)
    if re.search(r'Miracle {', card.Rules):
      if confirm("Cast this card for its Miracle cost?\n\n{}\n{}".format(card.name, card.Rules)):
        if autoscripts == True:
          miracletrig = table.create(card.model, 0, 0, 1)
          miracletrig.markers[scriptMarkers['miracle']] += 1
          cstack[miracletrig] = card
          card.highlight = MiracleColor
          cardalign()
        else:
          miracletrig = card
          miracletrig.moveToTable(0,0)
        notify("{} draws {}, triggering the Miracle.".format(me, miracletrig))
        return
    notify("{} draws a card.".format(me))

def drawMany(group, count = None):
    if len(group) == 0: return
    mute()
    if count == None: count = askInteger("Draw how many cards?", 7)
    for c in group.top(count): c.moveTo(me.hand)
    notify("{} draws {} cards.".format(me, count))

def mill(group = me.Library, count = None):
    if len(group) == 0: return
    mute()
    if count == None: count = askInteger("Mill how many cards?", 1)
    for c in group.top(count): c.moveTo(me.Graveyard)
    notify("{} mills top {} cards from Library.".format(me, count))

def exileMany(group = me.Library, count = None):
    if len(group) == 0: return
    mute()
    if count == None: count = askInteger("Exile how many cards?", 1)
    for c in group.top(count): c.moveTo(me.piles['Exiled Zone'])
    notify("{} exiles top {} cards from Library.".format(me, count))

def shuffleIntoLibrary(group = me.Graveyard):
    mute()
    Library = me.Library
    for c in group: c.moveTo(Library)
    rnd(100,1000)
    Library.shuffle()
    notify("{} shuffles {} into Library.".format(me, group.name))

def moveIntoLibrary(group):
    mute()
    Library = me.Library
    for c in group: c.moveTo(Library)
    notify("{} moves all cards from {} into Library.".format(me, group.name))

def revealtoplibrary(group, x = 0, y = 0):
    mute()
    if group[0].isFaceUp:
        notify("{} hides {} from top of Library.".format(me, group[0]))
        group[0].isFaceUp = False
    else:
        group[0].isFaceUp = True
        notify("{} reveals {} from top of Library.".format(me, group[0]))

def exileAll(group):
    mute()
    exiledZone = me.piles['Exiled Zone']
    for c in group: c.moveTo(exiledZone)
    notify("{} exiles all cards from {}".format(me, group.name))