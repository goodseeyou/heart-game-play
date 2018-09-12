import mock
import Card

KEY_PLAYER_NAME = 'playerName'
KEY_PLAYER_NUMBER = 'playerNumber'
KEY_GAME_SCORE = 'gameScore'
KEY_DEAL_SCORE = 'dealScore'
KEY_SCORE_CARDS = 'scoreCards'
KEY_CARDS = 'cards'
KEY_CARDS_COUNT = 'cardsCount'
KEY_PICKED_CARDS = 'pickedCards'
KEY_RECEIVED_CARDS = 'receivedCards'
KEY_CANDIDATE_CARDS = 'candidateCards'
KEY_RECEIVED_FROM = 'receivedFrom'
KEY_EXPOSED_CARDS = 'exposedCards'
KEY_SHOOTING_THE_MOON = 'shootingTheMoon'
KEY_ROUND_CARD = 'roundCard'


class Player:
    def __init__(self, player_name, player_number, bot):
        self.info = {
            KEY_PLAYER_NAME: player_name,
            KEY_PLAYER_NUMBER: player_number,
            KEY_GAME_SCORE: 0,
            KEY_DEAL_SCORE: 0,
            KEY_SCORE_CARDS: [],
            KEY_CARDS: [],
            KEY_CARDS_COUNT: 0,
            KEY_PICKED_CARDS: [],
            KEY_CANDIDATE_CARDS: [],
            KEY_RECEIVED_CARDS: [],
            KEY_RECEIVED_FROM: '',
            KEY_EXPOSED_CARDS: [],
            KEY_SHOOTING_THE_MOON: False,
            KEY_ROUND_CARD: ''
        }
        self.bot = bot

    def reset_deal(self):
        self.info[KEY_SCORE_CARDS] = []
        self.info[KEY_CARDS] = []
        self.info[KEY_CARDS_COUNT] = 0
        self.info[KEY_PICKED_CARDS] = []
        self.info[KEY_CANDIDATE_CARDS] = []
        self.info[KEY_RECEIVED_CARDS] = []
        self.info[KEY_RECEIVED_FROM] = ''
        self.info[KEY_EXPOSED_CARDS] = []
        self.info[KEY_SHOOTING_THE_MOON] = False
        self.info[KEY_ROUND_CARD] = ''

    def pick_cards(self, cards):
        self.info[KEY_PICKED_CARDS] += cards
        self.remove_cards(cards)

    def receive_opponent_cards(self, sender_name, cards):
        self.info[KEY_RECEIVED_CARDS] += cards
        self.info[KEY_RECEIVED_FROM] = sender_name
        self.add_cards(cards)

    def add_cards(self, cards):
        for card in cards:
            self.info[KEY_CARDS].append(card)
        self.info[KEY_CARDS_COUNT] = len(self.info[KEY_CARDS])

    def remove_cards(self, cards):
        for card in cards:
            index = self.info[KEY_CARDS].index(card)
            self.info[KEY_CARDS].pop(index)
        self.info[KEY_CARDS_COUNT] = len(self.info[KEY_CARDS])

    def expose_cards(self, cards):
        self.info[KEY_EXPOSED_CARDS] += cards

    def assign_score_cards(self, cards):
        self.info[KEY_SCORE_CARDS] += [card for card in cards if card in Card.ALL_SCORE_CARDS_LIST]

    def update_deal_score(self, does_exposed):
        multiple_AH = 2 if does_exposed else 1
        multiple_TC = 2 if Card.CARD_TC in self.info[KEY_SCORE_CARDS] else 1
        self.info[KEY_DEAL_SCORE] = \
            sum([Card.Q_SCORE_CARDS_MAP.get(card, 0) * multiple_TC for card in self.info[KEY_SCORE_CARDS]]) + \
            sum([Card.H_SCORE_CARDS_MAP.get(card, 0) * multiple_AH * multiple_TC for card in self.info[KEY_SCORE_CARDS]])
        if all([card in self.info[KEY_SCORE_CARDS] for card in Card.ALL_SCORE_CARDS_LIST]):
            self.info[KEY_DEAL_SCORE] = abs(self.info[KEY_DEAL_SCORE]) * 4
            self.info[KEY_SHOOTING_THE_MOON] = True
