from pathlib import Path
import pandas as pd


result_dir_path = Path('./result')
master_dir_path = Path('./original_data')


action_sequence_data = pd.read_csv(result_dir_path.joinpath('action_sequence.tsv'),
                                   sep='\t', encoding='utf-8')

action_sequence_data_sum = action_sequence_data.groupby(['action_from', 'action_to']).count()
action_sequence_data_sum = action_sequence_data_sum.reset_index()
action_sequence_data_sum = action_sequence_data_sum.ix[:, 0:3]
action_sequence_data_sum.columns = ['action_from', 'action_to', 'value']

action_sequence_data_sum.to_csv(result_dir_path.joinpath('sankey_data.tsv'), sep='\t', encoding='utf-8', index=False)

