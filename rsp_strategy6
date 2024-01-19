#ver.6   It keeps track of the opponent's previous moves and compares them with the current history of moves. 
        #If a match is found, it plays the move that follows the matched history. Otherwise, it chooses a random move. 
        #This strategy attempts to predict the opponent's next move based on patterns observed in previous moves and exploit those patterns to gain an advantage.

import timeout_decorator
import time
import numpy as np
import random
import math

class RSP_Agent:
    def __init__(self, num_match=10000):
        self.cnt = 0
        self.num_match = num_match
        self.my_hands = []
        self.oppo_hands = []
        self.debug_seek = []


    @timeout_decorator.timeout(1)
    def output_hand(self):
        last_oppo_hand = self.oppo_hands[-1] if self.oppo_hands else None
        self.debug_seek = last_oppo_hand

        if last_oppo_hand is None:
            # If no previous move is available, choose a random move
            hand = random.randint(0, 2)
        else:
            # Perform statistical analysis based on previous moves
            move_counts = defaultdict(int)
            for i in range(len(self.oppo_hands) - 1):
                history = tuple(self.oppo_hands[i:i+1] + self.my_hands[i:i+1])
                move_counts[history] += 1

            # Find the most frequent opponent move following your move
            max_frequency = 0
            most_frequent_move = None
            for i in range(3):
                history = (last_oppo_hand, i)
                frequency = move_counts[history]
                if frequency > max_frequency:
                    max_frequency = frequency
                    most_frequent_move = i

            if most_frequent_move is not None:
                # If a statistically significant correlation is found, play the move that maximizes your chances of winning against the pattern
                hand = (most_frequent_move + 2) % 3
            else:
                # If no significant correlation is found, choose a random move
                hand = random.randint(0, 2)

        self.my_hands.append(hand)
        return hand
