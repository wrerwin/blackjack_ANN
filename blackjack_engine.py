import random

class Deck():
    """currently initializes as a random deck of 52 cards"""
    def __init__(self):
        self.cards = self._random_deck()

    def draw_card(self, n=1):
        """return single card (int) or list of cards (list of ints)"""
        if n==1:
            card = self.cards.pop(0)
            return card
        if n>1:
            return [self.draw_card() for x in range(n)] 

    def _random_deck(self):
        # generate random deck of n*52 cards
        deck = 4*[*range(1,14)]
        random.shuffle(deck)
        return deck

class Hand():
    def __init__(self, cards=None):
        if cards == None:
            self.cards = []
        else:
            self.cards=cards

    def add_card():
        """adds card to hand"""
        # probably just use list append
        pass

    def sum_cards(self):
        # need to account for aces
        pass 

    def is_busted(self):
        """kinda unnecessary but whatever"""
        return self.sum_cards() > 21

    def is_soft(self):
        """return True if hand has ace being counted as 11"""
        # this is needed for dealer logic, which hits on soft 17 
        # but stays on hard 17
        pass

def blackjack_round():
    """ 
    Results:
        lose: -1
        push: 0
        win: 1
        blackjack: 1.5
    """
    deck, player_hand, dealer_hand = generate_initial_game_state()
    dealer_upcard = dealer_hand[1]  # dealer's second card

    # check if player or dealer have blackjack
    player_blackjack = dealer_blackjack = False
    if player_hand.sum_cards == 21:
        player_blackjack = True
    if dealer_hand.sum_cards == 21:
        dealer_blackjack = True
    if player_blackjack and dealer_blackjack:
        return 0
    elif player_blackjack:
        return 1.5
    elif dealer_blackjack:
        return -1

    # loop through player decisions until stay or bust
    while True:
        hit_or_stay == random.choice(['hit', 'stay'])
        if hit_or_stay == 'stay':
            break
        if hit_or_stay == 'hit':
            player_hand.add_card(deck.draw_card())
        if player_hand.is_busted():
            return -1
    
    # loop through dealer preset decisions
    while True:
        hit_or_stay = dealer_bot(dealer_hand)
        if hit_or_stay == 'stay':
            break
        if hit_or_stay == 'hit':
            dealer_hand.add_card(deck.draw_card())
        if dealer_hand.is_busted():
            return 1
    
    # if neither busted, determine winner by comparing final 
    # player hand and final dealer hand
    if player_total == dealer_total:
        return 0
    if player_total > dealer_total:
        return 1
    if player_total < dealer_total:
        return -1

def generate_initial_game_state():
    deck = Deck()
    player_hand = Hand(deck.draw_card(2))
    dealer_hand = Hand(deck.draw_card(2))
    return deck, player_hand, dealer_hand

def dealer_bot(dealer_hand):
    """
    Make a preset decisions for dealer given current hand.
    Currently stays on soft 17

    returns "hit" or "stay" 
    """
    total = dealer_hand.sum_cards()        

    # this  assumes 21 case is handled outside function and a 21 hand will
    # never need to get passed in
    assert total >= 4 and total < 21

    if total == 17 and dealer_hand.is_soft() == True:
        return "hit"
    elif total >= 17:
        return "stay"
    else:
        return "hit"

