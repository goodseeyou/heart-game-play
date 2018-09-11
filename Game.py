from collections import deque

VAL_PICKED = -1
VAL_NO_OR_UNKNOWN_CARD = 0
VAL_HAVE_CARD = 1
VAL_YES = 1
VAL_NO = 0

EMPTY_CARDS = [VAL_NO_OR_UNKNOWN_CARD]*52
EMPTY_ROUND_HEADER = [0] * 4


class Player:
    def __init__(self, play_name, _play_index):
        """
        :param play_name: Unique value during AI contest for player recognition
        :param _play_index: The order in the game according to self player
        """
        self.player_name = play_name
        self.player_index = _play_index
        self.game_score = 0
        self.deal_score = 0
        self.does_expose = VAL_NO
        self.hand_card_list = get_cards_array()

    def received_cards(self, cards):
        for card in cards:
            self.hand_card_list[card.instanceIndex] = VAL_HAVE_CARD

    def pass_cards(self, cards):
        for card in cards:
            self.pick_card(card)

    def pick_card(self, card):
        self.hand_card_list[card.instanceIndex] = VAL_PICKED

    def expose_card(self):
        self.does_expose = VAL_YES

    def new_deal(self):
        self.deal_score = 0
        self.does_expose = VAL_NO
        self.hand_card_list = get_cards_array()

    def copy(self):
        _p = Player(self.player_name, self.player_index)
        _p.game_score, _p.deal_score, _p.does_expose, _p.hand_card_list = \
            self.game_score, self.deal_score, self.does_expose, self.hand_card_list[:]
        return _p


class RoundState:
    def __init__(self):
        """
        passing: value v while passing card to player which has index v, when v > 0
        picking: 1 if begin picking card
        """
        self.passing = VAL_NO
        self.picking = VAL_NO
        self.first_cards = get_cards_array()

    def header(self):
        """
        bit 1: picking (0/1)
        bit 2: pass to player 1 (0/1)
        bit 3: pass to player 2 (0/1)
        bit 4: pass to player 3 (0/1)
        bit 5~57: first picked card in round
        :return: list of binary
        """
        header = EMPTY_ROUND_HEADER[:]
        header[self.passing] = VAL_YES
        header[0] = self.picking
        header += self.first_cards
        return header

    def pass_to_player_index(self, _index):
        self.passing = _index

    def begin_pick(self):
        self.picking = VAL_YES

    def inherit(self):
        rs = RoundState()
        rs.passing, rs.picking = self.passing, self.picking
        return rs

    def copy(self):
        rs = RoundState()
        rs.passing, rs.picking = self.passing, self.picking
        rs.first_cards = rs.first_cards[:]
        return rs


class BoardInstance:
    LEN_STATE_HISTORY = 16
    LEN_ROUND_STATE_INSTANCE = 4+52
    LEN_PLAYER_INSTANCE = 1+1+1+52
    LEN_BOARD_SIZE = LEN_STATE_HISTORY * (LEN_ROUND_STATE_INSTANCE + LEN_PLAYER_INSTANCE)

    def __init__(self):
        self.board = deque([], BoardInstance.LEN_STATE_HISTORY)

    def record_round(self, round_state, players):
        self.board.pop()
        self.board.appendleft((round_state.copy(), players.copy(), ))

    def to_array(self):
        _array = []
        for round_state, players in self.board:
            _array += BoardInstance.round_to_array(round_state, players)
        # append 0 postfix
        _array += [0]*(self.LEN_BOARD_SIZE - len(_array))
        return _array

    @classmethod
    def round_to_array(cls, round_state, players):
        round_state.header()

        _players_instance = []
        for player in players:
            _players_instance.append([player.player_index, player.game_score, player.deal_score, player.does_expose]
                                     + player.hand_card_list)

        players_instance = []
        for pi in sorted(_players_instance, key=lambda x: x[0]):
            players_instance += pi[1:]

        return round_state + players_instance

    @classmethod
    def array_to_round(cls, _array):
        round_state_instance = _array[:cls.LEN_ROUND_STATE_INSTANCE]
        round_state = RoundState()
        round_state.picking = round_state_instance[0]
        for i in range(1, 3):
            if round_state_instance[i] == VAL_YES:
                round_state.passing = VAL_YES
                break
        first_cards = round_state[4:56]
        round_state.first_cards = first_cards

        players_instance = _array[cls.LEN_ROUND_STATE_INSTANCE:]
        players = []
        for i in range(4):
            pi = players_instance[i*cls.LEN_PLAYER_INSTANCE:(i+1)*cls.LEN_PLAYER_INSTANCE]
            player = Player(str(i), i)
            game_score = pi[0]
            deal_score = pi[1]
            does_expose = pi[2]
            hand_cards = pi[3:55]
            player.hand_card_list = hand_cards
            player.does_expose = does_expose
            player.deal_score = deal_score
            player.game_score = game_score
            players.append(player)

        return round_state, players


INSTANCE_INDEX_MAP_DICT = {'3S': 1, '8S': 6, '5S': 3, 'JS': 9, '3C': 14, '3H': 27, 'JH': 35, '5H': 29, 'JD': 48, '5D': 42, '5C': 16, 'JC': 22, '9H': 33, '7D': 44, '7C': 18, '9C': 20, 'TS': 8, '7H': 31, '7S': 5, 'TH': 34, 'TD': 47, '3D': 40, 'TC': 21, 'AC': 25, 'AD': 51, '2S': 0, 'AH': 38, '4S': 2, '2D': 39, 'AS': 12, '9D': 46, '4H': 28, '2C': 13, '8H': 32, '4D': 41, '9S': 7, '2H': 26, '4C': 15, 'KC': 24, 'QS': 10, '6C': 17, '6D': 43, 'KD': 50, '6H': 30, '8C': 19, 'KH': 37, '8D': 45, 'KS': 11, 'QC': 23, '6S': 4, 'QD': 49, 'QH': 36}
CARD_STRING_INSTANCE_INDEX = ('2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD',)
SUIT_VALUE_DICT = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14, "2":2, "3":3, "4":4, "5":5, "6":6,"7":7,"8":8,"9":9}
SUIT_INDEX_DICT = {"S": 0, "C": 1, "H": 2, "D": 3}
VAL_STRING = "AKQJT98765432"


class Card:
    # Takes in strings of the format: "AS", "TC", "6D"
    def __init__(self, card_string):
        self.card_string = card_string
        value, self.suit = card_string[0], card_string[1]
        self.value = SUIT_VALUE_DICT[value]
        self.suit_index = SUIT_INDEX_DICT[self.suit]

    def __str__(self):
        return VAL_STRING[14 - self.value] + self.suit

    def toString(self):
        return VAL_STRING[14 - self.value] + self.suit

    def __repr__(self):
        return VAL_STRING[14 - self.value] + self.suit

    def __eq__(self, other):
        if self is None:
            return other is None
        elif other is None:
            return False
        return self.value == other.value and self.suit == other.suit

    def __hash__(self):
        return hash(self.value.__hash__()+self.suit.__hash__())

    @property
    def instanceIndex(self):
        return INSTANCE_INDEX_MAP_DICT[self.card_string]

    @classmethod
    def cardInstanceIndex(cls, card_string):
        return INSTANCE_INDEX_MAP_DICT[card_string]

    @classmethod
    def cardStringFromInstanceIndex(cls, index):
        return CARD_STRING_INSTANCE_INDEX[index]


def get_cards_array(card=None):
    if card is None:
        return EMPTY_CARDS[:]
    _tmp = EMPTY_CARDS[:]
    _tmp[card.instanceIndex] = VAL_YES
    return _tmp
