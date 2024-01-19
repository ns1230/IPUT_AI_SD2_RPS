!pip install timeout_decorator
!mkdir agents  # 各agent.pyファイルが入るディレクトリ

import os
import importlib  # ライブラリをインポートするためのモジュール
import timeout_decorator  # colab環境限定：Windows上ではうまく動かない
import pandas as pd
import numpy as np

# parameter
base_dir = "agents"
num_match = 10000  # 対戦数:デフォルトは10000

agents = os.listdir("agents")
agents = [x.split(".")[0] for x in agents if x[:3]=="rsp"] 

print(agents)

num_agents = len(agents)  # 対戦にエントリーしたエージェントの数
scores = pd.DataFrame(np.zeros((num_agents,num_agents)),columns=agents,index=agents)  # 対戦表
print(scores)

# 勝敗の判定  0:先手、1:後手、-1:ドロー、    h0:先手の手、h1:後手の手
# hand: {0:"rock", 1:"scisors", 2:"paper"}
def judge(h0,h1):
    if h0 not in [0,1,2]:  # 想定外の手は-1とする
        h0 = -1
    if h1 not in [0,1,2]:  # 想定外の手は-1とする
        h1 = -1
    if h0==h1:
        return -1  # 引き分け
    elif (h0==0 and h1==1) or (h0==1 and h1==2) or (h0==2 and h1==0) or h1==-1:  # r,s,p以外の手を出したら負け
        return 0  # h0を出した人が勝ち
    elif (h1==0 and h0==1) or (h1==1 and h0==2) or (h1==2 and h0==0) or h0==-1:  # r,s,p以外の手を出したら負け
        return 1  # h1を出した人が勝ち

# 総当たり戦
%%time
debug_agent0 = []
debug_agent1 = []
debug_me = []
for i in range(num_agents-1):
    flag0 = 1  # エージェントがちゃんと実体化できたかどうかのフラグ
    flag1 = 1  # エージェントがちゃんと実体化できたかどうかのフラグ
    for j in range(i+1,num_agents):
        try:
            agent0 = importlib.import_module(base_dir+"."+agents[i])  # クラスファイルの読み込み
            agent0 = agent0.RSP_Agent(num_match=num_match)  # 先手のエージェントを実体化,引数は対戦回数
        except:
            flag0 = 0  # 上の処理でエラーが出た場合
        try:
            agent1 = importlib.import_module(base_dir+"."+agents[j])  # クラスファイルの読み込み
            agent1 = agent1.RSP_Agent(num_match=num_match)  # 後手のエージェントを実体化、引数は対戦回数
        except:
            flag1 = 0  # 上の処理でエラーが出た場合
        if flag0==0 or flag1==0:  # どちらかの実体化にエラーが発生
            # 実体化に失敗した方は勝ち点０，成功した方は勝ち点１で対戦終了
            score0 = flag0
            score1 = flag1
        else:  # 対戦
            # スコアを初期化
            score0 = 0
            score1 = 0
            for k in range(num_match):  # num_match=1000⇒1000回対戦する
                try:
                    hand0 = agent0.output_hand()  # 先手の手の生成
                except:
                    hand0 = -1  # 手の生成に失敗
                try:
                    hand1 = agent1.output_hand()  # 後手の手の生成
                except:
                    hand1 = -1  # 手の生成に失敗したとき
                x = judge(hand0,hand1)  # 判定：どっちが勝ったか（0:先手、1:後手）

                if x==0:
                    score0 += 1
                elif x==1:
                    score1 += 1
                try:  # 相手の手を記憶する
                    agent0.get_hand(hand1)
                    agent1.get_hand(hand0)
                except:
                    pass
            # 勝率の計算
            score0 = score0/num_match
            score1 = score1/num_match
        # 対戦スコアへ記入
        scores.loc[agents[i],agents[j]] = score0
        scores.loc[agents[j],agents[i]] = score1

# 最終スコア
col = scores.columns
for agent in scores.index:
    scores.loc[agent,"total"] = scores.loc[agent,col].sum()
