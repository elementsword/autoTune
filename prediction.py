import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib

class Prediction:
    def __init__(self):
        self.model = xgb.XGBRegressor(
        objective='reg:squarederror',  # 使用平方误差作为目标函数
        n_estimators=100,             # 树的数量
        learning_rate=0.1,            # 学习率
        max_depth=4,                  # 树的最大深度
        random_state=42
        )
        self.X_train = None  # 初始化训练数据为空

    def is_model_trained(self):
        """
        检查模型是否已训练
        :return: True 如果模型已训练，否则 False
        """
        return self.X_train is not None
    
    def train(self,dataset):

        # 准备数据
        X = np.array([params for params, _ in dataset])  # 特征：参数配置
        y = np.array([result for _, result in dataset])  # 目标值：运行时间

        # 划分训练集和测试集
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 初始化 XGBoost 回归模型

        # 训练模型
        self.model.fit(self.X_train, self.y_train)

        # 预测
        self.y_pred = self.model.predict(self.X_test)

        # 评估模型
        self.mse = mean_squared_error(self.y_test, self.y_pred)
        print(f"均方误差 (MSE): {self.mse}")

        # 可选：打印特征重要性
        print("特征重要性:")
        print(self.model.feature_importances_)
        return self.model.feature_importances_
    
        
    def predict_best(self, candidate_params):
        # 检查模型是否已训练
        if not self.is_model_trained():
            raise ValueError("模型尚未训练，请先调用 train 方法进行训练。")
        """
        使用训练好的模型预测候选参数的目标值，并返回最优参数配置
        :param candidate_params: 候选参数配置列表
        :return: 最优参数配置及其预测值
        """
        predictions = self.model.predict(candidate_params)
        best_index = np.argmin(predictions)  # 找到目标值最小的索引
        best_params = candidate_params[best_index]
        best_value = predictions[best_index]
        return best_params, best_value
    
    def save_model(self, filename="xgboost_model.pkl"):
        # 检查模型是否已训练
        if not self.is_model_trained():
            raise ValueError("模型尚未训练，请先调用 train 方法进行训练。")
        """
        保存训练好的模型到文件
        :param filename: 保存的文件名
        """
        joblib.dump(self.model, filename)
        print(f"模型已保存到 {filename}")

    def load_model(self, filename="xgboost_model.pkl"):
        """
        从文件加载模型
        :param filename: 模型文件名
        """
        self.model = joblib.load(filename)
        print(f"模型已从 {filename} 加载")