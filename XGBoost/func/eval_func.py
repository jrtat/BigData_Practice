import os
import shap
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, classification_report,
                             mean_absolute_error, mean_squared_error, r2_score)

def eval_model(task_type, y_test, y_predict, le):
    if task_type == 'regression':
        mae = mean_absolute_error(y_test, y_predict) # 计算 mae
        rmse = np.sqrt(mean_squared_error(y_test, y_predict)) # 计算 rmse
        r2 = r2_score(y_test, y_predict) # 计算 r2
        print(f"回归评测结果：")
        print(f"  MAE : {mae:.4f}")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  R²  : {r2:.4f}")
    else:
        acc = accuracy_score(y_test, y_predict) # 计算 accuracy
        print(f"分类准确率: {acc:.4f}")
        if le is not None:
            target_names = [str(cls) for cls in le.classes_]
        else:
            target_names = None
        print("\n分类报告：")
        print(classification_report(y_test, y_predict, target_names=target_names))

def plot_feature_importance(model_name, model, importance_type, top_n=20):
    """
    weight 	该特征在所有树中被用作分裂节点的次数	                         出现频率（用了多少次（频繁度））
    gain	使用该特征作为分裂点时平均的损失减少量（例如信息增益、Gini 增益等）   平均增益（有多大提升（效果））
    cover	该特征分裂时平均覆盖的样本数（基于二阶梯度，大致反映样本量）	         平均影响范围（影响了多少样本（覆盖面））
    """
    booster = model.get_booster()
    # 通过 scikit-learn 包装器获取底层的 xgboost.Booster 对象，该对象提供 get_score 方法用于导出重要性

    importance_dict = booster.get_score(importance_type=importance_type)
    # 调用 get_score 获取特征重要性字典

    imp_df = pd.DataFrame(
        [(k, v) for k, v in importance_dict.items()],
        columns=['feature', 'importance']
    ).sort_values('importance', ascending=False)
    # 生成 DataFrame，键（特征名）通过 safe_name 映射，然后按重要性降序排列

    out_df = imp_df.head(top_n) # 保存 top_n 行到 JSON
    filename = f"{model_name}_{importance_type}.json"
    path = os.path.join("./res/evals/", filename)
    out_df.to_json(path, orient='records', force_ascii=False)
    print(f"Saved feature importance to {path}")

def shap_analysis(model_name, model, x_test, task_type, cut_num = 200):

    feature_names = x_test.columns.tolist()
    explainer = shap.Explainer(model)
    shap_values = explainer(x_test[:cut_num])

    x_sample = x_test[:cut_num]
    n_features = len(feature_names)

    shap_array = shap_values.values
    base_array = shap_values.base_values
    x_vals = x_sample[feature_names].values

    # ---------- 多分类 ----------
    if task_type == 'classification' and len(shap_array.shape) == 3:
        n_classes = shap_array.shape[2]

        sample_idx = np.repeat(np.arange(cut_num), n_features * n_classes)
        feature_idx = np.tile(np.repeat(np.arange(n_features), n_classes), cut_num)
        class_idx = np.tile(np.arange(n_classes), cut_num * n_features)

        feature_names_arr = np.array(feature_names)
        feature_col = feature_names_arr[feature_idx]

        feature_values = np.repeat(x_vals.flatten(), n_classes)

        shap_flat = shap_array.flatten()

        if base_array.ndim == 2:
            base_rep = base_array[sample_idx, class_idx]
        elif base_array.ndim == 1:
            base_expanded = np.tile(base_array[:, np.newaxis], (1, n_classes))
            base_rep = base_expanded[sample_idx, class_idx]
        elif np.isscalar(base_array) or base_array.ndim == 0:
            base_rep = np.full(cut_num * n_features * n_classes, base_array)
        else:
            base_rep = np.repeat(base_array.flatten(), n_features * n_classes)

        df_shap = pd.DataFrame({
            'sample': sample_idx,
            'class': class_idx,
            'feature': feature_col,
            'shap_value': shap_flat,
            'feature_value': feature_values,
            'base_value': base_rep
        })

    # ---------- 回归 / 二分类 ----------
    else:
        sample_idx = np.repeat(np.arange(cut_num), n_features)
        feature_idx = np.tile(np.arange(n_features), cut_num)
        feature_col = np.array(feature_names)[feature_idx]

        feature_values = x_vals.flatten()
        shap_flat = shap_array.flatten()

        if np.isscalar(base_array) or base_array.ndim == 0:
            base_rep = np.full(cut_num * n_features, base_array)
        elif base_array.ndim == 2 and base_array.shape[1] == 2:
            base_rep = np.repeat(base_array[:, 1], n_features)
        else:
            base_rep = np.repeat(base_array, n_features)

        df_shap = pd.DataFrame({
            'sample': sample_idx,
            'feature': feature_col,
            'shap_value': shap_flat,
            'feature_value': feature_values,
            'base_value': base_rep
        })

    # 判断每个特征的所有 shap_value 是否都为 0（精确零）
    zero_mask = df_shap.groupby('feature')['shap_value'].apply(
        lambda s: (s == 0).all()
    )
    zero_features = zero_mask[zero_mask].index.tolist()

    if zero_features:
        df_shap = df_shap[~df_shap['feature'].isin(zero_features)]

    filename = f"{model_name}_shap.json"
    path = os.path.join("./res/evals/", filename)
    df_shap.to_json(path, orient='records', force_ascii=False)
    print(f"Saved SHAP data to {path}")