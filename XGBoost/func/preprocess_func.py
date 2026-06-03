from setting.config import cat_order_map

from pandas.api.types import CategoricalDtype
from sklearn.preprocessing import StandardScaler, LabelEncoder

def preprocess(target, features_df, numeric_feature, categorical_feature, task_type, spec_type = None):

    # 特殊映射
    if spec_type is not None:
        target, df = spec_process(target, features_df, spec_type)

    # 处理 target 是分类的情况
    if task_type == 'classification': # 处理target是分类的情况，将其编码
        le_target = LabelEncoder()
        target = le_target.fit_transform(target)
    else: # 不是分类则不做
        le_target = None

    # 处理 feature 中是分类的列
    df = features_df.copy() if spec_type is None else df.copy() # 如果 spec_process 已经做了拷贝，这里避免重复；若无，则复制
    for c in categorical_feature:
        if c in df.columns:
            if c in cat_order_map: # 显式指定映射方式
                cat_type = CategoricalDtype(categories=cat_order_map[c], ordered=False)
                df[c] = df[c].astype(cat_type)
            else:
                df[c] = df[c].astype('category') # 没有显式定义的列保持默认（训练数据中的出现顺序）

    # 处理 feature 中是数值的列
    scaler = StandardScaler() # 处理数值特征
    num_cols = [c for c in numeric_feature if c in df.columns]
    if num_cols:
        df[num_cols] = scaler.fit_transform(df[num_cols])

    return target, df, le_target, scaler # 返回处理后的目标、特征、以及需要的转换器

def spec_process(target, df, spec_type):
    if spec_type == "sleep_disorder_risk":
        mapping = {'Healthy': 0.125, 'Mild': 0.375, 'Moderate': 0.625, 'Severe': 0.875}
        target = target.map(mapping)
        print(target)
    return target, df