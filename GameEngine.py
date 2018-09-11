import Game
from random import shuffle

CARD_AH = 'AH'
CARD_2C = '2C'


class GameEngine:
    def __init__(self, bots):
        self.bots = bots
        self.bots_name = None
        self.deal_num = 0
        self.cards = None
        self.leader_bot = None

        self.heart_multiple = 1

    def start_game(self):
        shuffle(self.bots)
        self.bots_name = [bot.name for bot in self.bots]
        for bot in self.bots:
            bot.new_game(self.bots_name)

        for i in range(4):
            self.deal_num += 1
            self.start_deal()

        self.end_game()

    def start_deal(self):
        self.heart_multiple = 1
        self.leader_bot = None

        print('deal: %s' % self.deal_num)
        for bot in self.bots:
            bot.new_deal()
        self.wash_cards()
        self.init_give_cards()
        self.pass_cards()
        self.expose_cards()
        for i in range(13):
            self.start_round()

        for bot in self.bots:
            bot.deal_end()

    def wash_cards(self):
        self.cards = Game.CARD_STRING_INSTANCE_INDEX[:]
        shuffle(self.cards)

    def init_give_cards(self):
        for i in range(4):
            bot = self.bots[i]
            cards = self.cards[13*i:13*i+13]
            bot.receive_cards(cards)

    def pass_cards(self):
        if self.deal_num == 4:
            return

        # pass order is not the same as official game
        _receivers = []
        for i in range(1, 4):
            bot = self.bots[i % 4]
            receiver = self.bots[(i+self.deal_num) % 4]
            cards = bot.pass_cards(receiver.name)
            _receivers.append((receiver, cards, ))

        for receiver, cards in _receivers:
            receiver.receive_cards(cards)

    def expose_cards(self):
        _bool = None
        for bot in self.bots:
            if CARD_AH in bot.cards and bot.cards[CARD_AH] == 1:
                _bool = bot.expose_cards()
                _name = bot.name
                break

        assert(_bool is not None)

        if _bool:
            self.heart_multiple *= 2
            for bot in self.bots:
                bot.expose_card_notify(_name)

    def start_round(self):
        bot_index = self.choose_first_bot_index()
        round_card_bot = []
        for i in range(4):
            bot = self.bots[(i+bot_index) % 4]
            card = bot.pick(self)
            round_card_bot.append((card, bot, ))

        self.scored_cards(round_card_bot)

    def choose_first_bot_index(self):
        if self.leader_bot is None:
            for bot in self.bots:
                if CARD_2C in bot.cards and bot.cards[CARD_2C] == 1:
                    self.leader_bot = bot
                    break

        return self.bots.index(self.leader_bot)

    def scored_cards(self, round_card_bot):
        lead_card, hold_bot = round_card_bot[0]
        lead_card = Game.Card(lead_card)

        cards = []
        for card_string, bot in round_card_bot:
            cards.append(card_string)
            card = Game.Card(card_string)
            if card.suit == lead_card.suit and card.value > lead_card.value:
                hold_bot = bot
                lead_card = card

        hold_bot.score_card(cards)

    def end_game(self):
        winner = sorted([(bot.game_score, bot) for bot in self.bots], key=lambda x: x[0])[-1][1]
        for bot in self.bots:
            bot.game_over(winner.name)


class Bot:
    def __init__(self, name, bot):
        self.name = name
        self.bot = bot
        self.cards = None
        self.scored_cards = None
        self.game_score = 0
        self.deal_score = 0

    def new_game(self, players_name):
        self.bot.new_game(players_name)
        self.cards = {}
        self.scored_cards = {}
        self.game_score = 0
        self.deal_score = 0

    def new_deal(self):
        self.cards = {}
        self.scored_cards = {}
        self.deal_score = 0

    def deal_end(self):
        self.game_score += self.deal_score

    def receive_cards(self, cards):
        cards.sort(key=lambda x: Game.Card(x).instanceIndex)
        print(cards)
        self.bot.receive_cards(cards)
        for card in cards:
            self.cards[card] = 1

    def receive_opponent_cards(self, cards):
        print(cards.sort(key=lambda x: Game.Card(x).instanceIndex))
        self.bot.receive_opponent_cards(cards)
        for card in cards:
            self.cards[card] = 1

    def pass_cards(self, receiver_name):
        cards = self.bot.pass_cards(receiver_name)
        for card in cards:
            self.cards[card] = -1

        return cards

    def expose_cards(self):
        exposed_cards = self.bot.expose_cards()
        if exposed_cards:
            return True
        return False

    def expose_card_notify(self, name):
        self.bot.expose_cards_end(name)

    def pick(self, game_engine):
        pass

    def game_over(self, winner_name):
        pass


if __name__ == '__main__':
    import unittest.mock as mock
    _bots = [Bot(str(i), mock.MagicMock()) for i in range(4)]
    ge = GameEngine(_bots)
    ge.start_game()
