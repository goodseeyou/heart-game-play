from Card import *
from itertools import combinations

EXPOSE_CARD_CANDIDATE = ['', 'AH', ]
PICK_CARD_CANDIDATE = ['2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS', '2C', '3C',
                       '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC', '2H', '3H', '4H', '5H',
                       '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH', '2D', '3D', '4D', '5D', '6D', '7D',
                       '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD', ]
PASS_CARD_CANDIDATE = [sorted(pass_cards) for pass_cards in combinations(CARD_STRING_LIST, 3)]
ACTION_CANDIDATE = EXPOSE_CARD_CANDIDATE + PICK_CARD_CANDIDATE + PASS_CARD_CANDIDATE

LEN_EXPOSE_CARD_CANDIDATE = len(EXPOSE_CARD_CANDIDATE)
LEN_PICK_CARD_CANDIDATE = len(PICK_CARD_CANDIDATE)
LEN_PASS_CARD_CANDIDATE = len(PASS_CARD_CANDIDATE)
LEN_ACTION_CANDIDATE = len(ACTION_CANDIDATE)

ACTION_INSTANCE = [0] * LEN_ACTION_CANDIDATE
FALSE_ACTION_INSTANCE = [False] * LEN_ACTION_CANDIDATE


def is_valid_pick(first_card, hand_cards, pick_card):
    if pick_card not in hand_cards:
        return False
    if not first_card:
        return pick_card == CARD_2C

    first_suit = Card(first_card).suit
    have_first_suit = any([first_suit == Card(card).suit for card in hand_cards])
    if have_first_suit:
        return first_suit == Card(pick_card).suit

    return True


def is_valid_pass(_pass_cards, hand_cards):
    for card in _pass_cards:
        if card not in hand_cards:
            return False

    return True


def is_valid_expose(expose_cards, hand_cards):
    for card in expose_cards:
        if card not in hand_cards:
            return False

    return True


def pick_card_action_index(card):
    begin_index = LEN_EXPOSE_CARD_CANDIDATE
    index = PICK_CARD_CANDIDATE.index(card)
    return begin_index + index


def pick_card_instance(card_prob_vector):
    action_instance = ACTION_INSTANCE[:]
    for card, prob in card_prob_vector:
        action_instance[pick_card_action_index(card)] = prob
    return action_instance


def pass_card_action_index(_pass_cards):
    begin_index = LEN_EXPOSE_CARD_CANDIDATE + LEN_PICK_CARD_CANDIDATE
    _pass_cards = sorted(_pass_cards)
    index = PASS_CARD_CANDIDATE.index(_pass_cards)
    return begin_index + index


def pass_card_instance(pass_cards_prob_vector):
    action_instance = ACTION_INSTANCE[:]
    for _pass_cards, prob in pass_cards_prob_vector:
        action_instance[pass_card_action_index(_pass_cards)] = prob
    return action_instance


def expose_card_action_index(expose_card):
    begin_index = 0
    index = EXPOSE_CARD_CANDIDATE.index(expose_card)
    return begin_index + index


def expose_card_instance(card_prob_vector):
    action_instance = ACTION_INSTANCE[:]

    for card, prob in card_prob_vector:
        action_instance[expose_card_action_index(card)] = prob
    return action_instance


def pick_candidate_cards(first_card, hand_cards):
    return [card for card in hand_cards if is_valid_pick(first_card, hand_cards, card)]


def valid_pick_action_instance(first_card, hand_cards):
    _valid_pick_action_instance = FALSE_ACTION_INSTANCE[:]
    for card in hand_cards:
        if is_valid_pick(first_card, hand_cards, card):
            _pick_card_action_index = pick_card_action_index(card)
            _valid_pick_action_instance[_pick_card_action_index] = True
    return _valid_pick_action_instance


def valid_pass_action_instance(hand_cards):
    _valid_pass_action_instance = FALSE_ACTION_INSTANCE[:]
    for _pass_cards in combinations(hand_cards, 3):
        _pass_cards = sorted(_pass_cards)
        if is_valid_pass(_pass_cards, hand_cards):
            _valid_pass_action_instance[pass_card_action_index(_pass_cards)] = True
    return _valid_pass_action_instance


def valid_expose_action_instance(hand_cards):
    _valid_pass_action_instance = FALSE_ACTION_INSTANCE[:]
    _valid_pass_action_instance[expose_card_action_index('')] = True
    if CARD_AH in hand_cards:
        _valid_pass_action_instance[expose_card_action_index(CARD_AH)] = True
    return _valid_pass_action_instance
