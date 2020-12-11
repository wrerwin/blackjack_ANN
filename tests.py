import blackjack_engine

def test_is_busted_1():
    """22, no aces"""
    assert blackjack_engine.is_busted([13,5,7]) == True

def test_is_busted_2():
    """19, no aces"""
    assert blackjack_engine.is_busted([10,9]) == False

def test_is_busted_3():
    """soft 17"""
    assert blackjack_engine.is_busted([1,6]) == False

def test_is_busted_4():
    """hard 17"""
    assert blackjack_engine.is_busted([1,12,6]) == False

def test_is_busted_5():
    """hard 22 (ace=1)"""
    assert blackjack_engine.is_busted([1,12,6,5]) == True

def test_Deck_draw_card_1():
    my_deck = blackjack_engine.Deck(1)
    assert len(my_deck.cards) == 52
    card = my_deck.draw_card()
    assert card in [*range(1,13)]  # card is a valid integer
    assert len(my_deck.cards) == 51  # 51 cards left after draw
    assert my_deck.count(card) == 3 # only 3 of same card left in deck
    card2 = my_deck.draw_card()
    assert card2 in [*range(1,13)]  # card2 is a valid integer
    assert len(my_deck.cards) == 50  # 50 cards left after second draw
    assert my_deck.count(card2) < 4 # only 2 or 3 of card2 left in deck
