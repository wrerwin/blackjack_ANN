import random

CARDS = ['A', '2', '3', '4', '5','6', '7', '8', '9', '10', 'J', 'Q', 'K']
CARD_VALUES = {'A':11, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7,
               '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

class GameOver(Exception):
    pass

class Deck():
    """
    currently initializes as a random deck of 52 cards
    """
    def __init__(self, seed=None):
        self.cards = self._random_deck(seed)

    def draw_card(self, n=1):
        """return single card (int) or list of cards (list of ints)"""
        if n==1:
            card = self.cards.pop(0)
            return card 
        if n>1:
            return [self.draw_card() for x in range(n)] 

    @staticmethod
    def _random_deck(seed):
        # generate random deck of n*52 cards
        deck = 4*CARDS
        if seed == None:
            random.shuffle(deck)
        else:
            random.Random(seed).shuffle(deck)
        return deck


class Hand():
    """
    attributes, read only:
        cards (list of strings): list of cards in hand
        total: sum of all cards (highest possible value without busting)
        is_soft: True if hand has an ace counted as 11, False otherwise
        is_busted: True if total > 21
        is_blackjack: true if only two cards and they are ace + face card
        is_pair: True if a two card hand where both cards have same VALUE
        is_stayed: True if player/dealer stays on hand, False otherwise, None if unset
        is_finished: True if stayed, busted, or 21
    methods:
        add_cards: add single card to hand and updates attributes
        stay: use this if player/dealer decides to stay to mark hand as finished

    Don't try to remove cards. Instead, create a new Hand without the 
    card you want to remove.
    """
    def __init__(self, cards_in):
        if len(cards_in) < 2:
            raise ValueError("Initial hand must have at least two cards")
        self._cards = []
        self._total = None
        self._is_soft = None
        self._is_busted = False
        self._is_pair = False
        self._is_stayed = False
        self._is_blackjack = False
        # do it this way so it uses validators in add_card
        for card in cards_in:
            self.add_card(card) 

    def __repr__(self):
        cards_string = '[' + ' '.join(self.cards) + ']'
        return ', '.join([cards_string, "total: "+str(self.total)])

    def add_card(self, card):
        """
        adds card to hand
        raises ValueError if card not valid
        """
        if card not in CARDS:
            raise ValueError("Not a valid card")

        if self.is_busted == True:
            raise RuntimeError("Can't add a card to a busted hand")
        if self.is_stayed == True:
            raise RuntimeError("Can't add a card after staying on a hand")
        if self.is_blackjack == True:
            raise RuntimeError("Can't add a card to blackjack")

        self._cards.append(card)
        # if at least two cards it's an actual hand that has a total
        if len(self._cards) > 1:
            self._total, self._is_soft = self._sum_cards()
            if self._total > 21:
                self._is_busted = True
        # if exactly two cards, could be a pair or blackjack
        if len(self._cards) == 2:
            self._is_pair = False
            if CARD_VALUES[self.cards[0]] == CARD_VALUES[self._cards[1]]:
                self._is_pair = True
            if self._total == 21:
                self._is_blackjack = True
    
    def stay(self):
        """
        sets is_stayed property True so hand can no longer be modified
        """
        self._is_stayed = True
    
    @property
    def is_finished(self):
        return self.is_blackjack or self.is_stayed or self.total == 21 or self.is_busted

    @property
    def cards(self):
        return self._cards

    @property
    def total(self):
        return self._total

    @property
    def is_soft(self):
        return self._is_soft

    @property
    def is_busted(self):
        return self._is_busted

    @property
    def is_pair(self):
        return self._is_pair

    @property
    def is_stayed(self):
        return self._is_stayed

    @property
    def is_blackjack(self):
        return self._is_blackjack

    def _sum_cards(self):
        # is_soft is needed for dealer logic, which hits on soft 17 
        # but stays on hard 17

        is_soft = False
        total = sum([CARD_VALUES[card] for card in self.cards])

        # deal with aces
        n_aces = self.cards.count('A')
        n_ace_ones = 0 # number of aces counted as 1
        for i in range(n_aces):
            if total > 21:
                n_ace_ones += 1 
                total -= 10
        if n_ace_ones < n_aces:  # if at least one ace is 11
            is_soft = True  
        
        return total, is_soft


class BlackjackGame():
    """ 
    The results are defined as ints based on how much money they make,
    a multiplier of the orignal bet.
        lose: -1
        push: 0
        win: 1
        blackjack: 2
    
    Attributes (read only):
        player_hands (list of Hands): current player hand, multiple if split
        dealer_hand (Hand): current dealer hand
        dealer_upcard (int): dealer upcard, which is dealer_hand.cards[0]
        is_finished (boolean): whether the game is finished
        result (int): result of the game is -1, 0, 1, or 1.5.
            Or None if game not finished.
        deck (Deck): current deck (default randomly shuffled deck)

    Methods:
        player_move (need better name?): update the game after player decision
    """
    def __init__(self, deck=None):
        if deck == None:
            self.deck = Deck()
        else:
            self.deck = deck
        self.player_hands = [Hand(self.deck.draw_card(2))]
        self.dealer_hand = Hand(self.deck.draw_card(2))
        self.dealer_upcard = self.dealer_hand.cards[0]
        self.is_finished = False
        self._hand_number = None # which hand is currently being played
        self.result = None

        # replace this with a modified check_winner eventually
        cfb_result = self._check_for_blackjacks()
        if cfb_result is not None:
            self.is_finished = True
            self.result = cfb_result
    
    def _check_for_blackjacks(self):
        """
        checks if player, dealer, or both have blackjack
        """
        player_blackjack = dealer_blackjack = False
        if self.player_hands[0].total == 21:
            player_blackjack = True
        if self.dealer_hand.total == 21:
            dealer_blackjack = True
        if player_blackjack and dealer_blackjack:
            return 0
        elif player_blackjack:
            return 2
        elif dealer_blackjack:
            return -1
        else:
            return None
    
    def player_move(self, hit_or_stay):
        """ haven't implemented double or split 
        player can't hit on 21
        """
        if self.is_finished == True:
            raise GameOver("This game is over. Can't make a move.")

        for i,hand in enumerate(self.player_hands):
            if hit_or_stay == 'stay':
                self.player_hands[i].stay()
            elif hit_or_stay == 'hit':
                self.player_hands[i].add_card(self.deck.draw_card())
            elif hit_or_stay == 'split':
                if is_pair == False:
                    raise RuntimeError('Can\'t split this hand...') # move this to Hand???
                if is_pair == True:
                    # split into two hands
                    hand_1 = Hand([self.player_hands[0].cards[0], self.Deck.draw_card()])
                    hand_2 = Hand([self.player_hands[0].cards[2], self.Deck.draw_card()])
        if all(hand.is_finished for hand in self.player_hands):
            self.is_finished = True
            self._dealer_turn()
            for hand in self.player_hands:
                self.result = check_winner(hand, self.dealer_hand)
    
    def _dealer_turn(self):
        # loop through dealer preset decisions
        # finishes game once dealer is done
        while True:
            hit_or_stay = dealer_bot(self.dealer_hand)
            if hit_or_stay == 'stay':
                break
            if hit_or_stay == 'hit':
                self.dealer_hand.add_card(self.deck.draw_card())
            if self.dealer_hand.is_busted or self.dealer_hand.total == 21:
                break
        
def check_winner(player_hand, dealer_hand):
    """ returns number depending on outcome
    dealer wins: -1
    push: 0
    player wins: 1
    player wins with blackjack: 2
    """
    if player_hand.is_blackjack and dealer_hand.is_blackjack:
        return 0
    elif player_hand.is_blackjack:
        return 2
    elif dealer_hand.is_blackjack:
        return -1

    if player_hand.is_busted:
        return -1
    elif dealer_hand.is_busted:
        return 1

    if player_hand.total == dealer_hand.total:
        return 0
    elif player_hand.total > dealer_hand.total:
        return 1
    else:
        return -1
    
def dealer_bot(dealer_hand):
    """
    Make preset decisions for dealer given current hand.
    Currently hits on soft 17

    returns "hit" or "stay" 
    """
    total = dealer_hand.total

    # this  assumes 21 case is handled outside function and a 21 hand will
    # never need to get passed in
    assert total >= 4 and total < 21

    if total == 17 and dealer_hand.is_soft == True:
        return "hit"
    elif total >= 17:
        return "stay"
    else:
        return "hit"

