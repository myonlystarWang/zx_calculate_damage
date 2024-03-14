# train_model.py
# 导入必要的库
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import joblib
import pandas as pd
import shap
import matplotlib.pyplot as plt
import seaborn as sns


feature_names = [
    'qixue', 
    'zhenqi', 
    'low_gongji', 
    'up_gongji', 
    'defense', 
    'baoshang', 
    'duiguai', 
    '1%_qixue', 
    '1%_zhenqi', 
    '1%_gongji', 
    '1%_fangyu', 
    'zishen_defense'
]

# 主输出选项
prof_options = ["逐霜", "鬼王", "太昊", "惊岚", "涅羽"]

def train_gradient_boosting_model(prof_idx, data):
    # 筛选出特定职业的数据
    data_for_profession = data[data['zhiye'] == prof_idx]

    # 提取特征和标签
    X = data_for_profession.drop(columns=['zhiye', 'up_damage'])  # 特征
    y = data_for_profession['up_damage']  # 目标标签

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 初始化梯度提升树回归模型
    model = GradientBoostingRegressor(random_state=42)

    # 定义参数网格
    param_grid = {
        'n_estimators': [50, 100, 200],  # 树的数量
        'learning_rate': [0.01, 0.1, 0.2],  # 学习率
        'max_depth': [3, 4, 5]  # 树的最大深度
    }

    # 使用网格搜索调优参数
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error', verbose=2)
    grid_search.fit(X_train, y_train)

    # 输出最佳参数
    print("最佳参数:", grid_search.best_params_)

    # 使用最佳参数初始化模型
    best_model = grid_search.best_estimator_

    # 训练模型
    best_model.fit(X_train, y_train)

    # 获取特征重要性
    feature_importance = best_model.feature_importances_
    print("特征重要性:", feature_importance)

    # 创建特征重要性条形图
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(feature_importance)), feature_importance, align='center')
    plt.yticks(range(len(feature_importance)), feature_names)
    plt.xlabel('Feature Importance')
    plt.ylabel('Feature')
    plt.title(f'{prof_idx} Feature Importance Plot')
    #plt.show()

    # 初始化 SHAP 解释器
    explainer = shap.TreeExplainer(best_model)

    # 获取特征的 SHAP 值
    shap_values = explainer.shap_values(X_test)
    print("局部特征贡献值一:", shap_values)

    # 创建热力图一
    plt.figure(figsize=(10, 6))
    sns.heatmap(shap_values.T, cmap='coolwarm', annot=True, fmt=".2f", linewidths=.5, xticklabels=feature_names)
    plt.title(f'{prof_idx} Local Feature Contributions Heatmap')
    plt.xlabel('Features')
    plt.ylabel('Samples')
    #plt.show()

    # 预测
    y_pred = best_model.predict(X_test)
    print("y_pred", y_pred)

    # 计算均方误差（MSE）
    mse = mean_squared_error(y_test, y_pred)
    print("均方误差 (MSE):", mse)

    # 保存模型
    joblib.dump(best_model, f'{prof_idx}_best_model.pkl')

# 主训练函数
def train_models():
    try:
        # 加载数据
        data = pd.read_csv('data.csv', encoding='utf-8')
    except FileNotFoundError:
        print("Error: 文件 'data.csv' 未找到！请确保文件存在并且位于正确的路径下。")
        return
    except Exception as e:
        print(f"Error: 读取文件时发生异常：{e}")
        return
    
    # 剔除重复数据
    data.drop_duplicates(inplace=True)    

    # 反写CSV文件
    data.to_csv('data.csv', index=False, encoding='utf-8')

    # 根据不同的职业训练模型
    professions = data['zhiye'].unique()
    trained_models = {}
    for prof_idx in professions:
        trained_model = train_gradient_boosting_model(prof_idx, data)
        trained_models[prof_idx] = trained_model

    #return trained_models

def model_single_predict(prof_idx, data):
    # 加载模型
    loaded_model = joblib.load(f'{prof_idx}_best_model.pkl')    
    
    # 使用训练好的模型进行预测
    predicted_label = loaded_model.predict(data)
    return predicted_label

def model_predict():
    try:
        # 加载数据
        data = pd.read_csv('data.csv', encoding='utf-8')
    except FileNotFoundError:
        print("Error: 文件 'data.csv' 未找到！请确保文件存在并且位于正确的路径下。")
        return
    except Exception as e:
        print(f"Error: 读取文件时发生异常：{e}")
        return

    # 保存实际值
    y = data['up_damage']  

    # 删除结果列
    X = data.drop(columns=['up_damage'])  

    # 遍历每一条数据
    predictions = {}
    for index, row in X.iterrows():
        prof_idx = int(row['zhiye'])
        row_df = pd.DataFrame([row])

        # 删除 'zhiye' 列
        row_df.drop(columns=['zhiye'], inplace=True)        
        predict_label = model_single_predict(prof_idx, row_df)

        # 检查 predictions 字典中是否已经有该职业的键，若没有，则创建一个空列表
        if prof_idx not in predictions:
            predictions[prof_idx] = []        
        predictions[prof_idx].append(predict_label)  # 使用append方法添加预测值

    for prof_idx,prediction in predictions.items():
        # 获取当前职业的实际值
        actual_values = y[data['zhiye'] == prof_idx]        

        # 创建散点图
        plt.figure(figsize=(8, 6))
        plt.scatter(actual_values, prediction, color='blue', alpha=0.5, label='Predicted Damage')  # 预测伤害为蓝色
        plt.scatter(actual_values, actual_values, color='red', alpha=0.5, label='Real Damage')  # 实际伤害为红色
        plt.title(f'{prof_idx} predict_damage vs real_damage')
        plt.xlabel('Real Damage', color='red')  # 设置实际伤害的x轴标签颜色为红色
        plt.ylabel('Predicted Damage', color='blue')  # 设置预测伤害的y轴标签颜色为蓝色    
        plt.grid(True)

    #return predictions
    plt.show()


train_models()
model_predict()
