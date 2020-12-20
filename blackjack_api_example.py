import blackjack_engine

def player_bot(hand):
    """ makes random choice, or makes decisions using neural net etc"""
    # decision making code goes here
    pass

def play_blackjack_game():
    # initialize a game with shuffled deck and hands dealt to dealer and player:
    game = blackjack_engine.BlackjackGame()

    # loop until game is over
    while True: 
        # Pass the current player hand to the decision maker function,
        # and return the decision (hit or stay):
        hit_or_stay = player_bot(game.player_hand)
        # Pass the player decision to the game, which will act on the player
        # decision and continue through the game logic
        # until either the game is finished or until it's 
        # time for the player to make another decision.
        # The BlackjackGame class handles the game logic and updates the
        # hands and deck as necessary.
        game.player_move(hit_or_stay)
        if game.result == None:
            continue # game is not finished so continue loop
        if game.result == 'win' or game.result == 'loss' or game.result == 'blackjack':
            break # game is finished so exit loop

    # return game (instance of BlackjackGame), which contains all the info about the game
    return game

# simulate a game using above functions
game = play_blackjack_game()
print("game result: ", game.result)
print("final player hand: ", game.player_hand)
print("final dealer hand: ", game.dealer_hand)
print("player decisions: ", game.list_player_decisions())

# Example output:
# game result: 'win'
# final player hand: [5, 6, 3, 6]
# final dealer hand: [8, 8, 3]
# player decisions: ['hit', 'hit', 'stay']

