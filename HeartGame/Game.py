from random import shuffle
from copy import deepcopy
from Player import *
import Card

MAP_PASS_CARD_TARGET_DELTA = [1, 3, 2, 0]

KEY_ROUND_NUMBER = 'roundNumber'
KEY_DEAL_NUMBER = 'dealNumber'
KEY_GAME_NUMBER = 'gameNumber'
KEY_ROUND_PLAYERS = 'roundPlayers'
KEY_TURN_PLAYER = 'turnPlayer'
KEY_TURN_CARD = 'turnCard'


class Game:
    def __init__(self, players):
        self.players = players
        self.info = {
            KEY_ROUND_NUMBER: 0,
            KEY_DEAL_NUMBER: 0,
            KEY_GAME_NUMBER: 0,
            KEY_ROUND_PLAYERS: [],
            KEY_TURN_PLAYER: '',
            KEY_TURN_CARD: '',
        }
        self.first_player_index = None
        self.round_card_records = []
        self.does_exposed = False

    # Assign order of players
    def new_game(self):
        self.info[KEY_GAME_NUMBER] += 1
        for player in self.players:
            player.bot.new_game(deepcopy(self.info), [deepcopy(player.info) for player in self.players])

    # deal cards to players
    # update deal score and game score
    def new_deal(self):
        self.info[KEY_DEAL_NUMBER] += 1
        self.info[KEY_ROUND_NUMBER] = 0
        self.does_exposed = False

        cards = Card.CARD_STRING_LIST[:]
        shuffle(cards)
        for i in range(4):
            player_cards = sorted(cards[i * 13:i * 13 + 13])

            self.players[i].reset_deal()
            player_info = self.players[i].info
            player_info[KEY_CARDS] = player_cards
            player_info[KEY_CARDS_COUNT] = len(player_info[KEY_CARDS])

            self.players[i].bot.new_deal([deepcopy(player.info) for player in self.players])

    # step of passing card
    def pass_card(self):
        """
        including asking player to pass cards, and notify player with received cards
        """
        delta = MAP_PASS_CARD_TARGET_DELTA[self.info[KEY_DEAL_NUMBER] - 1]
        if delta == 0:
            return

        tmp_records = []
        for i in range(4):
            sender = self.players[i]
            receiver = self.players[(i+delta) % 4]
            pass_cards = sender.bot.pass_card(deepcopy(self.info), deepcopy(sender.info))
            tmp_records.append((sender, pass_cards, receiver,))

        for sender, pass_cards, receiver in tmp_records:
            sender.remove_cards(pass_cards)
            receiver.add_cards(pass_cards)
            receiver.bot.receive_opponent_cards(deepcopy(sender.info), deepcopy(receiver.info))

    def pass_end(self):
        for player in self.players:
            player.bot.pass_end(deepcopy(self.info),
                                [deepcopy(player.info) for player in self.players],
                                deepcopy(player.info))

    def expose_cards(self):
        exposed_cards = None
        for player in self.players:
            if Card.CARD_AH in player.info[KEY_CARDS]:
                exposed_cards = player.bot.expose_cards(deepcopy(player.info))
                player.expose_cards(exposed_cards)
                if exposed_cards:
                    self.does_exposed = True
                break
        assert(exposed_cards is not None)

    def expose_cards_end(self):
        for player in self.players:
            player.bot.expose_cards_end([deepcopy(player.info) for player in self.players])

    def new_round(self):
        self.info[KEY_ROUND_NUMBER] += 1
        self.round_card_records = []

        if self.info[KEY_ROUND_NUMBER] == 1:
            for i in range(4):
                if Card.CARD_2C in self.players[i].info[KEY_CARDS]:
                    self.first_player_index = i
                    break
        self.info[KEY_ROUND_PLAYERS] = \
            [self.players[(i+self.first_player_index) % 4].info[KEY_PLAYER_NAME] for i in range(4)]

        for i in range(4):
            turn_player = self.players[(i+self.first_player_index) % 4]
            self.info[KEY_TURN_PLAYER] = turn_player.info[KEY_PLAYER_NAME]

            turn_card = self._your_turn(turn_player)
            self.info[KEY_TURN_CARD] = turn_card
            self.round_card_records.append((turn_player, turn_card, ))

            for notify_payer in self.players:
                self._turn_end(notify_payer)

    def _your_turn(self, player):
        # TODO candidate cards

        turn_card = player.bot.your_turn(deepcopy(self.info), deepcopy(player.info))
        player.pick_cards([turn_card])
        return turn_card

    def _turn_end(self, player):
        player.bot.turn_end(deepcopy(self.info), deepcopy(player.info))

    # calculate score card and notify
    def round_end(self):
        self._assign_score_cards()
        self.players[self.first_player_index].update_deal_score(self.does_exposed)
        for player in self.players:
            player.bot.round_end(deepcopy(self.info), [deepcopy(player.info) for player in self.players])

    def _assign_score_cards(self):
        cards = []
        target_card = None

        for player, card_string in self.round_card_records:
            cards.append(card_string)

            card = Card.Card(card_string)
            if target_card is None:
                target_card = card
                continue

            if card.suit == target_card.suit and card.value > target_card.value:
                self.first_player_index = self.players.index(player)

        self.players[self.first_player_index].assign_score_cards(cards)

    def deal_end(self):
        for player in self.players:
            player_info = player.info
            player_info[KEY_GAME_SCORE] += player_info[KEY_DEAL_SCORE]
            player_info[KEY_DEAL_SCORE] = 0

        for player in self.players:
            player.bot.deal_end(deepcopy(self.info), [deepcopy(player.info) for player in self.players])

    def game_end(self):
        # TODO
        pass
