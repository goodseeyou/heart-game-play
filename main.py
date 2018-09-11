#coding=UTF-8

from websocket import create_connection
from Bot import PokerBot
from abcBot import AbcBot
import json
import logging
import sys

from Card import Card

class Log(object):
    def __init__(self,is_debug=True):
        self.is_debug=is_debug
        self.msg=None
        self.logger = logging.getLogger('hearts_logs')
        hdlr = logging.FileHandler('hearts_logs.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)
    def show_message(self,msg):
        if self.is_debug:
            print msg
    def save_logs(self,msg):
        self.logger.info(msg)

IS_DEBUG=False
system_log=Log(IS_DEBUG)

class PokerSocket(object):
    ws = ""

    def __init__(self, player_name, player_number, token, connect_url, poker_bot):
        self.player_name = player_name
        self.connect_url = connect_url
        self.player_number = player_number
        self.poker_bot = poker_bot
        self.token = token

    def takeAction(self, action, data):
        if action == "new_game":
            self.poker_bot.new_game(data)

        if action == "new_deal":
            self.poker_bot.new_deal(data)



       if  action=='new_game':
           self.poker_bot.new_game()
       elif action=="new_deal":
           self.poker_bot.init_players(data['players'])
           self.poker_bot.receive_cards(data['self']['cards'])
       elif action=="pass_cards":
           pass_cards=self.poker_bot.pass_cards(data['receiver'])
           self.ws.send(json.dumps(
                {
                    "eventName": "pass_my_cards",
                    "data": {
                        "dealNumber": data['dealNumber'],
                        "cards": pass_cards
                    }
                }))
       elif action=="receive_opponent_cards":
           self.poker_bot.receive_opponent_cards(data['receivedCards'])
       elif action=="expose_cards":
           export_cards = self.poker_bot.expose_my_cards()
           if not export_cards:
               export_cards = []
           self.ws.send(json.dumps(
               {
                   "eventName": "expose_my_cards",
                   "data": {
                       "dealNumber": data['dealNumber'],
                       "cards": export_cards
                   }
               }))
       elif action=="expose_cards_end":
           self.poker_bot.expose_cards_end(data['players'])
       elif action=="new_round":
           self.poker_bot.new_round(data['players'])
       elif action=="turn_end":
           self.poker_bot.turn_end(data)
       elif action=="your_turn":
           pick_card = self.poker_bot.select_card()
           message="Send message:{}".format(json.dumps(
                {
                   "eventName": "pick_card",
                   "data": {
                       "dealNumber": data['dealNumber'],
                       "roundNumber": data['roundNumber'],
                       "turnCard": pick_card
                   }
               }))
           system_log.show_message(message)
           system_log.save_logs(message)
           self.ws.send(json.dumps(
               {
                   "eventName": "pick_card",
                   "data": {
                       "dealNumber": data['dealNumber'],
                       "roundNumber": data['roundNumber'],
                       "turnCard": pick_card
                   }
               }))
       elif action=="turn_end":
           self.poker_bot.turn_end(data)
       elif action=="round_end":
           pass
           #self.poker_bot.round_end(data)
       elif action=="deal_end":
           pass
           #self.poker_bot.deal_end(data)
           #self.poker_bot.reset_card_his()
       elif action=="game_end":
           self.poker_bot.game_over(data)
           self.ws.close()
    def doListen(self):
        try:
            self.ws = create_connection(self.connect_url)
            self.ws.send(json.dumps({
                "eventName": "join",
                "data": {
                    "playerNumber":self.player_number,
                    "playerName":self.player_name,
                    "token":self.token
                }
            }))
            while 1:
                result = self.ws.recv()
                msg = json.loads(result)
                event_name = msg["eventName"]
                data = msg["data"]
                system_log.show_message(event_name)
                system_log.save_logs(event_name)
                system_log.show_message(data)
                system_log.save_logs(data)
                self.takeAction(event_name, data)
        except Exception, e:
            system_log.show_message(e)
            system_log.save_logs(e)
            self.doListen()

class LowPlayBot(PokerBot):

    def __init__(self,name):
        super(LowPlayBot,self).__init__(name)
        self.my_hand_cards=[]
        self.expose_card=False
        self.my_pass_card=[]
    def receive_cards(self,data):
        self.my_hand_cards=self.get_cards(data)

    def pass_cards(self,data):
        cards = data['self']['cards']
        self.my_hand_cards = []
        for card_str in cards:
            card = Card(card_str)
            self.my_hand_cards.append(card)
        pass_cards=[]
        count=0
        for i in range(len(self.my_hand_cards)):
            card=self.my_hand_cards[len(self.my_hand_cards) - (i + 1)]
            if card==Card("QS"):
                pass_cards.append(card)
                count+=1
            elif card==Card("TC"):
                pass_cards.append(card)
                count += 1
        for i in range(len(self.my_hand_cards)):
            card = self.my_hand_cards[len(self.my_hand_cards) - (i + 1)]
            if card.suit_index==2:
                pass_cards.append(card)
                count += 1
                if count ==3:
                    break
        if count <3:
            for i in range(len(self.my_hand_cards)):
                card = self.my_hand_cards[len(self.my_hand_cards) - (i + 1)]
                if card not in self.game_score_cards:
                    pass_cards.append(card)
                    count += 1
                    if count ==3:
                        break
        return_values=[]
        for card in pass_cards:
            return_values.append(card.toString())
        message="Pass Cards:{}".format(return_values)
        system_log.show_message(message)
        system_log.save_logs(message)
        self.my_pass_card=return_values
        return return_values

    def pick_card(self,data):
        cadidate_cards=data['self']['candidateCards']
        cards = data['self']['cards']
        self.my_hand_cards = []
        for card_str in cards:
            card = Card(card_str)
            self.my_hand_cards.append(card)
        message = "My Cards:{}".format(self.my_hand_cards)
        system_log.show_message(message)
        card_index=0
        message = "Pick Card Event Content:{}".format(data)
        system_log.show_message(message)
        message = "Candidate Cards:{}".format(cadidate_cards)
        system_log.show_message(message)
        system_log.save_logs(message)
        message = "Pick Card:{}".format(cadidate_cards[card_index])
        system_log.show_message(message)
        system_log.save_logs(message)
        return cadidate_cards[card_index]

    def expose_my_cards(self,yourcards):
        expose_card=[]
        for card in self.my_hand_cards:
            if card==Card("AH"):
                expose_card.append(card.toString())
        message = "Expose Cards:{}".format(expose_card)
        system_log.show_message(message)
        system_log.save_logs(message)
        return expose_card

    def expose_cards_end(self,data):
        players = data['players']
        expose_player=None
        expose_card=None
        for player in players:
            try:
                if player['exposedCards']!=[] and len(player['exposedCards'])>0 and player['exposedCards']!=None:
                    expose_player=player['playerName']
                    expose_card=player['exposedCards']
            except Exception, e:
                system_log.show_message(e.message)
                system_log.save_logs(e.message)
        if expose_player!=None and expose_card!=None:
            message="Player:{}, Expose card:{}".format(expose_player,expose_card)
            system_log.show_message(message)
            system_log.save_logs(message)
            self.expose_card=True
        else:
            message="No player expose card!"
            system_log.show_message(message)
            system_log.save_logs(message)
            self.expose_card=False

    def receive_opponent_cards(self,data):
        self.my_hand_cards = self.get_cards(data)
        players = data['players']
        for player in players:
            player_name = player['playerName']
            if player_name == self.player_name:
                picked_cards = player['pickedCards']
                receive_cards = player['receivedCards']
                message = "User Name:{}, Picked Cards:{}, Receive Cards:{}".format(player_name, picked_cards,receive_cards)
                system_log.show_message(message)
                system_log.save_logs(message)

    def round_end(self,data):
        try:
            round_scores=self.get_round_scores(self.expose_card, data)
            for key in round_scores.keys():
                message = "Player name:{}, Round score:{}".format(key, round_scores.get(key))
                system_log.show_message(message)
                system_log.save_logs(message)
        except Exception, e:
            system_log.show_message(e.message)

    def deal_end(self,data):
        self.my_hand_cards=[]
        self.expose_card = False
        deal_scores,initial_cards,receive_cards,picked_cards=self.get_deal_scores(data)
        message = "Player name:{}, Pass Cards:{}".format(self.player_name, self.my_pass_card)
        system_log.show_message(message)
        system_log.save_logs(message)
        for key in deal_scores.keys():
            message = "Player name:{}, Deal score:{}".format(key,deal_scores.get(key))
            system_log.show_message(message)
            system_log.save_logs(message)
        for key in initial_cards.keys():
            message = "Player name:{}, Initial cards:{}, Receive cards:{}, Picked cards:{}".format(key, initial_cards.get(key),receive_cards.get(key),picked_cards.get(key))
            system_log.show_message(message)
            system_log.save_logs(message)

    def game_over(self,data):
        game_scores = self.get_game_scores(data)
        for key in game_scores.keys():
            message = "Player name:{}, Game score:{}".format(key, game_scores.get(key))
            system_log.show_message(message)
            system_log.save_logs(message)

    def pick_history(self,data,is_timeout,pick_his):
        for key in pick_his.keys():
            message = "Player name:{}, Pick card:{}, Is timeout:{}".format(key,pick_his.get(key),is_timeout)
            system_log.show_message(message)
            system_log.save_logs(message)

def main():
    argv_count=len(sys.argv)
    if argv_count>2:
        player_name = sys.argv[1]
        player_number = sys.argv[2]
        token= sys.argv[3]
        connect_url = sys.argv[4]
    else:
        player_name="Sample Bot"
        player_number=99
        token="12345678"
        connect_url="ws://localhost:8080/"
    #sample_bot=LowPlayBot(player_name)
    sample_bot=AbcBot(player_name, 0, 0)
    myPokerSocket=PokerSocket(player_name,player_number,token,connect_url,sample_bot)
    myPokerSocket.doListen()

if __name__ == "__main__":
    main()