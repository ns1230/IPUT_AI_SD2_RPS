#ver.2 - 相手の一個前と同じ

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
            # Implement a rule-based strategy based on the opponent's last move
            if last_oppo_hand == 0:  # Opponent played "Rock"
                hand = 0  # Choose "Paper" to counter
            elif last_oppo_hand == 1:  # Opponent played "Scissors"
                hand = 1  # Choose "Rock" to counter
            else:  # Opponent played "Paper"
                hand = 2  # Choose "Scissors" to counter
        
        self.my_hands.append(hand)
        return hand
