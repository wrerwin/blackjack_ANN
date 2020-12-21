import blackjack_engine
import pytest

# Hand tests
def test_Hand_total_22_no_aces():
    assert blackjack_engine.Hand([13,5,7]).total == 22

def test_Hand_total_19_no_aces():
    assert blackjack_engine.Hand([10,9]).total == 19

def test_Hand_total_soft_17():
    assert blackjack_engine.Hand([1,6]).total == 17

def test_Hand_total_hard_17():
    assert blackjack_engine.Hand([1,9,7]).total == 17

def test_Hand_total_hard_22():
    assert blackjack_engine.Hand([1,9,6,6]).total == 22

def test_Hand_total_two_aces():
    # one ace is hard and one is soft
    assert blackjack_engine.Hand([1,2,1]).total == 14

def test_Hand_total_three_aces():
    # two aces are hard and one is soft
    assert blackjack_engine.Hand([1,1,1,3]).total == 16

def test_Hand_total_three_aces_hard():
    # three aces, all are hard
    assert blackjack_engine.Hand([5,1,1,5,1]).total == 13

def test_Hand_total_three_aces():
    # two aces are hard and one is soft
    assert blackjack_engine.Hand([1,1,1,3]).total == 16

def test_Hand_is_soft_22_no_aces():
    assert blackjack_engine.Hand([13,5,7]).is_soft == False

def test_Hand_is_soft_19_no_aces():
    assert blackjack_engine.Hand([10,9]).is_soft == False

def test_Hand_is_soft_soft_17():
    assert blackjack_engine.Hand([1,6]).is_soft == True

def test_Hand_is_soft_hard_17():
    assert blackjack_engine.Hand([1,9,7]).is_soft == False

def test_Hand_is_soft_hard_22():
    assert blackjack_engine.Hand([1,9,6,6]).is_soft == False

def test_Hand_is_soft_two_aces():
    # one ace is hard and one is soft
    assert blackjack_engine.Hand([1,2,1]).is_soft == True

def test_Hand_is_soft_three_aces():
    # two aces are hard and one is soft
    assert blackjack_engine.Hand([1,1,1,3]).is_soft == True

def test_Hand_total_three_aces_hard():
    # three aces, all are hard
    assert blackjack_engine.Hand([5,1,1,5,1]).is_soft == False

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

def test_Hand_add_card_busted():
    hand = blackjack_engine.Hand([1,2,12,13])
    with pytest.raises(BustedHand):
        hand.add_card(5)

def test_Hand_init_busted():
    # can't initialize a busted hand
    assert False

# Deck tests
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

# Dealer bot tests
# dealer bot tests will fail if Hand tests fail unfortunately
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
