import random

class GameOver(Exception):
    pass

class BustedHand(Exception):
    pass


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
    """
    attributes:
        total: sum of all cards (highest possible value without busting)
        is_soft: True if hand has an ace counted as 11, False otherwise
        is_busted: True if total > 21
        is_blackjack: true if only two cards and they are ace + face card
    methods:
        add_cards: add single card to hand and updates attributes

    Don't try to remove cards. Instead, create a new Hand without the 
    card you want to remove.
    """
    def __init__(self, cards=None):
        if len(cards) < 2:
            raise ValueError("Initial hand must have at least two cards")
        self.cards = []
        self.total = None
        self.is_soft = None
        self.is_busted = False
        # self.is_blackjack = False
        # do it this way so it uses validator in add_card
        for card in cards:
            self.add_card(card) 

    def add_card(self, card):
        """
        adds card to hand
        raises ValueError if card not valid
        """
        if card not in [*range(1,14)]:
            raise ValueError("Not a valid card")

        if self.is_busted == True:
            raise BustedHand("Can't add a card to a busted hand")

        self.cards.append(card)
        print(self.cards)
        if len(self.cards) > 1:
            self.total, self.is_soft = self._sum_cards()
            if self.total > 21:
                self.is_busted = True
 
    def _sum_cards(self):
        # is_soft is needed for dealer logic, which hits on soft 17 
        # but stays on hard 17
        card_values = {1:11, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7,
                       8:8, 9:9, 10:10, 11:10, 12:10, 13:10}
        card_values_hard = card_values.copy()
        card_values_hard[1] = 1

        is_soft = False
        total = sum([card_values[card] for card in self.cards])
        # if self.total > 21 and 1 in self.cards:
        #     total = sum([card_values_hard[card] for card in self.cards])
        return total, is_soft


class BlackjackGame():
    """ 
    The results are defined as ints based on how much money they make,
    a multiplier of the orignal bet.
        lose: -1
        push: 0
        win: 1
        blackjack: 1.5

    Attributes (read only):
        player_hand (Hand): current player hand
        dealer_hand (Hand): current dealer hand
        dealer_upcard (int): dealer upcard, which is dealer_hand[0]
        is_finished (boolean): whether the game is finished
        result (int): result of the game is -1, 0, 1, or 1.5.
            Or None if game not finished.
        deck (Deck): current deck

    Methods:
        player_move (need better name?): update the game after player decision
    """
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand(deck.draw_card(2))
        self.dealer_hand = Hand(deck.draw_card(2))
        self.dealer_upcard = self.dealer_hand[0]
        self.is_finished = False
        self.result = None
        if cfb_result := self._check_for_blackjacks() is not None:
            self.is_finished = True
            self.result = cfb_result
    
    def _check_for_blackjacks(self):
        """
        checks if player, dealer, or both have blackjack
        """
        player_blackjack = dealer_blackjack = False
        if self.player_hand.sum_cards == 21:
            player_blackjack = True
        if self.dealer_hand.sum_cards == 21:
            dealer_blackjack = True
        if player_blackjack and dealer_blackjack:
            return 0
        elif player_blackjack:
            return 1.5
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

        if hit_or_stay == 'stay':
            self._dealer_turn()
        elif hit_or_stay == 'hit':
            player_hand.add_card(deck.draw_card())
            # check for game status changes after move
            if player_hand.is_busted():
                self._finish_game(-1)
            elif player_hand.total == 21:
                # in this case, game isn't over but player is done
                self._dealer_turn() # updates dealer hand
            elif player_hand.total < 21:
                pass
        
    def _dealer_turn(self):
        # loop through dealer preset decisions
        # finishes game once dealer is done
        while True:
            hit_or_stay = dealer_bot(dealer_hand)
            if hit_or_stay == 'stay':
                break
            if hit_or_stay == 'hit':
                dealer_hand.add_card(deck.draw_card())
            if dealer_hand.is_busted() or dealer_hand.total == 21:
                break
        
        # Assuming dealer didn't bust, determine winner by comparing final 
        # player hand and final dealer hand
        if player_total == dealer_total:
            self._finish_game(0)
        if player_total > dealer_total:
            self.finish_game(1)
        if player_total < dealer_total:
            self._finish_game(-1)

    def _finish_game(self, result):
        self.is_finished = True
        self.result = result


    
def dealer_bot(dealer_hand):
    """
    Make preset decisions for dealer given current hand.
    Currently hits on soft 17

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

