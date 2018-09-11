from Game import Card

class GameEngine:
    def __init__(self, bots):
        # random sort bots order
        self.bots = bots
        self.deal_num = 0

    def start_game(self):
        for i in xrange(4):
            self.start_deal()
            self.deal_num += 1

    def start_deal(self):
        
        self.init_give_cards()
        self.pass_cards()
        self.expose_cards()
        for i in xrange(13):
            self.start_round()
            self.calculate_round_score()

    def init_give_cards(self):
        pass

    def pass_cards(self):
        pass

    def expose_cards(self):
        pass

    def start_round(self):
        bot_index = self.choose_first_bot()
        for i in xrange(4):
            bot = self.bots[(i+bot_index)%4]
            bot.pick(self)
        self.calculate_round_score()

    def choose_first_bot(self):
        pass

    def calculate_round_score(self):
        pass


class Bot:
    def __init__(self):
        pass

    def receive_cards(self, cards):
        pass

    def pass_cards(self):
        pass

    def expose_cards(self):
        pass

    def pick(self,game_engine):
        pass