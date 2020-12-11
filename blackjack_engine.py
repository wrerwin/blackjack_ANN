example_hand = [1,3,12]  # ace, 3, queen

def is_busted(hand):
    """returns True if hand is busted, False otherwise"""
    #  if total(hand) > 21:
    #      return True
    #  need to deal with aces
    pass

class Deck():
    def __init__(self, n=1):
        self.cards = self._random_deck(n)

    def draw_card(self):
        card = self.cards.pop(0)
        return card

    def _random_deck():
        # generate random deck of n*52 cards
        pass

def blackjack_round():
    deck = Deck()
    player_hand = [deck.draw_card() for x in range(2)]
    dealer_hand = [deck.draw_card() for x in range(2)]
    dealer_upcard = dealer_hand[1]
    # loop through player decisions until stay or bust
    # loop through dealer preset decisions
    # determine winner
    # outcome = win, loss, put, etc.
    # return outcome with all player decisions made in the game
