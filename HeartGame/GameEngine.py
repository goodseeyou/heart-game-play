from Game import Game
from Bot import Bot
from Player import Player
from random import shuffle


class GameEngine:
    def __init__(self, game):
        self.game = game

    def shuffle_players_seat(self):
        shuffle(self.game.players)

    def start_a_game(self):
        self.game.new_game()
        for _ in range(4):
            self.game.new_deal()
            #print('deal number: %s' % self.game.info['dealNumber'])
            self.game.pass_cards()
            self.game.pass_end()
            self.game.expose_cards()
            self.game.expose_cards_end()
            for _ in range(13):
                self.game.new_round()
                #print('round number: %s' % self.game.info['roundNumber'])
                self.game.round_end()
                #print('round players: %s' % self.game.info['roundPlayers'])
            #print(','.join([str((game.players[i].info['dealScore'], game.players[i].info['playerName'],)) for i in range(4)]))
            #print('\n'.join([str(game.players[i].info['scoreCards']) for i in range(4)]))
            #print(sum([game.players[i].info['dealScore'] for i in range(4)]))
            self.game.deal_end()
            #print(','.join([str((game.players[i].info['dealScore'], game.players[i].info['playerName'],)) for i in range(4)]))
            self.game.deal_winner()
        self.game.game_end()


if __name__ == '__main__':
    players = []
    for i in range(4):
        name = str(i)
        bot = Bot(name)
        player = Player(name, i, bot)
        players.append(player)

    game = Game(players)
    ge = GameEngine(game)
    ge.shuffle_players_seat()
    ge.start_a_game()
