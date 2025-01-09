# Probabilistic-Robotics-Problem
確率ロボティクスの課題提出用のリポジトリ

## Description
1次元の数直線上を右に動くロボットにmclを実装したものになります.

## 実行例
実行すると以下のような画面が現れ, ロボットが右向きに動き始めます. \

ロボットが動くとロボットの軌道直線上に矢印で示した, ランドマークを観測すると狭まります. \
また、ランドマークを観測している間は、ランドマークが青色に変化します.\
<img src="resource/mcl_demo.gif">

## 実行手順
1) ターミナル上でインストールするディレクトリに移動
```
cd path_to_your_directory
```
2) インストール
```
git clone https://github.com/21C1072takahashishoku/Probabilistic-Robotics-Problem.git
```
3) 実行
```
cd mcl
./main.py
```

## 動作確認済み環境
- Python 3.8.10
- Ubuntu 20.04

## 参考
- 上田隆一『詳解 確率ロボティクス -Pythonによる基礎アルゴリズムの実装-』講談社, 2019年.
- https://qiita.com/NaokiAkai/items/44b2a160e47a8de44abf
