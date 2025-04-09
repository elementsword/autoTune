import time
import csv
import numpy as np
from skopt import Optimizer
from skopt.space import Real, Integer, Categorical
import subprocess
from logger import Logger
# 获取日志实例
logger = Logger().get_logger()
class DatasetGenerator:
    def __init__(self,filter):
        """
        根据 significant_params 动态生成搜索空间
        :param significant_params: Filter 类中的 significant_params 列表
        :return: 搜索空间列表
        """
        self.best_params = None
        self.best_value = float('inf')
        self.filter =filter
        self.space = []
        print(filter.significant_params)
        for param in filter.significant_params:
            if param.param_type == "range":
                # 如果是范围类型，使用步长生成候选值
                if isinstance(param.min_val, int) and isinstance(param.max_val, int):
                    # 整数范围
                    values = list(range(param.min_val, param.max_val + 1, param.steps))
                    self.space.append(Categorical(values, name=param.name))
                else:
                    # 实数范围
                    values = list(np.arange(param.min_val, param.max_val + param.steps, param.steps))
                    self.space.append(Categorical(values, name=param.name))
            elif param.param_type == "options":
                # 如果是选项类型，使用 Categorical
                self.space.append(Categorical(param.options, name=param.name))
                
    def set_kernel_params(self,values):
        for each_parameter,value in zip(self.filter.significant_params, values):
            command = each_parameter.set.format(value)
            subprocess.run(command, shell=True, check=True)
            
    def exec(self):
        """
        模拟程序运行，返回运行时间。
        """
        start_time = time.time()
        subprocess.run(['bash', self.filter.base.target], capture_output=True, text=True)
        end_time = time.time()
        return end_time - start_time

    def objective(self,values):
        """
        目标函数：运行程序，并以运行时间作为优化目标。
        """
        self.set_kernel_params(values)
        return self.exec()  # 目标是最小化运行时间

    def run_optimization(self,n_iterations=20):
        """
        运行贝叶斯优化，并返回优化数据集。
        """
        optimizer = Optimizer(dimensions=self.space, random_state=42)
        self.data = []
    
        for _ in range(n_iterations):
            next_params = optimizer.ask()
            result = self.objective(next_params)
            optimizer.tell(next_params, result)
            self.data.append((next_params, result))
            if result < self.best_value:
                self.best_value = result
                self.best_params = next_params
        return self.data

    def store(self, filename="dataset.csv"):
        """
        将优化数据集存储为 CSV 文件
        :param filename: 存储文件名
        """
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # 写入表头
            header = [param.name for param in self.filter.significant_params] + ["result"]
            writer.writerow(header)

            # 写入数据
            for params, result in self.data:
                writer.writerow(params + [result])

        logger.info(f"数据集已保存到 {filename}")

    def get_best_from_dataset(self):
        logger.info(f"最优值: {self.best_value}")
        best_params_info = ", ".join(
            [f"{param.name}: {value}" for param, value in zip(self.filter.significant_params, self.best_params)]
        )
        logger.info(f"最优参数: {best_params_info}")
