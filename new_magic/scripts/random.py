# A Replacement for the Random module that runs locally in iron python

seed = 0, 0, 0

def localRandom():
    global seed
    x, y, z = seed
    if 0 == x == y == z:
        import time
        t = long(time.time() * 256)
        t = int((t&0xffffff) ^ (t>>24))
        t, x = divmod(t, 256)
        t, y = divmod(t, 256)
        t, z = divmod(t, 256)
        # Zero is a poor seed, so substitute 1
        seed = (x or 1, y or 1, z or 1)
        x, y, z = seed
    x = (171 * x) % 30269
    y = (172 * y) % 30307
    z = (170 * z) % 30323
    seed = x, y, z
    return (x/30269.0 + y/30307.0 + z/30323.0) % 1.0

def riffleShuffle(deck):
    mute()
    topChunk = deck[:len(deck)/2] ##Grabs the top half of the deck
    bottomChunk = deck[len(deck)/2:] ##Grabs the bottom half of the deck
    newDeck = []
    while len(bottomChunk) > 0: ##keep looping as long as there's still cards
        if localRandom() > 0.5:
            newDeck.insert(0, bottomChunk.pop()) ##The bottom of the chunk gets added to the top of the deck
            if len(topChunk) > 0: ##The bottom chunk will always have 1 more card if the deck was odd-numbered, due to rounding
                newDeck.insert(0, topChunk.pop())
        else:
            if len(topChunk) > 0: ##The bottom chunk will always have 1 more card if the deck was odd-numbered, due to rounding
                newDeck.insert(0, topChunk.pop())
            newDeck.insert(0, bottomChunk.pop()) ##The bottom of the chunk gets added to the top of the deck
    return newDeck

def pileShuffle(deck, pileCount = None):
    mute()
    piles = []
    if pileCount == None:
        pileCount = askInteger('How many piles?', 5) ##default is 5 piles
    for num in xrange(0, pileCount): ##loops from 0 to 4, each one being the starting index of the list
        piles.append(deck[num::pileCount]) ## Distributes the cards into the specified number of piles
    newDeck = []
    while len(piles) > 0:  ##Now we'll randomly stack the piles together
        rndPile = piles.pop(int(localRandom() * len(piles)))  ##Choose a random pile (index) in the list of piles
        newDeck += rndPile ##Add the random pile to the deck
    return newDeck