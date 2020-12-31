import blackjack_engine
import pytest


# Hand tests
## Hand.total
def test_Hand_total_22_no_aces():
    assert blackjack_engine.Hand(['K','5','7']).total == 22

def test_Hand_total_19_no_aces():
    assert blackjack_engine.Hand(['10','9']).total == 19

def test_Hand_total_soft_17():
    assert blackjack_engine.Hand(['A','6']).total == 17

def test_Hand_total_hard_17():
    assert blackjack_engine.Hand(['A','9','7']).total == 17

def test_Hand_total_hard_22():
    assert blackjack_engine.Hand(['A','9','6','6']).total == 22

def test_Hand_total_two_aces():
    # one ace is hard and one is soft
    assert blackjack_engine.Hand(['A','2','A']).total == 14

def test_Hand_total_three_aces():
    # two aces are hard and one is soft
    assert blackjack_engine.Hand(['A','A','A','3']).total == 16

def test_Hand_total_three_aces_hard():
    # three aces, all are hard
    assert blackjack_engine.Hand(['5','A','A','5','A']).total == 13

def test_Hand_total_three_aces():
    # two aces are hard and one is soft
    assert blackjack_engine.Hand(['A','A','A','3']).total == 16

def test_Hand_total_three_aces_hard():
    # three aces, all are hard
    assert blackjack_engine.Hand(['5','A','A','5','A']).is_soft == False

## Hand.is_soft
def test_Hand_is_soft_22_no_aces():
    assert blackjack_engine.Hand(['K','5','7']).is_soft == False

def test_Hand_is_soft_19_no_aces():
    assert blackjack_engine.Hand(['10','9']).is_soft == False

def test_Hand_is_soft_soft_17():
    assert blackjack_engine.Hand(['A','6']).is_soft == True

def test_Hand_is_soft_hard_17():
    assert blackjack_engine.Hand(['A','9','7']).is_soft == False

def test_Hand_is_soft_hard_22():
    assert blackjack_engine.Hand(['A','9','6','6']).is_soft == False

def test_Hand_is_soft_two_aces():
    # one ace is hard and one is soft
    assert blackjack_engine.Hand(['A','2','A']).is_soft == True

def test_Hand_is_soft_three_aces():
    # two aces are hard and one is soft
    assert blackjack_engine.Hand(['A','A','A','3']).is_soft == True

## Hand.add_card
def test_Hand_add_card_goodcard():
    hand = blackjack_engine.Hand(['A','2'])
    hand.add_card('A')
    assert hand.cards == ['A','2','A']
    hand = blackjack_engine.Hand(['10','10'])
    hand.add_card('7')
    assert hand.cards == ['10','10','7']
    hand = blackjack_engine.Hand(['2','2'])
    hand.add_card('7')
    hand.add_card('5')
    assert hand.cards == ['2','2','7','5']

def test_Hand_add_card_badcard():
    hand = blackjack_engine.Hand(['A','2','Q','7'])
    with pytest.raises(ValueError):
        hand.add_card('15')
    with pytest.raises(ValueError):
        hand.add_card(9)
    with pytest.raises(ValueError):
        hand.add_card(0)
    with pytest.raises(ValueError):
        hand.add_card('1.5')
    with pytest.raises(ValueError):
        hand.add_card('cat')

def test_Hand_add_card_busted():
    hand = blackjack_engine.Hand(['A','2','Q','K'])
    with pytest.raises(blackjack_engine.BustedHand):
        hand.add_card('5')

## Hand initialized busted
def test_Hand_init_busted():
    # can initialize a busted hand, but only if the last card
    # was the one that busted it
    hand = blackjack_engine.Hand(['J','8','8']) 
    with pytest.raises(blackjack_engine.BustedHand):
        hand = blackjack_engine.Hand(['J','8','8','8']) 

## Hand.is_pair
def test_Hand_is_pair_two_numbers():
    hand = blackjack_engine.Hand(['3','3'])
    assert hand.is_pair == True

def test_Hand_is_pair_two_aces():
    hand = blackjack_engine.Hand(['A','A'])
    assert hand.is_pair == True

def test_Hand_is_pair_two_same_faces():
    hand = blackjack_engine.Hand(['Q','Q'])
    assert hand.is_pair == True

def test_Hand_is_pair_two_diff_faces():
    hand = blackjack_engine.Hand(['Q','K'])
    assert hand.is_pair == True

def test_Hand_is_pair_face_and_10():
    hand = blackjack_engine.Hand(['K','10'])
    assert hand.is_pair == True

def test_Hand_is_pair_not_pair():
    hand = blackjack_engine.Hand(['A','8'])
    assert hand.is_pair == False

## Hand.is_stayed
def test_Hand_is_stayed_False():
    hand = blackjack_engine.Hand(['A','8'])
    assert hand.is_stayed == False
    
def test_Hand_is_stayed_True():
    hand = blackjack_engine.Hand(['A','8'])
    hand.is_stayed = True
    assert hand.is_stayed == True

def test_Hand_is_stayed_ValueError():
    hand = blackjack_engine.Hand(['A','8'])
    with pytest.raises(ValueError):
        hand.is_stayed = 'cat'

def test_Hand_is_stayed_add_card():
    # can't add a card to a hand after stay
    hand = blackjack_engine.Hand(['A','8'])
    hand.is_stayed = True
    with pytest.raises(blackjack_engine.StayedHand):
        hand.add_card('2')
    

# Deck tests
def test_Deck_draw_card():
    my_deck = blackjack_engine.Deck()
    assert len(my_deck.cards) == 52
    card = my_deck.draw_card()
    assert card in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
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
    hand = blackjack_engine.Hand(['J','6']) 
    assert blackjack_engine.dealer_bot(hand) == 'hit'

def test_dealer_bot_hard_17():
    hand = blackjack_engine.Hand(['J','6','A'])
    assert blackjack_engine.dealer_bot(hand) == 'stay'

def test_dealer_bot_soft_17():
    hand = blackjack_engine.Hand(['A','6'])
    assert blackjack_engine.dealer_bot(hand) == 'hit'

def test_dealer_bot_20():
    hand = blackjack_engine.Hand(['Q','4','6'])
    assert blackjack_engine.dealer_bot(hand) == 'stay'

def test_dealer_bot_hard_20():
    hand = blackjack_engine.Hand(['A','2','Q','7'])
    assert blackjack_engine.dealer_bot(hand) == 'stay'

