#ver.5 Statistical Analysis: calculates the frequency of the opponent's previous moves and chooses the move with the highest frequency as the next move. 
        #If there is a tie, it randomly selects one of the moves with the highest frequency. 
        #This strategy aims to exploit any patterns or biases in the opponent's play by analyzing their historical moves.

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
            # Perform statistical analysis based on opponent's previous moves
            freq = [0, 0, 0]  # Frequency of opponent's moves: [Rock, Paper, Scissors]
            for hand in self.oppo_hands:
                freq[hand] += 1

            # Choose the move with the highest frequency as the next move
            max_freq = max(freq)
            hand = freq.index(max_freq)

        self.my_hands.append(hand)
        return hand
