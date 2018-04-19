from pathlib import Path
import pandas as pd
import numpy as np

"""
行動ログをSankey Diagramで扱えるような行動列に加工する

"""

action_dir_path = Path('./action_data')
result_dir_path = Path('./result')
if not result_dir_path.exists():
    result_dir_path.mkdir(parents=True)


data = pd.read_csv(action_dir_path.joinpath('action_data.tsv'),
                   encoding='utf-8',
                   sep='\t')

ids = sorted(np.unique(data['id']))
start_point = 'top'
end_points = ['purchase']

# action_from : 行動の基点
# action_to : action_fromに繋がる行動
# num_layer : 行動遷移番号
datas = [['id', 'action_from', 'action_to', 'num_layer', 'flag_end']]

for id in ids:
    tmp = data.ix[data['id'] == id, :].copy()
    end_index = len(tmp)
    action_names = tmp['action_name'].values

    i = 0
    num_layer = 0
    #  行動がTOP画面か否かで場合分け
    if end_index > 1:
        while i < end_index:
            # 終端になったらaciton_toをendとする
            if i == end_index-1:
                list_ = [id, action_names[i], 'end', num_layer, 1]
                num_layer += 1
            else:
                # 次の行動がtop画面になっている場合、action_toをendとする
                if action_names[i+1] == start_point:
                    list_ = [id, action_names[i], 'end', num_layer, 1]
                    num_layer = 0
                else:
                    list_ = [id, action_names[i], action_names[i + 1], num_layer, 0]
                    num_layer += 1
                    # 指定したゴールの行動がある場合、その行動がaction_fromにならないように飛ばす
                    if action_names[i+1] in end_points:
                        i += 1
                        num_layer = 0
            i += 1
            datas.append(list_)
    else:
        list_ = [id, action_names[0], 'end', 0, 1]
        id += 1
        datas.append(list_)


datas = pd.DataFrame(datas)
datas.to_csv(result_dir_path.joinpath('action_sequence.tsv'),
             index=False,
             sep='\t',
             encoding='utf-8',
             header=False)
