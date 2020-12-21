import blackjack_engine
import random

def player_bot(hand):
    """ makes random choice, or makes decisions using neural net etc"""
    # decision making code goes here
    return random.choice(['hit', 'stay'])   

def play_blackjack_game():
    # initialize a game with shuffled deck and hands dealt to dealer and player:
    game = blackjack_engine.BlackjackGame()
    print('initial player hand: ', game.player_hand.cards)
    print('initial dealer hand: ', game.dealer_hand.cards, '\n')

    if game.is_finished == False:
        # loop until game is over
        while True: 
            hit_or_stay = player_bot(game.player_hand)
            print('player will ', hit_or_stay, '\n')
            game.player_move(hit_or_stay)
            # print('player hand: ', game.player_hand.cards)
            # print('dealer hand: ', game.dealer_hand.cards, '\n')
            if game.result == None:
                continue # game is not finished so continue loop
            if game.result in [-1, 0, 1, 1.5]:
                break # game is finished so exit loop

    return game

# simulate a game using above functions
game = play_blackjack_game()
print("Game result: ", game.result)
print("Final player hand: ", game.player_hand.cards)
print("Final dealer hand: ", game.dealer_hand.cards)

# Example output:
# game result: 'win'
# final player hand: [5, 6, 3, 6]
# final dealer hand: [8, 8, 3]

