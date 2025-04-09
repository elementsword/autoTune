from basedata import BaseData
from param_filter import Filter
from dataset_generator import DatasetGenerator
from prediction import Prediction
from logger import Logger
import numpy as np
def printImportance(significant_params, importances):
    # 将参数和重要性打包并排序
    sorted_params = sorted(zip(significant_params, importances), key=lambda x: x[1], reverse=True)
    print("特征重要性排序:")
    for each_parameter, importance in sorted_params:
        importance_percentage = f"{importance * 100:.2f}%"
        print(f"{each_parameter.name} : {importance_percentage}")
        
def main():
    # 初始化日志
    logger = Logger(log_file="autoTune.log").get_logger()
    print("请选择操作：")
    print("1. 从头开始调优")
    print("2. 加载模型并进行预测")
    choice = input("请输入选项 (1 或 2): ")

    if choice == "1":
        # 从头开始调优
        print("开始从头调优...")
        # 执行基线数据获取
        base = BaseData()
        base.getBase()

        # 执行参数过滤
        filter = Filter(base)
        filter.filter()

        # 生成数据集
        generator = DatasetGenerator(filter)
        dataset = generator.run_optimization()
        generator.store()
        generator.get_best_from_dataset()
        # 训练模型
        prediction = Prediction()
        prediction.train(dataset)
        
        feature_importances = prediction.get_feature_importances()
        # 打印特征重要性
        printImportance(filter.significant_params, feature_importances)

        # 保存模型
        prediction.save_model()

    elif choice == "2":
        # 加载模型并进行预测
        print("加载模型...")
        prediction = Prediction()
        prediction.load_model()
        while True:
            # 输入参数进行预测
            print("请输入参数进行预测（以逗号分隔，例如：10,0.5,128）：")
            try:
                input_params = input("参数: ")
                input_params = np.array([
                    float(value) if value.replace('.', '', 1).isdigit() else value #如果是float 
                    for value in input_params.split(",")
                ])
                #预测需要的必须是二维数组 
                input_params = input_params.reshape(1, -1)
                break
            except UnicodeDecodeError:
                print("输入的参数包含无法解码的字符，请检查输入的格式和编码！")
                # 或者提供默认值或者重新输入的逻辑
                # 进行预测
        predictions = prediction.predict(input_params)
        logger.info(f"预测结果: {predictions}")

    else:
        print("无效的选项，请重新运行程序并选择 1 或 2。")

if __name__ == "__main__":
    main()