#ver.3  Win-Stay, Lose-Shift: In this strategy, you remember your own previous move and repeat it if you win, but switch to a different move if you lose. 
        #This strategy aims to capitalize on winning streaks and adapt to break losing streaks.

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

    def output_hand(self):
        last_oppo_hand = self.oppo_hands[-1] if self.oppo_hands else None
        self.debug_seek = last_oppo_hand

        if last_oppo_hand is None:
            # If no previous move is available, choose a random move
            hand = random.randint(0, 2)
        else:
            if self.cnt > 1 and self.my_hands[-1] == self.oppo_hands[-1]:
                # If the agent won or drew the previous round, repeat the same move
                hand = self.my_hands[-1]
            else:
                # If the agent lost, shift to a different move
                hand = (self.my_hands[-1] + 1) % 3  # Choose the next move in a cyclic manner

        self.my_hands.append(hand)
        return hand
