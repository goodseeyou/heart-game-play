
class AbcBot:
    def __init__(self, botNumber):
        """
        :param botNumber: Unique value during AI contest for player recognition
        """
        self.gameInstance = None
        self.players = {}
        self.botNumber = botNumber

    def new_game(self, players):
        """
        Initiate new Game Sate
        set Player with index
        :return:
        """
        self.gameInstance = GameInstance()
        self._set_players(players)

    def _set_players(self, players):
        for i in range(4):
            if self.botNumber == players[i]['playerNumber']:
                diffIndex = i
                break
        for i in range(4):
            playerNumber = str(players[i]['playerNumber'])
            index = (i - diffIndex) % 4
            self.players[playerNumber] = Player(playerNumber, index)


VAL_PICKED = -1
VAL_NO_OR_UNKNOWN_CARD = 0
VAL_HAVE_CARD = 1
VAL_YES = 1
VAL_NO = 0


class Player:
    def __init__(self, playerNumber, playerIndex):
        """
        :param playerNumber: Unique value during AI contest for player recognition
        :param playerIndex: The order in the game according to self player
        """
        self.playerNumber = playerNumber
        self.playerIndex = playerIndex
        self.gameScore = 0
        self.dealScore = 0
        self.exposeAH = VAL_NO
        self.handCards = getCardsArray()

    def receivedCards(self, cards):
        for card in cards:
            self.handCards[card.instanceIndex] = VAL_HAVE_CARD

    def passCards(self, cards):
        for card in cards:
            self.pickCard(card)

    def pickCard(self, card):
        self.handCards[card.instanceIndex] = VAL_PICKED

    def exposeCardAH(self):
        self.exposeAH = VAL_YES

    def resetDeal(self):
        self.dealScore = 0
        self.exposeAH = VAL_NO
        self.handCards = getCardsArray()

    def copy(self):
        _p = Player(self.playerNumber, self.playerIndex)
        _p.gameScore, _p.dealScore, _p.exposeAH, _p.handCards = \
            self.gameScore, self.dealScore, self.exposeAH, self.handCards[:]
        return _p


class Round:
    def __init__(self):
        """
        roundState: True/False (1/0) list for [begin round, to pass card to player index 1,2,3]
        firstCardInRound: The first card picked by the first player, roundState[0] should be YES
        """
        self.roundState = [VAL_NO]*4
        self.firstCardInRound = None

    def stateBeginRound(self):
        self.roundState[0] = VAL_YES

    def passCardToPlayer(self, player):
        self.roundState[player.playerIndex] = VAL_YES

    def setFirstCard(self, card):
        self.firstCardInRound = card

    def copy(self):
        _r = Round()
        _r.roundState, _r.firstCardInRound = self.roundState[:], self.firstCardInRound
        return _r


LEN_STATE_HISTORY = 16
LEN_ROUND_INSTANCE = 4+4+4+4+52+52+52+52+52


class RoundInstance:
    def __init__(self, roundNumber, instance):
        self.roundNumber = roundNumber
        self.instance = instance


from collections import deque


class GameInstance:
    def __init__(self):
        self.roundInstances = deque([], LEN_STATE_HISTORY)
        self.gameInstance = [VAL_NO] * LEN_ROUND_INSTANCE * LEN_STATE_HISTORY

    def addNewRoundInstance(self, roundInstance):
        self.roundInstances.appendleft(roundInstance)
        self.gameInstance = self.gameInstance[:-LEN_ROUND_INSTANCE]
        self.gameInstance += self.roundInstances



def genRoundInstance(_round, players):
    gameScore = [player.gameScore for player in players]
    dealScore = [player.dealScore for player in players]
    exposeAH = [player.exposeAH for player in players]
    roundState = _round.roundState
    roundFirstCard = getCardsArray(_round.firstCardInRound)
    playersHandCards = [player.handCards for player in players]

    _instance = gameScore + dealScore + exposeAH + roundState + roundFirstCard + \
        playersHandCards[0] + playersHandCards[1] + playersHandCards[2] + playersHandCards[3]

    return _instance


EMPTY_CARDS = [VAL_NO_OR_UNKNOWN_CARD]*52


def getCardsArray(card=None):
    if card is None:
        return EMPTY_CARDS[:]
    _tmp = EMPTY_CARDS[:]
    _tmp[card.instanceIndex] = VAL_YES
    return _tmp
