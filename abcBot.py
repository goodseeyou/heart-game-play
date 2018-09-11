from Card import Card

# action number for passing card
NUM_C52_3 = 22100
# action number for expose AH card
NUM_C2_1 = 2
# action number for select card
NUM_C52_1 = 52

NUM_TOTAL_ACTION = NUM_C52_3 + NUM_C2_1 + NUM_C52_1

class AbcBot:
    def __init__(self, botName, nn, mcts):
        """
        :param botName: bot name during AI contest for player recognition
        """
        self.gameInstance = GameInstance()
        self.playersDict = {}
        self.playersList = []
        self.botName = botName
        self.currentRound = None
        self.nn = nn
        self.mcts = mcts
        self.trainGameInstances = []

    def new_game(self):
        self.trainGameInstances = []

    def init_players(self, server_players):
        self.len_players = len(server_players)
        for i in range(self.len_players):
            if self.botName == server_players[i]['playerName']:
                diffIndex = i
                break
        for i in range(self.len_players):
            playerName = str(server_players[i]['playerName'])
            index = (i - diffIndex) % 4
            player = Player(playerName, index)
            player.gameScore = server_players[i]['gameScore']
            player.dealScore = server_players[i]['dealScore']
            self.playersDict[playerName] = player

        _players_i_p = sorted([(self.playersDict[playerName].playerIndex, self.playersDict[playerName]) for playerName in self.playersDict], key=lambda x: x[0])
        for i, p in _players_i_p:
            self.playersList.append(p)

    def receive_cards(self, self_cards):
        for cardString in self_cards:
            self.playersDict[self.botName].handCards[Card.cardInstanceIndex(cardString)] = 1

    def receive_opponent_cards(self, cards):
        self.receive_cards(cards)

    def _get_player(self, playerName):
        return self.playersDict[str(playerName)]

    def pass_cards(self, receiverPlayerName):
        self.currentRound = Round()
        receiver = self._get_player(receiverPlayerName)
        self.currentRound.passCardToPlayer(receiver)
        roundInstance = genRoundInstance(self.currentRound, self.playersList)
        gameInstance = self.gameInstance.addNewRoundInstance(roundInstance)

        cardStringList = self._predict_pass_cards(gameInstance)
        CardList = [Card(cardString) for cardString in cardStringList]
        self.playersList[0].pass_cards(CardList)
        return cardStringList

    # TODO
    def _predict_pass_cards(self, gameInstance):
        print 'pass card', gameInstance.roundInstances[0]
        self.trainGameInstances.append(gameInstance.gameInstance)
        return ["AH"] * 3

    def receive_opponent_cards(self, cardStringList):
        self.playersList[0].received_cards([Card(cardString) for cardString in cardStringList])

    def expose_my_cards(self):
        self.currentRound = self.currentRound.newRound()
        roundInstance = genRoundInstance(self.currentRound, self.playersList)
        gameInstance = self.gameInstance.addNewRoundInstance(roundInstance)

        cardStringList = self._predict_expose_cards(gameInstance)
        if cardStringList:
            self.playersList[0].expose_card()

        return cardStringList

    # TODO
    def _predict_expose_cards(self, gameInstance):
        print 'expose card', gameInstance.roundInstances[0]
        self.trainGameInstances.append(gameInstance.gameInstance)
        return ["AH"]
        pass

    def expose_cards_end(self, server_players):
        for server_player in server_players:
            if server_player['exposedCards']:
                self._get_player(server_player['playerName']).expose_card()

    def new_round(self, server_players):
        self.currentRound = self.currentRound.newRound()
        self.currentRound.stateBeginRound()
        for server_player in server_players:
            player = self._get_player(server_player['playerName'])
            player.gameScore = server_player['gameScore']
            player.dealScore = server_player['dealScore']

    def turn_end(self, data):
        first_player = data['roundPlayers'][0]
        turn_player = data['turnPlayer']
        turn_card_string = data['turnCard']
        turnCard = Card(turn_card_string)

        if first_player == turn_player:
            self.currentRound.setFirstCard(turnCard)

        self._get_player(turn_player).pick_card(turnCard)

    def select_card(self):
        roundInstance = genRoundInstance(self.currentRound, self.playersList)
        gameInstance = self.gameInstance.addNewRoundInstance(roundInstance)
        selectCardString = self._predict_pick_card(gameInstance)
        self.playersList[0].pick_card(Card(selectCardString))

        return selectCardString

    # TODO
    def _predict_pick_card(self, gameInstance):
        print 'pick card', gameInstance.roundInstances[0]
        self.trainGameInstances.append(gameInstance.gameInstance)
        return "AH"
        pass

    def game_over(self, server_players):
        for server_player in server_players:
            player = self._get_player(server_player['playerName'])
            player.gameScore = server_player['gameScore']
            if 1 == server_player['rank']:
                winner = player.playerIndex

        label = winner == 0
        for i in self.trainGameInstances:
            print '%s\t%s'%(label, i)

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

    def newRound(self):
        _r = Round()
        _r.roundState, _r.firstCardInRound = self.roundState[:], None
        return _r





