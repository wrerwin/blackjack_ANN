import blackjack_engine
import pytest

def test_sum_cards_22_no_aces():
    assert blackjack_engine.Hand([13,5,7]).sum_cards() == 22

def test_sum_cards_19_no_aces():
    assert blackjack_engine.Hand([10,9]).sum_cards() == 19

def test_sum_cards_soft_17():
    assert blackjack_engine.Hand([1,6]).sum_cards() == 17

def test_sum_cards_hard_17():
    assert blackjack_engine.Hand([1,12,6]).sum_cards() == 17

def test_sum_cards_hard_22():
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

def test_dealer_bot_16():
    hand = blackjack_engine.Hand([11,6])
    assert blackjack_engine.dealer_bot(hand) == 'hit'

def test_dealer_bot_hard_17():
    hand = blackjack_engine.Hand([11,6,1])
    assert blackjack_engine.dealer_bot(hand) == 'stay'

def test_dealer_bot_soft_17():
    hand = blackjack_engine.Hand([1,6])
    assert blackjack_engine.dealer_bot(hand) == 'hit'

def test_dealer_bot_20():
    hand = blackjack_engine.Hand([12,4,6])
    assert blackjack_engine.dealer_bot(hand) == 'stay'

def test_dealer_bot_hard_20():
    hand = blackjack_engine.Hand([1,2,12,7])
    assert blackjack_engine.dealer_bot(hand) == 'stay'

def test_Hand_is_soft_no_aces():
    hand = blackjack_engine.Hand([11,6])
    assert hand.is_soft() == False
    
def test_Hand_is_soft_soft_17():
    hand = blackjack_engine.Hand([1,6])
    assert hand.is_soft() == True

def test_Hand_is_soft_hard_17():
    hand = blackjack_engine.Hand([11,6,1])
    assert hand.is_soft() == False

def test_Hand_add_card_goodcard():
    hand = blackjack_engine.Hand([1,2,12,7])
    hand.add_card(1)
    hand.add_card(11)
    hand.add_card(13)
    assert hand.cards == [1,2,12,7,1,11,13]

def test_Hand_add_card_badcard():
    hand = blackjack_engine.Hand([1,2,12,7])
    with pytest.raises(ValueError):
        hand.add_card(15)
    with pytest.raises(ValueError):
        hand.add_card(0)
    with pytest.raises(ValueError):
        hand.add_card(1.5)
    with pytest.raises(ValueError):
        hand.add_card('cat')
