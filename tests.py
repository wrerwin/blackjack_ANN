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

## Hand.is_blackjack
def test_Hand_is_blackjack_True():
    assert blackjack_engine.Hand(['A','Q']).is_blackjack == True

def test_Hand_is_blackjack_True():
    assert blackjack_engine.Hand(['A','9']).is_blackjack == False

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
    # can't add card to a busted hand
    hand = blackjack_engine.Hand(['A','2','Q','K'])
    with pytest.raises(RuntimeError):
        hand.add_card('5')

def test_Hand_add_card_21():
    # can't add a card to a 21 hand (non-blackjack)
    hand = blackjack_engine.Hand(['10','2','9'])
    with pytest.raises(RuntimeError):
        hand.add_card('4')

## Hand initialization
def test_Hand_init_busted():
    # can initialize a busted hand, but only if the last card
    # was the one that busted it
    hand = blackjack_engine.Hand(['J','8','8']) 
    with pytest.raises(RuntimeError):
        hand = blackjack_engine.Hand(['J','8','8','8']) 

def test_Hand_init_one_card():
    # can't initialize a hand with one card since that's not
    # a valid hand
    with pytest.raises(ValueError):
        hand = blackjack_engine.Hand(['J']) 
        

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
    hand.stay()
    assert hand.is_stayed == True

def test_Hand_is_stayed_add_card():
    # can't add a card to a hand after stay
    hand = blackjack_engine.Hand(['A','8'])
    hand.stay()
    with pytest.raises(RuntimeError):
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

def test_Deck_seed():
    # seeding deck gives same deck every time
    # (not sure if this works cross-platform)
    seeded_deck = blackjack_engine.Deck(seed=1)
    assert seeded_deck.cards[:10] == ['J', '10', 'Q', '10', '3', 
                                     'K', '7', 'Q', '10', '6']
    assert seeded_deck.cards[-10:] == ['3', '5', '3', '6', '8', 
                                      '4', '5', '10', 'J', '9']

# check_winner tests
def test_Game_check_winner_player_blackjack():
    player_hand = blackjack_engine.Hand(['A', '10'])
    dealer_hand = blackjack_engine.Hand(['7', '10'])
    assert blackjack_engine.check_winner(player_hand, dealer_hand) == 2

def test_Game_check_winner_dealer_blackjack():
    player_hand = blackjack_engine.Hand(['2', '10'])
    dealer_hand = blackjack_engine.Hand(['J', 'A'])
    assert blackjack_engine.check_winner(player_hand, dealer_hand) == -1

def test_Game_check_winner_both_blackjack():
    player_hand = blackjack_engine.Hand(['A', '10'])
    dealer_hand = blackjack_engine.Hand(['J', 'A'])
    assert blackjack_engine.check_winner(player_hand, dealer_hand) == 0

def test_Game_check_winner_player_bust():
    player_hand = blackjack_engine.Hand(['5', '10', '8'])
    dealer_hand = blackjack_engine.Hand(['3', '2'])
    assert blackjack_engine.check_winner(player_hand, dealer_hand) == -1

def test_Game_check_winner_dealer_bust():
    player_hand = blackjack_engine.Hand(['5', '10', '4'])
    dealer_hand = blackjack_engine.Hand(['6', '8', '10'])
    assert blackjack_engine.check_winner(player_hand, dealer_hand) == 1

def test_Game_check_winner_both_bust():
    player_hand = blackjack_engine.Hand(['5', '10', '10'])
    dealer_hand = blackjack_engine.Hand(['6', '8', '10'])
    assert blackjack_engine.check_winner(player_hand, dealer_hand) == -1

def test_Game_check_winner_player_high():
    player_hand = blackjack_engine.Hand(['5', '10', '5'])
    dealer_hand = blackjack_engine.Hand(['6', '8', '5'])
    assert blackjack_engine.check_winner(player_hand, dealer_hand) == 1

def test_Game_check_winner_player_21():
    player_hand = blackjack_engine.Hand(['5', 'K', '6'])
    dealer_hand = blackjack_engine.Hand(['6', '8', '5'])
    assert blackjack_engine.check_winner(player_hand, dealer_hand) == 1

def test_Game_check_winner_dealer_high():
    player_hand = blackjack_engine.Hand(['9', '8'])
    dealer_hand = blackjack_engine.Hand(['5', 'K', '4'])
    assert blackjack_engine.check_winner(player_hand, dealer_hand) == -1

def test_Game_check_winner_dealer_21():
    player_hand = blackjack_engine.Hand(['9', '10'])
    dealer_hand = blackjack_engine.Hand(['4', 'J', '7'])
    assert blackjack_engine.check_winner(player_hand, dealer_hand) == -1


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

# Game tests
def test_Game_full_push_1():
    # both dealt 20s, both stay, push
    # player_hands: [[J 10], total: 20]
    # dealer_hand: [Q 10], total: 20
    seeded_deck = blackjack_engine.Deck(seed=1)
    game = blackjack_engine.BlackjackGame(deck=seeded_deck)
    assert game.is_finished == False
    game.player_move('stay')
    assert game.is_finished == True
    assert game.player_hands[0].cards == ['J', '10']
    assert game.dealer_hand.cards == ['Q', '10']
    assert game.result == 0

def test_Game_full_push_2():
    # player hits to 19, dealer stays, push
    # initial player hand: [3 4], total: 7
    # initial dealer hand: [10 9], total: 19
    seeded_deck = blackjack_engine.Deck(seed=2)
    game = blackjack_engine.BlackjackGame(deck=seeded_deck)
    game.player_move('hit')  # [[3 4 5], total: 12]
    game.player_move('hit')  # [[3 4 5 7], total: 19]
    assert game.is_finished == False
    game.player_move('stay')
    assert game.is_finished == True
    assert game.player_hands[0].cards == ['3', '4', '5', '7']
    assert game.dealer_hand.cards == ['10', '9']
    assert game.result == 0

def test_Game_full_loss_1():
    # player hits to hard 19, dealer hits to 21, player loses
    # initial player hand: [A 3], total: 14
    # initial dealer hand: [4 7], total: 11
    seeded_deck = blackjack_engine.Deck(seed=3)
    game = blackjack_engine.BlackjackGame(deck=seeded_deck)
    game.player_move('hit')  # [[A 3 4], total: 18]
    game.player_move('hit')  # [[A 3 4 A], total: 19]
    game.player_move('hit')  # [[A 3 4 A K], total: 19]
    assert game.is_finished == False
    game.player_move('stay')
    assert game.is_finished == True
    assert game.player_hands[0].cards == ['A', '3', '4', 'A', 'K']
    assert game.dealer_hand.cards == ['4', '7', '10']
    assert game.result == -1

def test_Game_full_win_1():
    # player hits on 16, wins with 21
    # initial player hand [Q 6], total: 16
    # initial dealer hand [10 K], total: 20
    seeded_deck = blackjack_engine.Deck(seed=5)
    game = blackjack_engine.BlackjackGame(deck=seeded_deck)
    print('initial player hand', game.player_hands[0])
    print('initial dealer hand', game.dealer_hand)
    assert game.is_finished == False
    game.player_move('hit')  
    print('new player hand: ', game.player_hands)
    assert game.is_finished == True
    print('final dealer hand: ', game.dealer_hand)
    assert game.player_hands[0].cards == ['Q', '6', '5']
    assert game.dealer_hand.cards == ['10', 'K']
    assert game.result == 1

def test_Game_full_win_2():
    # player hits to hard 18, dealer hits to hard 17, player wins
    # initial player hand [Q 10], total: 20
    # initial dealer hand [A 9], total: 20
    seeded_deck = blackjack_engine.Deck(seed=7)
    game = blackjack_engine.BlackjackGame(deck=seeded_deck)
    print('initial player hand', game.player_hands[0])
    print('initial dealer hand', game.dealer_hand)
    assert game.is_finished == False
    game.player_move('hit')  
    print('player hand 2: ', game.player_hands)
    game.player_move('hit')  
    print('player hand 3: ', game.player_hands)
    game.player_move('stay')  
    assert game.is_finished == True
    print('final dealer hand: ', game.dealer_hand)
    assert game.player_hands[0].cards == ['5', 'A', '2', 'Q']
    assert game.dealer_hand.cards == ['6', 'J', 'A']
    assert game.result == 1

def test_Game_full_win_3():
    # player dealt blackjack, player wins
    # initial player hand [10 A], total: 21
    # initial dealer hand [J 6], total: 16
    seeded_deck = blackjack_engine.Deck(seed=63)
    game = blackjack_engine.BlackjackGame(deck=seeded_deck)
    print('initial player hand', game.player_hands[0])
    print('initial dealer hand', game.dealer_hand)
    assert game.is_finished == True
    print('final dealer hand: ', game.dealer_hand)
    assert game.player_hands[0].cards == ['10', 'A']
    # assert game.dealer_hand.cards == ['J', '6'] # behavior undefined?
    assert game.result == 2
                                                 
# def test_Game_template():
#     # player...
#     # initial player hand: 
#     # initial dealer hand: 
#     seeded_deck = blackjack_engine.Deck(seed=4)
#     game = blackjack_engine.BlackjackGame(deck=seeded_deck)
#     print('initial player hand', game.player_hands[0])
#     print('initial dealer hand', game.dealer_hand)
#     assert game.is_finished == False
#     game.player_move('hit')  
#     print('player hand 2: ', game.player_hands)
#     game.player_move('hit')  
#     print(game.player_hands)
#     print('player hand 3: ', game.player_hands)
#     game.player_move('hit')  
#     print('player hand 4: ', game.player_hands)
#     game.player_move('hit')
#     print('player hand 5: ', game.player_hands)
#     game.player_move('hit')
#     print('player hand 6: ', game.player_hands)
#     game.player_move('hit')
#     print('player hand 7: ', game.player_hands)
#     game.player_move('hit')
#     print('player hand 8: ', game.player_hands)
#     game.player_move('hit')
#     print('player hand 9: ', game.player_hands)
#     game.player_move('hit')
#     print('player hand 10: ', game.player_hands)
#     game.player_move('hit')
#     print('player hand 11: ', game.player_hands)
#     game.player_move('hit')
#     print('player hand 12: ', game.player_hands)
#     print('final dealer hand: ', game.dealer_hand)
#     assert game.player_hands[0].cards == ['A']
#     assert game.dealer_hand.cards == ['4']
#     assert game.result == -2
                         
