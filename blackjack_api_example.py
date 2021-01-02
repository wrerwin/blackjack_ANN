import blackjack_engine
import random

def player_bot(hand):
    """ makes random choice, or makes decisions using neural net etc"""
    # decision making code goes here
    # return input('hit or stay? ')
    return random.choice(['hit', 'stay'])   

def play_blackjack_game():
    # initialize a game with shuffled deck and hands dealt to dealer and player:
    game = blackjack_engine.BlackjackGame()
    print('initial player hand: ', game.player_hands[0])
    print('initial dealer hand: ', game.dealer_hand, '\n')

    # check if game ended with blackjacks
    if game.is_finished == True:
        if game.result == 2:
            print('Player wins with blackjack')
        elif game.result == -1:
            print('Player loses, dealer blackjack')
    # otherwise, loop through player decisions until game is over 
    else:
        while True: 
            hit_or_stay = player_bot(game.player_hands)
            print('player will ', hit_or_stay)
            game.player_move(hit_or_stay)
            if hit_or_stay == 'hit':
                print('new player hand:', game.player_hands[0], '\n')
            if game.player_hands[0].is_busted:
                print('Player busted')
            # print('dealer hand: ', game.dealer_hand.cards, '\n')
            if game.is_finished == True:
                print('Final dealer hand:', game.dealer_hand)
                if game.result == -1:
                    print('Player loses')
                if game.result == 0:
                    print('Push')
                if game.result == 1:
                    print('Player wins')
                break # game is finished so exit loop

    return game

# simulate a game using above functions
game = play_blackjack_game()
print("Game result: ", game.result)
