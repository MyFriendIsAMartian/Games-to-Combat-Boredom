import random

cards = {
    "Spades" : ["A♠︎", "2♠︎", "3♠︎", "4︎︎♠︎", "5♠︎", "6♠︎", "7♠︎", "8♠︎", "9♠︎", "10♠︎", "J♠︎", "Q♠︎", "K♠︎"],
    "Diamonds" : ["A♦︎", "2♦︎", "3♦︎", "4︎♦︎", "5♦︎", "6♦︎", "7♦︎︎", "8♦︎", "9♦︎", "10♦︎", "J♦︎", "Q♦︎", "K♦︎"],
    "Clubs" : ["A♣︎", "2♣︎", "3♣︎︎", "4︎♣︎", "5♣︎", "6♣︎︎", "7♣︎", "8♣︎", "9♣︎", "10♣︎", "J♣︎", "Q♣︎", "K♣︎"],
    "Hearts" : ["A♥︎", "2♥︎", "3♥︎", "4︎︎♥︎", "5♥︎︎", "6♥︎", "7♥︎", "8♥︎", "9♥︎︎", "10♥︎", "J♥︎", "Q♥︎", "K♥︎"]
}

ranks = {
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "10" : 10,
    "J" : 11,
    "Q" : 12,
    "K" : 13,
    "A" : 14,
}


def createGame():
    initiate = input("Do you wish to initiate a new game? (Y/N): ")
    if initiate.lower() in ["y", "yes"]:
        playerName = input("\nPlease enter your name here: ")
        print("\nHow many AI players do you wish to add? You need a minimum of 1 player, but can have up to 9 others.")
        try:
            players = int(input("Enter the number of players you wish to add (#): "))
            if players < 1 or players > 10:
                print("Please enter a valid number of players.")
                return
        except ValueError:
            print("Please input a number.")
            return
        numPlayers = players + 1
        deck = shuffleDeck()
        if not countCardsLeft(deck, players):
            print("There aren't enough cards left to start a new round. Reshuffling Deck.")
            return
        players = [createPlayer(playerID = 1, playerName = playerName)]
        for i in range(2, numPlayers + 1):
            players.append(createPlayer(playerID=i, playerName="Player " + str(i)))
        dealInitialCards(deck, players)
        for player in players:
            print(f"Player {player['Player ID']}'s hand: {player['Player Hand']}")


def createPlayer(playerID, playerName):
    player = {
        "Player ID" : "Player " + str(playerID),
        "Player Name" : playerName,
        "Player Hand" : []
    }
    return player


def shuffleDeck():
    deck = []
    for suit, cardList in cards.items():
        deck.extend(cardList)
    random.shuffle(deck)
    return deck


def dealInitialCards(deck, players):
    for i in range(2):
        for player in players:
            player["Player Hand"].append(deck.pop(0))


def countCardsLeft(deck, players):
    required = 2 * players + 5
    return len(deck) >= required


def extractRank(card):
    return card[:-2].strip()


def extractSuit(card):
    return card[-2:]


def getCardValue(card):
    rank = extractRank(card)
    return ranks.get(rank, 0)


def isFlush(cards):
    suits = {}
    for card in cards:
        suit = extractSuit(card)
        suits.setdefault(suit, []).append(card)

    for suitCards in suits.values():
        if len(suitCards) >= 5:
            # Sort and return the top 5 highest cards by rank
            sortedFlush = sorted(suitCards, key=getCardValue, reverse=True)
            return True, sortedFlush[:5]

    return False, []


def isStraight(cards):
    values = sorted(set(getCardValue(card) for card in cards), reverse=True)
    if 14 in values:
        values.append(1)
    for i in range(len(values)-4):
        window = values[i:i+5]
        if window[0] - window[4] == 4 and len(window) == 5:
            return True, window
    return False, []


def getMultiples(cards):
    rankCounts = {}
    for card in cards:
        rank = extractRank(card)
        if rank not in rankCounts:
            rankCounts[rank] = [card]
        else:
            rankCounts[rank].append(card)
    pairs = []
    threes = []
    fours = []
    for rank in rankCounts:
        count = len(rankCounts[rank])
        if count == 4:
            fours.append(rank)
        elif count == 3:
            threes.append(rank)
        elif count == 2:
            pairs.append(rank)
    pairs.sort(key=lambda r: ranks[r], reverse=True)
    threes.sort(key=lambda r: ranks[r], reverse=True)
    fours.sort(key=lambda r: ranks[r], reverse=True)
    return {
        "pairs": pairs,
        "threes": threes,
        "fours": fours,
        "rank_groups": rankCounts
    }


def isFullHouse(multiples):
    threes = multiples["threes"]
    pairs = multiples["pairs"]
    if len(threes) >= 1:
        if len(pairs) >= 1 or len(threes) >= 2:
            bestThree = threes[0]
            # Use second three as pair if needed
            bestPair = pairs[0] if pairs else threes[1]
            return True, (bestThree, bestPair)
    return False, ()


def isStraightFlush(cards):
    flush, flushCards = isFlush(cards)
    if not flush:
        return False, []

    straight, straightValues = isStraight(flushCards)
    if straight:
        return True, straightValues
    return False, []


def isRoyalFlush(cards):
    straightFlush, values = isStraightFlush(cards)
    if straightFlush and max(values) == 14:
        return True
    return False


#createGame()
