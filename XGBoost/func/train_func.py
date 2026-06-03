from func.preprocess_func import preprocess
from func.eval_func import eval_model, plot_feature_importance, shap_analysis
from setting.config import mask_feature_list

import numpy as np
import json
from sklearn.model_selection import train_test_split
import xgboost as xgb

def train_xgboost_model(df_data, numeric_feature, categorical_feature, target_name, task_type):

    mask_feature = mask_feature_list[target_name]
    feature = df_data.drop(columns=[target_name]) # 去除目标列
    feature = feature.drop(columns=mask_feature) # 去除mask列
    target = df_data[target_name] # 提出目标列

    num_feats = [c for c in numeric_feature if c in feature.columns] # 从特征列提出数值列
    cat_feats = [c for c in categorical_feature if c in feature.columns] # 从特征列提出分类列
    target, feature, le, scaler = preprocess(target, feature, num_feats, cat_feats, task_type, spec_type = target_name) # 归一化 和 数值化

    x_train, x_test, y_train, y_test = train_test_split(
        feature, target, test_size=0.2, random_state=42,
        stratify=(target if task_type == 'classification' else None)
    ) # 划分训练集和测试集
    x_test, x_val, y_test, y_val = train_test_split(
        x_test, y_test, test_size=0.5, random_state=42,
        stratify=(y_test if task_type == 'classification' else None)
    ) # 进一步划分测试集和验证集

    if task_type == 'regression': # 回归任务
        model = xgb.XGBRegressor(
            n_estimators=300, # 梯度提升树的数量
            learning_rate=0.05, # 学习率
            max_depth=8, # 每棵树的最大深度。深度越大，模型越复杂，更容易捕捉交互特征，但也更容易过拟合。
            enable_categorical=True, # 启用对类别型特征的直接支持，允许输入数据中存在 category 类型的列
            random_state=42,
            eval_metric='rmse',  # 回归指标
            early_stopping_rounds=20 # 早停轮数
        )
    elif task_type == 'classification': # 分类任务
        model = xgb.XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=8,
            enable_categorical=True,
            random_state=42,
            eval_metric='mlogloss' if len(np.unique(target)) > 2 else 'logloss',
            early_stopping_rounds=20
        )
    else :
        model = None

    model.fit(x_train, y_train, eval_set=[(x_val, y_val)], verbose=False) # 训练模型
    print(f"早停触发，最佳迭代次数: {model.best_iteration}")

    y_predict = model.predict(x_test) # 用于评估
    eval_model(task_type, y_test, y_predict, le)

    for imp_type in ['weight', 'gain', 'cover']: # 三种重要性
        plot_feature_importance(target_name, model, importance_type=imp_type, top_n=20)
    shap_analysis(target_name, model, x_test,task_type, cut_num = 200) # 计算 SHAP 值
    return model, scaler, num_feats, list(feature.columns)

def save_xgb_model(model_path, model, scaler, num_feats, feature_order):
    model.save_model("./res/models/" + model_path + ".json")  # JSON 格式

    # 增加 feature_order 列表，记录训练时输入给模型的特征列顺序
    # 注意：feature 是在 train_xgboost_model 中预处理后的 DataFrame
    # 你需要在调用 save_xgb_model 时传入 feature 或 feature_order
    # 建议修改 train_xgboost_model 也返回 feature_order
    preprocessor_info = {
        "numeric_columns": num_feats,             # 数值列顺序
        "mean": scaler.mean_.tolist(),
        "std": scaler.scale_.tolist(),
        "feature_order": feature_order            # 全部特征列的顺序，例如 feature.columns.tolist()
    }
    with open("./res/models/" + model_path + '_scaler', 'w') as f:
        json.dump(preprocessor_info, f, indent=2)
