import blackjack_engine
import random

def player_bot(hand):
    """ makes random choice, or makes decisions using neural net etc"""
    # decision making code goes here
    return random.choice(['hit', 'stay'])   

def play_blackjack_game():
    # initialize a game with shuffled deck and hands dealt to dealer and player:
    game = blackjack_engine.BlackjackGame()
    print('initial player hand: ', game.player_hands[0])
    print('initial dealer hand: ', game.dealer_hand, '\n')

    if game.is_finished == True:
        if game.result == 1.5:
            print('Player wins with blackjack')
        elif game.result == 0:
            print('Player loses, dealer blackjack')
    if game.is_finished == False:
        # loop until game is over
        while True: 
            hit_or_stay = player_bot(game.player_hands)
            print('player will ', hit_or_stay)
            game.player_move(hit_or_stay)
            print('new player hand:', game.player_hands[0], '\n')
            # print('dealer hand: ', game.dealer_hand.cards, '\n')
            if game.result in [-1, 0, 1, 1.5]:
                print('Final dealer hand:', game.dealer_hand)
                if game.result == None:
                    continue # game is not finished so continue loop
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
# print("Final player hand: ", game.player_hands.cards)
# print("Final dealer hand: ", game.dealer_hand.cards)

# Example output:
# game result: 'win'
# final player hand: [5, 6, 3, 6]
# final dealer hand: [8, 8, 3]

