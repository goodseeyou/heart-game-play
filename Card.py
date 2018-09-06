INSTANCE_INDEX_MAP_DICT = {'3S': 1, '8S': 6, '5S': 3, 'JS': 9, '3C': 14, '3H': 27, 'JH': 35, '5H': 29, 'JD': 48, '5D': 42, '5C': 16, 'JC': 22, '9H': 33, '7D': 44, '7C': 18, '9C': 20, 'TS': 8, '7H': 31, '7S': 5, 'TH': 34, 'TD': 47, '3D': 40, 'TC': 21, 'AC': 25, 'AD': 51, '2S': 0, 'AH': 38, '4S': 2, '2D': 39, 'AS': 12, '9D': 46, '4H': 28, '2C': 13, '8H': 32, '4D': 41, '9S': 7, '2H': 26, '4C': 15, 'KC': 24, 'QS': 10, '6C': 17, '6D': 43, 'KD': 50, '6H': 30, '8C': 19, 'KH': 37, '8D': 45, 'KS': 11, 'QC': 23, '6S': 4, 'QD': 49, 'QH': 36}
SUIT_VALUE_DICT = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9}
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
