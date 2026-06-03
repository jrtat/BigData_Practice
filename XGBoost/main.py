from func.train_func import train_xgboost_model, save_xgb_model
from setting.config import (id_column, numeric_feature, categorical_feature,
                            model_dict, data_path)
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

target_name = "felt_rested"
task_type = model_dict[target_name]["task_type"]
model_name = model_dict[target_name]["model_name"]
print(f"当前目标为: {target_name}，任务类型为: {task_type}")

df = pd.read_csv(data_path)
df.dropna(inplace=True) # 删除包含缺失值的行
df.drop_duplicates(inplace=True) # 删除完全重复的行
df_data = df.drop(columns=id_column) # 删除ID列，因为没啥用

xgb_model, scaler, num_feats, feat_order = train_xgboost_model(df_data, numeric_feature, categorical_feature,
                                target_name = target_name, task_type = task_type)

save_xgb_model(model_name, xgb_model, scaler, num_feats, feat_order)
