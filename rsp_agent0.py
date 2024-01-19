import timeout_decorator  # pipインストール必須
import time
import numpy as np
import random
import math
class RSP_Agent:
    def __init__(self,num_match=10000):  # インスタンス変数self.cnt,self.my_hands,self.oppo_hands,self.num_matchだけは固定。その他は自由に削除、追加OK.
        self.cnt = 0  # カウンター（今の相手と何回対戦したか）
        self.my_hands = []  # 自分の手の記録
        self.oppo_hands = []  # 相手の手の記録
        self.num_match = num_match  # １ゲームあたりの対戦回数

        self.x = np.random.randint(0,3)  # 0,1,2のどれかをランダムに取り出す⇒実体化する際に性格が決定される（戦略によっては使用しない変数）

    @timeout_decorator.timeout(1)  # 固定decorator
    def output_hand(self):  # 固定
        # 戻り値（hand)について必ずself.my_hands.append(hand)とする。
        # 戦略
        
        if self.x==0:
            self.p0 = 1  # probability of "Rock"
            self.p1 = 0  # probability of "Scisors"
            self.p2 = 0  # probability of "Paper"
        elif self.x==1:
            self.p0 = 0  # probability of "Rock"
            self.p1 = 1  # probability of "Scisors"
            self.p2 = 0  # probability of "Paper"
        else:
            self.p0 = 0  # probability of "Rock"
            self.p1 = 0  # probability of "Scisors"
            self.p2 = 1  # probability of "Paper"
        # 手の決定
        a = np.random.rand()
        if a<=self.p0:
            hand = 0
        elif a<=self.p0+self.p1:
            hand = 1
        else:
            hand = 2
        
        #hand = 0   #debug
        self.my_hands.append(hand)  # 戻り値をmy_handsに追加
        return hand
    def get_hand(self,oppo_hand):  # 関数名・中身固定
        self.cnt += 1
        self.oppo_hands.append(oppo_hand)
