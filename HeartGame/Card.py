CARD_STRING_MAP = {'3S': 1, '8S': 6, '5S': 3, 'JS': 9, '3C': 14, '3H': 27, 'JH': 35, '5H': 29, 'JD': 48, '5D': 42, '5C': 16, 'JC': 22, '9H': 33, '7D': 44, '7C': 18, '9C': 20, 'TS': 8, '7H': 31, '7S': 5, 'TH': 34, 'TD': 47, '3D': 40, 'TC': 21, 'AC': 25, 'AD': 51, '2S': 0, 'AH': 38, '4S': 2, '2D': 39, 'AS': 12, '9D': 46, '4H': 28, '2C': 13, '8H': 32, '4D': 41, '9S': 7, '2H': 26, '4C': 15, 'KC': 24, 'QS': 10, '6C': 17, '6D': 43, 'KD': 50, '6H': 30, '8C': 19, 'KH': 37, '8D': 45, 'KS': 11, 'QC': 23, '6S': 4, 'QD': 49, 'QH': 36}
CARD_STRING_LIST = ['2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD',]
SUIT_VALUE_DICT = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14, "2":2, "3":3, "4":4, "5":5, "6":6,"7":7,"8":8,"9":9}
SUIT_INDEX_DICT = {"S": 0, "C": 1, "H": 2, "D": 3}
VAL_STRING = "AKQJT98765432"

CARD_AH = 'AH'
CARD_2C = '2C'
CARD_TC = 'TC'

H_SCORE_CARDS_MAP = {'2H':-1, '3H':-1, '4H':-1, '5H':-1, '6H':-1, '7H':-1, '8H':-1, '9H':-1, 'TH':-1, 'JH':-1, 'QH':-1, 'KH':-1, 'AH':-1, }
Q_SCORE_CARDS_MAP = {'QS':-13}
ALL_SCORE_CARDS_LIST = list(H_SCORE_CARDS_MAP.keys()) + list(Q_SCORE_CARDS_MAP.keys()) + [CARD_TC, ]


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
        return CARD_STRING_MAP[self.card_string]

    @classmethod
    def cardInstanceIndex(cls, card_string):
        return CARD_STRING_MAP[card_string]

    @classmethod
    def cardStringFromInstanceIndex(cls, index):
        return CARD_STRING_LIST[index]
