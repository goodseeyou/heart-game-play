from Game import *
from Player import *
import Card
from copy import deepcopy

EMPTY_CARDS_INSTANCE = [0] * 52
EMPTY_ACTION_INSTANCE = [0] * 4
EMPTY_DEAL_NUMBER_INSTANCE = [0] * 4
LEN_EMPTY_DEAL_NUMBER_INSTANCE = len(EMPTY_DEAL_NUMBER_INSTANCE)
LEN_EMPTY_ACTION_INSTANCE = len(EMPTY_ACTION_INSTANCE)
LEN_EMPTY_CARDS_INSTANCE = len(EMPTY_CARDS_INSTANCE)
VAL_PICKED = -1
VAL_NO_OR_UNKNOWN_CARD = 0
VAL_HAVE_CARD = 1
VAL_YES = 1
VAL_NO = 0


class Bot:
    def __init__(self, name):
        self.gameInstance = GameInstance(16)
        self.name = name
        self.players_info = None
        self.self_info = None
        self.game_info = None
        self.is_winner = None

    def new_game(self, game_info, players_info):
        self.gameInstance.new_game()
        self.is_winner = None
        self.game_info = game_info
        self.players_info = players_info
        for info in players_info:
            if info[KEY_PLAYER_NAME] == self.name:
                self.self_info = info
                break

    def new_deal(self, players_info):
        self.is_winner = None
        self.players_info = players_info
        for info in players_info:
            if info[KEY_PLAYER_NAME] == self.name:
                self.self_info = info
                break

    def pass_cards(self, game_info, self_info):
        self.game_info.update(game_info)
        self.self_info.update(self_info)

        return self._pass_cards(game_info[KEY_RECEIVER])

    def _pass_cards(self, receiver_name):
        # TODO
        state_instance = StateInstance(self.name, KEY_ACTION_PASS, self.game_info, self.players_info, self.is_winner)
        print(self.name, StateInstance.from_instance(state_instance.instance[:]))
        self.gameInstance.add_state(state_instance)
        #print self.gameInstance.instance[-10:]

        pass_cards = self.self_info[KEY_CANDIDATE_CARDS][:3]

        Bot.record_picked_cards(self.self_info, pass_cards)
        for player in self.players_info:
            if player[KEY_PLAYER_NAME] == receiver_name:
                player[KEY_CARDS] = player.get(KEY_CARDS, []) + pass_cards
                break

        return pass_cards

    def receive_opponent_cards(self, self_info):
        self.self_info.update(self_info)
        received_cards = self.self_info[KEY_RECEIVED_CARDS]

        sender_name = self.self_info[KEY_RECEIVED_FROM]
        for player in self.players_info:
            if player[KEY_PLAYER_NAME] == sender_name:
                Bot.record_picked_cards(player, received_cards)

    def pass_end(self, game_info, players_info, self_info):
        self.game_info.update(game_info)
        self._update_players_info(players_info)
        self.self_info.update(self_info)

    def _update_players_info(self, players_info):
        for player in self.players_info:
            name = player[KEY_PLAYER_NAME]
            to_update = [_player for _player in players_info if _player[KEY_PLAYER_NAME] == name][0]
            player.update(to_update)

    def expose_cards(self, self_info):
        self.self_info.update(self_info)
        return self._expose_cards()

    def _expose_cards(self):
        # TODO
        state_instance = StateInstance(self.name, KEY_ACTION_EXPOSE, self.game_info, self.players_info, self.is_winner)
        print(self.name, StateInstance.from_instance(state_instance.instance[:]))
        self.gameInstance.add_state(state_instance)
        #print self.gameInstance.instance[-10:]
        return [Card.CARD_AH]

    def expose_cards_end(self, players_info):
        self._update_players_info(players_info)
        for info in players_info:
            if info[KEY_PLAYER_NAME] == self.name:
                self.self_info.update(info)
                break

    def new_round(self, game_info):
        self.game_info.update(game_info)

        for player in self.players_info:
            del player[KEY_ROUND_CARD]

    def your_turn(self, game_info, self_info):
        self.game_info.update(game_info)
        self.self_info.update(self_info)

        return self._pick_turn_card()

    def _pick_turn_card(self):
        # TODO
        state_instance = StateInstance(self.name, KEY_ACTION_PICK, self.game_info, self.players_info, self.is_winner)
        print(self.name, StateInstance.from_instance(state_instance.instance[:]))
        self.gameInstance.add_state(state_instance)
        #print self.gameInstance.instance[-10:]
        return self.self_info[KEY_CANDIDATE_CARDS][0]

    def turn_end(self, game_info, players_info):
        self.game_info.update(game_info)

        turn_player_name = game_info[KEY_TURN_PLAYER]
        turn_player_info = None
        for player in players_info:
            if player[KEY_PLAYER_NAME] == turn_player_name:
                turn_player_info = player
                break
        assert(turn_player_info is not None)

        for player in self.players_info:
            if player[KEY_PLAYER_NAME] == turn_player_name:
                player.update(turn_player_info)
                Bot.record_picked_cards(player, [player[KEY_ROUND_CARD]])

    @classmethod
    def record_picked_cards(cls, player, cards):
        if KEY_PICKED_CARDS not in player:
            player[KEY_PICKED_CARDS] = []

        for card in cards:
            if card not in player[KEY_PICKED_CARDS]:
                player[KEY_PICKED_CARDS].append(card)

    def round_end(self, game_info, players_info):
        del self.game_info[KEY_ROUND_PLAYERS]
        self.game_info.update(game_info)
        self._update_players_info(players_info)
        for player in self.players_info:
            if player[KEY_PLAYER_NAME] == self.name:
                self.self_info = player
                break

    def deal_end(self, game_info, players_info):
        self.game_info.update(game_info)
        self._update_players_info(players_info)
        for player in self.players_info:
            if player[KEY_PLAYER_NAME] == self.name:
                self.self_info = player
                break

    def deal_winner(self, winner_name):
        self.is_winner = self.name == winner_name
        state_instance = StateInstance(self.name, KEY_ACTION_GAME_OVER,
                                       self.game_info, self.players_info, self.is_winner)
        print(self.name, state_instance.is_winner, StateInstance.from_instance(state_instance.instance[:]))
        self.gameInstance.add_state(state_instance)
        #print self.gameInstance.instance[-10:]


KEY_ACTION_PASS = 'pass'
KEY_ACTION_EXPOSE = 'expose'
KEY_ACTION_PICK = 'pick'
KEY_ACTION_GAME_OVER = 'game_over'
ACTION_LIST = [KEY_ACTION_PASS, KEY_ACTION_EXPOSE, KEY_ACTION_PICK, KEY_ACTION_GAME_OVER, ]


class StateInstance:
    def __init__(self, name, action, game_info, players_info, is_winner):
        self._players_instance = None
        self._step_instance = None
        self._instance = None
        self.name = name
        self.action = action
        self.game_info = deepcopy(game_info)
        self.players_info = deepcopy(players_info)
        self.sort_players()
        self.is_winner = is_winner

    def set_is_winner(self, is_winner):
        self.is_winner = is_winner
        return self

    @property
    def players_instance(self):
        if self._players_instance is None:
            self._players_instance = self._gen_players_instance()
        return self._players_instance

    @property
    def step_instance(self):
        if self._step_instance is None:
            self._step_instance = self._gen_step_instance()
        return self._step_instance

    @property
    def instance(self):
        if self._instance is None:
            #self._instance = self.step_instance + reduce(lambda x, y: x + y, self.players_instance)
            _tmp = []
            for player_instance in self.players_instance:
                _tmp += player_instance
            self._instance = self.step_instance + _tmp
        return self._instance

    def sort_players(self):
        ordered_players_info = []
        for i in range(4):
            if self.name == self.players_info[i][KEY_PLAYER_NAME]:
                ordered_players_info += self.players_info[i:]
                ordered_players_info += self.players_info[:i]
                break
        self.players_info = ordered_players_info
        return self

    def _gen_players_instance(self):
        players_instance = []
        for i in range(4):
            player = self.players_info[i]
            does_expose = 1 if player.get(KEY_EXPOSED_CARDS, False) else 0
            shooting_moon = 1 if player[KEY_SHOOTING_THE_MOON] else 0
            scored_cards_instance = get_cards_array([Card.Card(card_string) for card_string in player[KEY_SCORE_CARDS]])
            hand_cards_instance = get_cards_array(
                [Card.Card(card_string) for card_string in player.get(KEY_CARDS, tuple())])
            for card_string in player.get(KEY_RECEIVED_CARDS, tuple()):
                hand_cards_instance[Card.Card(card_string).instanceIndex] = VAL_HAVE_CARD
            for card_string in player.get(KEY_PICKED_CARDS, tuple()):
                hand_cards_instance[Card.Card(card_string).instanceIndex] = VAL_PICKED

            player_instance = [does_expose, shooting_moon] + scored_cards_instance + hand_cards_instance
            players_instance.append(player_instance)

        return players_instance

    def _gen_step_instance(self):
        deal_number_instance = StateInstance.deal_number_instance(self.game_info[KEY_DEAL_NUMBER])
        action_instance = StateInstance.action_instance(self.action)
        round_first_card_instance = self.__get_round_first_card_instance()

        return deal_number_instance + action_instance + round_first_card_instance

    @classmethod
    def from_instance(cls, instance,
                      len_step_instance=LEN_EMPTY_DEAL_NUMBER_INSTANCE + LEN_EMPTY_ACTION_INSTANCE + LEN_EMPTY_CARDS_INSTANCE,
                      len_player_instance=106):
        step_instance = instance[:len_step_instance]

        deal_number_instance = step_instance[:LEN_EMPTY_DEAL_NUMBER_INSTANCE]
        deal_number = deal_number_instance.index(1) + 1
        action_instance = step_instance[LEN_EMPTY_DEAL_NUMBER_INSTANCE :
                                        LEN_EMPTY_DEAL_NUMBER_INSTANCE + LEN_EMPTY_ACTION_INSTANCE]
        action = ACTION_LIST[action_instance.index(1)]

        first_card_instance = step_instance[LEN_EMPTY_DEAL_NUMBER_INSTANCE + LEN_EMPTY_ACTION_INSTANCE:
                                            LEN_EMPTY_DEAL_NUMBER_INSTANCE + LEN_EMPTY_ACTION_INSTANCE +
                                            LEN_EMPTY_CARDS_INSTANCE]
        first_cards = [Card.Card.cardStringFromInstanceIndex(i) for i in range(LEN_EMPTY_CARDS_INSTANCE)
                       if first_card_instance[i] != 0]
        assert(len(first_cards) <= 1)
        game_info = {KEY_DEAL_NUMBER: deal_number,
                     'event_name': action,
                     'first_card': first_cards}

        players_info = []
        for player_index in range(4):
            player_instance = instance[len_step_instance + player_index * len_player_instance:
                                       len_step_instance + (player_index+1) * len_player_instance]
            does_expose = player_instance[0] == 1
            shooting_moon = player_instance[1] == 1
            scored_cards_instance = player_instance[2:54]
            scored_cards = [Card.Card.cardStringFromInstanceIndex(i) for i in range(LEN_EMPTY_CARDS_INSTANCE)
                            if scored_cards_instance[i] == 1]
            hand_cards_instance = player_instance[54:106]
            hand_cards = [Card.Card.cardStringFromInstanceIndex(i) for i in range(LEN_EMPTY_CARDS_INSTANCE)
                          if hand_cards_instance[i] == 1]
            picked_cards = [Card.Card.cardStringFromInstanceIndex(i) for i in range(LEN_EMPTY_CARDS_INSTANCE)
                            if hand_cards_instance[i] == -1]
            player_info = {
                'index': player_index,
                'exposed': does_expose,
                'shooting_moon': shooting_moon,
                KEY_CARDS: hand_cards,
                KEY_SCORE_CARDS: scored_cards,
                KEY_PICKED_CARDS: picked_cards,
            }
            players_info.append(player_info)

        return game_info, players_info

    def __get_round_first_card_instance(self):
        if KEY_ROUND_PLAYERS not in self.game_info \
                or not self.game_info[KEY_ROUND_PLAYERS]\
                or self.game_info[KEY_ROUND_PLAYERS][0] == self.name:
            return get_cards_array()

        first_player = None
        first_player_name = self.game_info[KEY_ROUND_PLAYERS][0]
        for player in self.players_info:
            if player[KEY_PLAYER_NAME] == first_player_name:
                first_player = player
                break
        assert (first_player is not None)

        if KEY_ROUND_CARD not in first_player or not first_player[KEY_ROUND_CARD]:
            return get_cards_array()

        round_first_card_string = first_player[KEY_ROUND_CARD]
        round_first_card = Card.Card(round_first_card_string)
        round_first_card_instance = get_cards_array((round_first_card, ))

        return round_first_card_instance

    @classmethod
    def deal_number_instance(cls, deal_number):
        deal_number_instance = EMPTY_DEAL_NUMBER_INSTANCE[:]
        deal_number_instance[deal_number - 1] = VAL_YES
        return deal_number_instance

    @classmethod
    def action_instance(cls, action):
        action_instance = EMPTY_ACTION_INSTANCE[:]
        index = ACTION_LIST.index(action)
        assert(index >= 0)
        action_instance[index] = VAL_YES
        return action_instance


class GameInstance:
    def __init__(self, history_size):
        self._instance = None
        self.history_size = history_size
        self.game_history = []
        self.state_history = []
        self._state_size = None
        self._empty_player_instance = None

    def add_state(self, state):
        assert(isinstance(state, StateInstance))
        self.state_history.append(state)
        return self

    def new_game(self):
        self.game_history.append(self.state_history)
        self.state_history = []
        return self

    @property
    def instance(self):
        if self._instance is None or self._instance[:self.step_instance_size] != self.state_history[-1].step_instance:
            self._instance = self.__gen_instance()
        return self._instance

    def __gen_instance(self):
        if not self.state_history:
            return None

        if self._state_size is None:
            self.step_instance_size = len(self.state_history[0].step_instance)
            self.player_instance_size = len(self.state_history[0].players_instance[0])
            self._state_size = self.step_instance_size + self.history_size * 4 * self.player_instance_size
            self._empty_player_instance = [0] * len(self.state_history[0].players_instance[0])

        instance = []
        instance += self.state_history[-1].step_instance
        for player_i in range(4):
            history_i = 0
            for _ in range(self.history_size):
                history_i -= 1
                try:
                    instance += self.state_history[history_i].players_instance[player_i]
                except IndexError:
                    instance += self._empty_player_instance[:]

        return instance


def get_cards_array(cards=None):
    if cards is None:
        return EMPTY_CARDS_INSTANCE[:]

    _tmp = EMPTY_CARDS_INSTANCE[:]
    if isinstance(cards, Card.Card):
        cards = [cards]

    for card in cards:
        assert(isinstance(card, Card.Card))
        _tmp[card.instanceIndex] = VAL_HAVE_CARD

    return _tmp
