import random
'''
this entire file is pseudo code and kind of a mess. the logic is pretty close, but there will undoubtedly be some kinks to work out.
maybe the deck should be a global variable, there is a ton of passing it in and out required
most of the nitty gritty/rules that will be required here can be pulled from blackjack_game_rules.py, if we want to use it
'''

def play_blackjack_round():
    '''this function plays a 1v1 round of blackjack and outputs
    the decisions, cards, and whether the round resulted in a win'''
    [player_hand,dealer_first_card,deck] = generate_initial_game_state(deck)
    while not win_loss_result:   # this is meant to be a while loop that keeps going until a decision is reached regarding a win or loss
        [cards,decision,win_loss_result,deck] = play_blackjack_hand(player_hand,dealer_card,deck)
    return hands_played,decisions_made,dealer_first_card,win_loss_result

def generate_initial_game_state(previous_hand,deck)
    '''this function generates the first hand of play hand'''
    [player_hand,deck] = draw_card(deck,num_cards=2)
    [dealer_card,deck] = draw_card(deck)
    return player_hand, dealer_first_card,deck

def play_blackjack_hand(player_hand,dealer_card,deck):
    '''this function plays a hand of blackjack against the dealer,
    and outputs the cards that were played in the hand and the 
    decisions made at each instance'''
    decision_to_stay_or_hit = random.randint(0, 1)
    if decision_to_stay_or_hit == 0: # 0 represents a "stay" action
        win_loss_result = evaluate_hand(player_hand,dealer_first_card,deck)
    if decision_to_stay_or_hit == 1: # 1 represents a "hit" action
        new_hand,is_busted = generate_new_hand(deck)
        # need to assert whether is_busted is true, if busted, go straight to a loss, end the round
        if is_busted:
            win_loss_result = 0 # this is triggered if you bust, indicating a loss
        else:
            pass # this will end the function without passing win_loss_result, something something args and kwargs 
        
    return cards,decision,win_loss_result

def generate_new_hand(previous_hand,deck):
    '''this function adds a card to blackjack hand'''
    new_card = draw_card(deck)
    new_hand = previous_hand.append(new_card)
        
    return new_hand,dealer_card,remaining_deck

def draw_card(deck,num_cards=1):
    card = deck[0:num_cards-1]
    return card

def evaluate_hand(player_hand,dealer_first_card,deck):
    '''
    This function evaluates whether the player or dealer wins given their relative positions. 
    I assume that the dealer keeps drawing if it hasn't won or busted, not sure if that's actually how it's played.
    How are ties dealt with here and IRL?
    '''
    player_deck_value = sum_cards(player_hand)
    dealer_hand = dealer_first_card
    dealer_deck_value = sum_cards(dealer_hand)
    
    # the logic on this while loop feels bad and the pseudo code looks ugly, but I'm not exactly sure why, also I'm tired. 
    while dealer_deck_value > player_deck_value & < 22: # the goal here is to have the dealer draw until it busts or wins
        win_loss_result = 0 # the case where the player has lost to the dealer outright
    if dealer_deck_value < 22 & : 
        dealer_hand = draw_card(dealer_hand,deck) # the case where the dealer has to draw another hand
        pass # pass might not be doing what I want here, but generally I want to escape the rest of the function if this condition is met
    else:
        win_loss_result = 1 # the remaining case, where the dealer has busted and the player has won
    return win_loss_result
    