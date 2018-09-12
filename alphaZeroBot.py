import Game
from candidate import *

class AlphaZeroBot:
    def __init__(self, name, nn=None, mcts=None):
        self.name = name
        self.nn = nn
        self.mcts = mcts

        self.boardInstance = Game.BoardInstance()
        self.players_list = []
        self.players_dict = dict()
        self.round = None

    def new_game(self, players_name):
        diff_index = -1
        for i in range(4):
            player_name = players_name[i]
            if player_name == self.name:
                diff_index = i
                break

        assert(diff_index >= 0)

        for i in range(4):
            player_name = players_name[i]
            index = (i - diff_index) % 4
            self.players_dict[player_name] = Game.Player(player_name, index)

        players_i_player = sorted([(self.players_dict[player_name].player_index, self.players_dict[player_name])
                                   for player_name in self.players_dict], key=lambda x: x[0])
        for _, player in players_i_player:
            self.players_list.append(player)

    def new_deal(self):
        self.players_list[0].new_deal()
        self.round = Game.RoundState()

    def deal_end(self, players):
        for player in players:
            name, game_score, deal_score = player['playerName'], player['gameScore'], player['dealScore']
            player = self.players_dict[name]
            player.game_score = game_score
            player.deal_score = deal_score

    def receive_cards(self, cards):
        self.players_list[0].receive_cards([Game.Card(card_string) for card_string in cards])

    def receive_opponent_cards(self, sender_name, cards):
        cards = [Game.Card(card_string) for card_string in cards]
        self.players_dict[sender_name].pass_cards(cards)
        self.players_list[0].receive_cards(cards)

    def pass_cards(self, receiver_name):
        receiver = self.players_dict[receiver_name]
        self.round.pass_to_player_index(receiver.player_index)

        cards = self._predict_pass_cards()
        cards_string = list(cards)
        cards = [Game.Card(card_string) for card_string in cards]
        receiver.receive_cards(cards)

        return cards_string

    def _predict_pass_cards(self):
        candidate_cards_index = []
        _last_index = -1
        while len(candidate_cards_index) < 3:
            card_index = self.players_list[0].hand_card_list.index(Game.VAL_YES, _last_index+1)
            candidate_cards_index.append(card_index)
            _last_index = card_index

        cards_to_pass = tuple(Game.CARD_STRING_INSTANCE_INDEX[index] for index in candidate_cards_index)

        pass_candidate_index = PASS_CARD_CANDIDATE.index(cards_to_pass) if self.nn is None else self.nn.predict()
        return PASS_CARD_CANDIDATE[pass_candidate_index]

    def expose_cards(self):
        self.round = self.round.inherit()
        self.round.begin_expose()

        expose_candidate_index = 0 if self.nn is None else self.nn.predict()
        return EXPOSE_CARD_CANDIDATE[expose_candidate_index]

    def expose_cards_end(self, player_name):
        self.players_dict[player_name].expose_card()

    def new_round(self):
        self.round = self.round.inherit()
        self.round.begin_pick()

    def pick_card(self):
        pick_candidate_index = 1 if self.nn is None else self.nn.predict()
        card_string = PICK_CARD_CANDIDATE[pick_candidate_index]
        card = Game.Card(card_string)
        self.players_list[0].pick_card(card)

        return card_string

    def turn_end(self, player_name, card_string):
        cards = Game.Card(card_string)
        self.players_dict[player_name].pick_card(cards)

    def round_end(self, players):
        for player in players:
            player_name, score_cards, deal_score = player['playerName'], player['scoreCards'], player['dealScore']
            player = self.players_dict[player_name]
            player.get_scored_card([Game.Card(card_string) for card_string in score_cards])
            player.deal_score = deal_score






