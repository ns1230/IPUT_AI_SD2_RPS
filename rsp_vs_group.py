!pip install timeout_decorator
!mkdir group_agents  # 各agent.pyファイルが入るディレクトリ

import os
import importlib
import timeout_decorator
# parameter
base_dir = "group_agents"
num_match = 10000  # 対戦数:デフォルトは10000

groups = os.listdir("group_agents")
groups = [x.split(".")[0] for x in groups if x[:3]=="rsp"]  # ファイル名はrsp_group_k.pyに限定（k部分はグループ番号）

import pandas as pd
import numpy as np
TEAM_NUM = 3  # 1チームの構成エージェント数
num_agents = len(groups)*TEAM_NUM  # リーグ戦に参加する全エージェント数
agents = []
for i in range(len(groups)):
    x = groups[i].split("_")[-1]  # groups[i1]のグループ番号（文字型）
    for j in range(1,TEAM_NUM+1):
        agents.append(f"agent{x}_{j}")  # 各グループのエージェントにグループ名＋番号で名付け
scores = pd.DataFrame(np.zeros((num_agents,num_agents)),columns=agents,index=agents)

print(scores)

# 勝敗の判定  1:先手、2:後手、-1:ドロー、h1:先手の手、h2:後手の手
# hand: {0:"rock", 1:"scisors", 2:"paper"}
def judge(h1,h2):
    if h1 not in [0,1,2]:  # 想定外の手は-1とする
        h1 = -1
    if h2 not in [0,1,2]:  # 想定外の手は-1とする
        h2 = -1
    if h1==h2:
        return -1  # 引き分け
    elif (h1==0 and h2==1) or (h1==1 and h2==2) or (h1==2 and h2==0) or h2==-1:  # r,s,p以外の手を出したら負け
        return 1  # h1勝ち
    elif (h2==0 and h1==1) or (h2==1 and h1==2) or (h2==2 and h1==0) or h1==-1:  # r,s,p以外の手を出したら負け
        return 2  # h2勝ち

%%time
# 総当たり戦
for i1 in range(len(groups)-1):  # 団体戦の1グループ目=group1
    group1 = importlib.import_module(base_dir+"."+groups[i1])  # group1のファイル読み込み
    x1 = groups[i1].split("_")[-1]  # group1=groups[i1]のグループ番号（文字型）
    flag1 = [1 for _ in range(TEAM_NUM)]  # groups[i1]の各エージェントの実体化チェック
    agent1 = [0 for _ in range(TEAM_NUM)]  # groups[i1]の各エージェントが入る箱
    for j1 in range(TEAM_NUM):
        try:
            exec(f"agent1[{j1}]=group1.RSP_Agent_{j1+1}(num_match=num_match)")  # groups[i1]のj1番目のエージェントの実体化
        except:
            flag1[j1] = 0  # 実体化失敗の場合
    for i2 in range(i1+1,len(groups)):  # 団体戦の２グループ目=group2(=group1の相手)
        group2 = importlib.import_module(base_dir+"."+groups[i2])  # group2のファイル読み込み
        x2 = groups[i2].split("_")[-1]  # group2=groups[i2]のグループ番号（文字型）
        flag2 = [1 for _ in range(TEAM_NUM)]  # groups[i2]の各エージェントの実体化チェック
        agent2 = [0 for _ in range(TEAM_NUM)]  # groups[i2]の各エージェントが入る箱
        for j2 in range(TEAM_NUM):
            try:
                exec(f"agent2[{j2}]=group2.RSP_Agent_{j2+1}(num_match=num_match)")  # groups[i2]のj2番目のエージェントの実体化
            except:
                flag2[j2] = 0  # 実体化失敗の場合
        for j in range(TEAM_NUM):  # 各チームj番目のメンバどうしの対戦開始
            if flag1[j]==0 or flag2[j]==0:  # どちらかの実体化にバグがあった場合はバグがあった方のスコアを0にして対戦終了
                score1 = flag1[j]
                score2 = flag2[j]
            else:  # j番目のagentどうしの対戦
                score1 = 0
                score2 = 0
                for k in range(num_match):  # num_match=10000
                    try:
                        hand1 = agent1[j].output_hand()  # 先手の手の生成
                    except:
                        hand1 = -1  # 手の生成に失敗
                    try:
                        hand2 = agent2[j].output_hand()  # 後手の手の生成
                    except:
                        hand2 = -1  # 手の生成に失敗
                    win = judge(hand1,hand2)  # 判定：どっちが勝ったか（1:先手、2:後手）
                    if win==1:
                        score1 += 1
                    elif win==2:
                        score2 += 1
                    try:  # 相手の手{-1,0,1,2}を記憶する
                        agent1[j].get_hand(hand2)
                        agent2[j].get_hand(hand1)
                    except:
                        pass
                score1 = score1/num_match  # 勝率に変換
                score2 = score2/num_match  # 勝率に変換
            # 対戦スコアへ記入
            scores.loc[f"agent{x1}_{j+1}",f"agent{x2}_{j+1}"] = score1
            scores.loc[f"agent{x2}_{j+1}",f"agent{x1}_{j+1}"] = score2

# 最終スコア: 各agentのスコア合計
col = scores.columns
for agent in scores.index:
    scores.loc[agent,"total"] = scores.loc[agent,col].sum()

scores  # 最後の列がエージェント毎のトータルスコア

for agent in scores.index:
    scores.loc[agent,"group"] = agent.split("_")[0][5:]

print(scores)

res = scores[["group","total"]].groupby("group").sum()  # グループ毎にスコアをまとめる
print(res)



