from pathlib import Path
import numpy as np
import datetime
import pandas as pd


"""

行動ログの作成

"""

action_data_dir_path = Path('./action_data')
if not action_data_dir_path.exists():
    action_data_dir_path.mkdir(parents=True)

## 行動の定義
start_action = 'top'
pages = ['page1','page2', 'page3', 'page4', 'page5']
buttons = ['like','purchase']

## ページ遷移の重み設定
## ページ5よりページ１のほうが5倍出現しやすい
pages_weights = np.array([5, 3, 2, 1.5, 1])
pages_weights = pages_weights / pages_weights.sum()


n_id = 100                         # id数
max_action = 12                    # 遷移行動数の最大
action_datas = pd.DataFrame()
for id in range(n_id):

    # 遷移行動数の決定
    n_action = np.random.randint(1, max_action)
    now = datetime.datetime.now()

    if n_action - 1 >0:
        # 遷移行動数をページ遷移とボタンで分配
        n_page = n_action - 1 - np.random.randint(0, n_action-1)
        # page_weightsの確率でページ遷移リストの中からn_page個ランダムに選択
        pages_ = np.random.choice(pages, n_page, replace=True, p=pages_weights)
        # 残りの行動遷移数をボタンリストの中からランダムに選択
        buttons_ = np.random.choice(buttons, n_action-n_page-1, replace=True)
        actions = np.random.choice(np.r_[pages_, buttons_], n_action-1, replace=False)
        # topと結合
        actions = np.r_[np.array([start_action]), actions]

        # 行動ログっぽくするため時間も付与
        dates = [(now + datetime.timedelta(seconds=i)).strftime('%Y-%m-%d %H:%M:%S') for i in range(1, n_action + 1)]
    else:
        actions = [start_action]
        dates = [now.strftime('%Y-%m-%d %H:%M:%S')]

    data = pd.DataFrame(np.array([[id]*n_action,
                                  actions,
                                  dates]).T, columns=['id', 'action_name', 'date'])
    action_datas = pd.concat([action_datas, data], axis=0)

action_datas.to_csv(action_data_dir_path.joinpath('action_data.tsv'),
                    index=False, sep='\t', encoding='utf-8')


