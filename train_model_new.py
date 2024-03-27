
from supervised.automl import AutoML  # 导入 AutoML 类
import pandas as pd  # 导入 pandas 库处理数据
from sklearn.model_selection import train_test_split
import os
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import joblib
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# 配置信息
class Config:
    DATA_FILE = 'data.csv'
    PREDICT_DATA_FILE = 'train/data.csv'
    PREPROCESSED_DATA_DIR = 'train'
    MODEL_DIR = 'train/models'
    FEATURE_NAMES = [
        'qixue', 'zhenqi', 'low_gongji', 'up_gongji', 'defense', 'baoshang', 'duiguai',
        '1%_qixue', '1%_zhenqi', '1%_gongji', '1%_fangyu', 'zishen_defense'
    ]
    PROFESSION_OPTIONS = [0,1,2,3,4]#["逐霜", "鬼王", "太昊", "惊岚", "涅羽"]

# 数据处理函数
def load_data(path):
    try:
        data = pd.read_csv(path, encoding='utf-8')
        return data
    except FileNotFoundError:
        print(f"Error: 文件 '{path}' 未找到。")
        return None
    except Exception as e:
        print(f"Error: 读取文件时发生异常：{e}")
        return None

def preprocess_data(data):
    # 剔除重复数据
    data.drop_duplicates(inplace=True)    

    data.to_csv(os.path.join(Config.PREPROCESSED_DATA_DIR, 'data.csv'), index=False, encoding='utf-8')
    return data

# 模型训练函数
def train_model(prof_idx, data):
    # 检查职业索引是否在数据中存在
    if prof_idx not in data['zhiye'].unique():
        print(f"No data found for profession index {prof_idx}.")
        return None
        
    # 筛选出特定职业的数据
    data_for_profession = data[data['zhiye'] == prof_idx]

    # 检查当前职业下的样本个数是否大于5,
    if len(data_for_profession) < 5:
        print(f"Error: 对于职业 {prof_idx}，数据集的样本数小于5，无法进行训练。")
        return None

    # 需要对数据进行预处理
    data_for_profession.loc[data_for_profession['zhiye'] != 1, ['defense', '1%_fangyu', 'zishen_defense']] = 0    

    # 保存预处理后的数据
    data_for_profession.to_csv(f'./train/{prof_idx}_preprocessed_data.csv', index=False, encoding='utf-8')
    '''
    # 观察数据的基本信息
    print(data_for_profession.head())  # 打印数据的前几行
    print(data_for_profession.info())  # 打印数据的基本信息，包括每列的数据类型和非空值数量
    print(data_for_profession.describe())  # 打印数据的描述性统计信息，包括均值、标准差、最小值、最大值等
    '''
    # 提取特征和标签
    X = data_for_profession.drop(columns=['zhiye', 'up_damage'])  # 特征
    y = data_for_profession['up_damage']
    
    '''
    # 打印特征和目标变量的形状
    print("特征形状:", X.shape)
    print("目标变量形状:", y.shape)
    '''

    '''
    plt.figure(figsize=(12, 6))

    # 绘制特征的直方图
    for i, feature in enumerate(X.columns):
        plt.subplot(3, 4, i + 1)
        sns.histplot(X[feature], kde=True)
        plt.title(feature)

    plt.tight_layout()
    plt.show()

    # 绘制目标变量的直方图
    plt.figure(figsize=(8, 6))
    sns.histplot(y, kde=True, color='red')
    plt.title('up_damage Distribution')
    plt.xlabel('up_damage')
    plt.ylabel('Frequency')
    plt.show()
    '''

    # 计算特征与目标变量的相关系数
    data_corr = data_for_profession.drop(columns=['zhiye']) 
    correlation_matrix = data_corr.corr()
    print("\n特征与目标变量的相关系数:")
    print(correlation_matrix['up_damage'])

    # 绘制特征与目标变量的散点图
    plt.figure(figsize=(12, 6))

    for i, feature in enumerate(X.columns):
        plt.subplot(3, 4, i + 1)
        sns.scatterplot(x=X[feature], y=y)
        plt.title(f'{feature} vs up_damage')

    plt.tight_layout()
    plt.show()

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    '''
    # 打印训练集和测试集的形状
    print("训练集特征形状:", X_train.shape)
    print("训练集目标变量形状:", y_train.shape)
    print("测试集特征形状:", X_test.shape)
    print("测试集目标变量形状:", y_test.shape)
    '''

    '''
    # 训练模型
    automl = AutoML(results_path=f'AutoML_{prof_idx}')
    automl.fit(X_train, y_train)

    # 获取预测值
    y_pred = automl.predict(X_test)
    '''

    model = GradientBoostingRegressor(random_state=42)
    param_grid = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 4, 5]
    }

    # 使用网格搜索调优参数
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error', verbose=2)
    grid_search.fit(X_train, y_train)

    # 输出最佳参数
    print("最佳参数:", grid_search.best_params_)

    # 训练模型
    best_model = grid_search.best_estimator_
    best_model.fit(X_train, y_train)

    # 获取预测值
    y_pred = best_model.predict(X_test)

    # 获取特征重要性并绘图
    feature_importance = best_model.feature_importances_
    plot_feature_importance(prof_idx, feature_importance, Config.FEATURE_NAMES)

    # 保存模型
    save_model(best_model, prof_idx)

    # 计算均方误差（MSE）
    mse = mean_squared_error(y_test, y_pred)
    print(f"职业 {prof_idx} 的均方误差 (MSE): {mse}")


def plot_feature_importance(prof_idx, importances, feature_names):
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(importances)), importances, align='center')
    plt.yticks(range(len(importances)), feature_names)
    plt.xlabel(f'{prof_idx} Feature Importance')
    plt.ylabel('Feature')
    plt.title(f'{prof_idx} Feature Importance Plot')

def save_model(model, prof_idx):
    model_dir = Config.MODEL_DIR
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    model_file = os.path.join(model_dir, f'{prof_idx}_best_model.pkl')
    joblib.dump(model, model_file)

def model_single_predict(prof_idx, data):
    '''
    model_file = f'./train/models/{prof_idx}_best_model.pkl'
    if not os.path.exists(model_file):
        print(f"Model file '{model_file}' not found.")
        return None
        
    # 加载模型
    loaded_model = joblib.load(model_file)    
    
    # 使用训练好的模型进行预测
    predicted_label = loaded_model.predict(data)
    '''

    automl = AutoML(results_path=f'AutoML_{prof_idx}')
    predicted_label = automl.predict(data)
    return predicted_label

def predict_compare():
    data = load_data(Config.PREDICT_DATA_FILE)
    if data is None:
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

    # 绘图
    plt.show()

# 主函数
def main():
    # 读取csv文件
    data = load_data(Config.DATA_FILE)
    if data is None:
        return

    # 预处理数据
    data = preprocess_data(data)

    # 训练配置中所有职业（可能data中没有某些职业）
    for prof_idx in Config.PROFESSION_OPTIONS:
        print("=======now train the prof", prof_idx)
        train_model(prof_idx, data)

    # 使用原始数据进行预测，并比较预测值和实际值
    predict_compare()

# 运行主函数
if __name__ == "__main__":
    main()
