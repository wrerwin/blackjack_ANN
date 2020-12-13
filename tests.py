import blackjack_engine

def test_sum_cards():
    # 22, no aces
    assert blackjack_engine.Hand([13,5,7]).sum_cards() == 22
    # 19, no aces
    assert blackjack_engine.Hand([10,9]).sum_cards() == 19
    # soft 17
    assert blackjack_engine.Hand([1,6]).sum_cards() == 17
    # hard 17
    assert blackjack_engine.Hand([1,12,6]).sum_cards() == 17
    # hard 22 (ace=1)
    assert blackjack_engine.Hand([1,12,6,5]).sum_cards() == 22

def test_Deck_draw_card():
    my_deck = blackjack_engine.Deck()
    assert len(my_deck.cards) == 52
    card = my_deck.draw_card()
    assert card in [*range(1,14)]  # card is a valid integer
    assert len(my_deck.cards) == 51  # 51 cards left after draw
    assert my_deck.cards.count(card) == 3 # only 3 of same card left in deck
    
    cards2 = my_deck.draw_card(3)
    assert len(cards2) == 3
    assert len(my_deck.cards) == 48  # cards left after second draw
    assert my_deck.cards.count(cards2[0]) < 4 # less than 4 of same card left in deck
    assert my_deck.cards.count(cards2[1]) < 4 
    assert my_deck.cards.count(cards2[2]) < 4 
