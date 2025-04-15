import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib
from logger import Logger
# 获取日志实例
logger = Logger().get_logger()
class Prediction:
    def __init__(self):

        self.model = None  # 初始化训练数据为空

    def is_model_trained(self):
        """
        检查模型是否已训练
        :return: True 如果模型已训练，否则 False
        """
        return self.model is not None
    
    def train(self,dataset):
        self.model = xgb.XGBRegressor(
        objective='reg:squarederror',  # 使用平方误差作为目标函数
        n_estimators=100,             # 树的数量
        learning_rate=0.3,            # 学习率
        max_depth=4,                  # 树的最大深度
        random_state=42
        )
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
        
    def get_feature_importances(self):
        # 检查模型是否已训练
        if not self.is_model_trained():
            logger.error("模型尚未训练，请先调用 train 方法进行训练。")
            raise ValueError("模型尚未训练，请先调用 train 方法进行训练。")
        return self.model.feature_importances_

    def predict_best(self, candidate_params):
        """
        遍历候选参数组合，找到预测目标值最小的参数组合
        :param candidate_params: 所有候选参数组合（一维列表，每个元素是一个元组）
        :return: 最优参数组合及其预测值
        """
        # 检查模型是否已训练
        if not self.is_model_trained():
            logger.error("模型尚未训练，请先调用 train 方法进行训练。")
            raise ValueError("模型尚未训练，请先调用 train 方法进行训练。")

        best_params = None
        best_value = float('inf')

        for params in candidate_params:
            # 将参数组合转换为二维数组
            params = np.array(params).reshape(1, -1)
            prediction = self.predict(params)
            if prediction < best_value:
                best_value = prediction
                best_params = params

        logger.info(f"最优参数组合: {best_params.flatten()}, 预测值: {best_value}")
        return best_params.flatten(), best_value
    def predict(self, params):
        """
        使用训练好的模型预测单组参数的目标值
        :param params: 单组参数（一维数组）
        :return: 预测目标值
        """
        # 检查模型是否已训练
        if not self.is_model_trained():
            logger.error("模型尚未训练，请先调用 train 方法进行训练。")
            raise ValueError("模型尚未训练，请先调用 train 方法进行训练。")
        if params.shape[1] != self.model.n_features_in_:
            raise ValueError(f"每组参数的维度必须为 {self.model.n_features_in_}。")
        # 预测目标值
        prediction = self.model.predict(params)
        return prediction[0]
    
    def save_model(self, filename="xgboost_model.pkl"):
        # 检查模型是否已训练
        if not self.is_model_trained():
            logger.error("模型尚未训练，请先调用 train 方法进行训练。")
            raise ValueError("模型尚未训练，请先调用 train 方法进行训练。")
        """
        保存训练好的模型到文件
        :param filename: 保存的文件名
        """
        joblib.dump(self.model, filename)
        logger.info(f"模型已保存到 {filename}")

    def load_model(self, filename="xgboost_model.pkl"):
        """
        从文件加载模型
        :param filename: 模型文件名
        """
        self.model = joblib.load(filename)
        logger.info(f"模型已从 {filename} 加载")