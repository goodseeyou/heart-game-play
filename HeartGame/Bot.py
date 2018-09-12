from Player import *
import Card


class Bot:
    def __init__(self, name):
        self.name = name
        self.players_info = None
        self.self_info = None
        self.game_info = None

    def new_game(self, game_info, players_info):
        self.game_info = game_info
        self.players_info = players_info
        for info in players_info:
            if info[KEY_PLAYER_NAME] == self.name:
                self.self_info = info
                break

    def new_deal(self, players_info):
        self.players_info = players_info
        for info in players_info:
            if info[KEY_PLAYER_NAME] == self.name:
                self.self_info = info
                break

    def pass_card(self, game_info, self_info):
        self.game_info = game_info
        for key in self_info:
            self.self_info[key] = self_info[key]

        return self._pass_card()

    def _pass_card(self):
        # TODO
        return self.self_info[KEY_CARDS][:3]

    def receive_opponent_cards(self, sender_info, self_info):
        for i in range(4):
            player = self.players_info[i]
            if player[KEY_PLAYER_NAME] == sender_info[KEY_PLAYER_NAME]:
                break
        self.players_info[i] = sender_info
        for key in self_info:
            self.self_info[key] = self_info[key]

    def pass_end(self, game_info, players_info, self_info):
        self.game_info = game_info
        self.players_info = players_info
        for key in self_info:
            self.self_info[key] = self_info[key]

    def expose_cards(self, self_info):
        for key in self_info:
            self.self_info[key] = self_info[key]
        return self._expose_cards()

    def _expose_cards(self):
        # TODO
        return [Card.CARD_AH]

    def expose_cards_end(self, players_info):
        self.players_info = players_info
        for info in players_info:
            if info[KEY_PLAYER_NAME] == self.name:
                self.self_info = info

    def your_turn(self, game_info, self_info):
        self.game_info = game_info
        for key in self_info:
            self.self_info[key] = self_info[key]

        return self._pick_turn_card()

    def _pick_turn_card(self):
        # TODO
        return self.self_info[KEY_CARDS][0]

    def turn_end(self, game_info, player_info):
        self.game_info = game_info

        for player in self.players_info:
            if player[KEY_PLAYER_NAME] == player_info[KEY_PLAYER_NAME]:
                for key in player_info:
                    player[key] = player_info[key]
                break

    def round_end(self, game_info, players_info):
        self.game_info = game_info
        self.players_info = players_info
        for player in self.players_info:
            if player[KEY_PLAYER_NAME] == self.name:
                self.self_info = player
                break

    def deal_end(self, game_info, players_info):
        self.game_info = game_info
        self.players_info = players_info
        for player in self.players_info:
            if player[KEY_PLAYER_NAME] == self.name:
                self.self_info = player
                break
