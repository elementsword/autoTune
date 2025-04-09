import readTool
import subprocess
import time
from basedata import BaseData
from logger import Logger
# 获取日志实例
logger = Logger().get_logger()
class Filter:
    def __init__(self,base):
        # 存储满足条件的参数
        self.base = base
        self.significant_params = []
        # 输出文件
        self.output_file = "param_effects.txt"
        
    def filter(self):
        # 遍历参数列表
        with open(self.output_file, "w") as f:
            for each_parameter in self.base.parameter_list:
                if not each_parameter.name or not each_parameter.set or not each_parameter.get:
                    logger.info(f"参数 {each_parameter.name} 配置不完整，跳过")
                    continue

                # 如果参数是范围设置，跳过
                if each_parameter.is_range():
                    logger.info(f"参数 {each_parameter.name} 是范围设置，跳过监测,直接加入。")
                    self.significant_params.append(each_parameter)
                    continue

                logger.info(f"开始测试参数 {each_parameter.name}，当前值: {each_parameter.default}")

                # 遍历 options 中的每个值
                for option in each_parameter.options:
                    if str(option) == each_parameter.default:
                        logger.info(f"参数 {each_parameter.name} 的值已是 {option}，跳过")
                        continue
                    # 修改参数值
                    try:
                        subprocess.run(each_parameter.set.format(option), shell=True, check=True)
                        logger.info(f"已将参数 {each_parameter.name} 修改为 {option}")
                    except subprocess.CalledProcessError as e:
                        logger.info(f"无法设置参数 {each_parameter.name} 的值为 {option}: {e}")
                        continue

                    # 记录开始时间
                    start_time = time.time()

                    # 执行性能测试脚本
                    try:
                        result = subprocess.run(['bash', self.base.target], capture_output=True, text=True, check=True)
                    except subprocess.CalledProcessError as e:
                        logger.info(f"性能测试失败: {e}")
                        continue
                    # 记录结束时间
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    # 恢复参数值
                    try:
                        subprocess.run(each_parameter.set.format(option), shell=True, check=True)
                        logger.info(f"已将参数 {each_parameter.name} 恢复为原始值 {each_parameter.default}")
                    except subprocess.CalledProcessError as e:
                        logger.info(f"无法恢复参数 {each_parameter.name} 的值为 {each_parameter.default}: {e}")
                        continue
                    # 计算百分比差值
                    percentage_diff = abs((elapsed_time - self.base.baseline_time) / self.base.baseline_time) * 100

                    # 写入结果（仅当百分比差值大于阈值时）
                    status = "提升" if elapsed_time < self.base.baseline_time else "劣化"
                    f.write(f"参数: {each_parameter.name}, 修改值: {option}, 耗时: {elapsed_time:.2f} 秒, 百分比差值: {percentage_diff:.2f}%, {status}\n")
                    logger.info(f"记录完成: 参数 {each_parameter.name}, 修改值 {option}, 耗时 {elapsed_time:.2f} 秒, 百分比差值: {percentage_diff:.2f}%, {status}")
                    if percentage_diff > self.base.improvement and each_parameter not in self.significant_params:
                        self.significant_params.append(each_parameter)
        logger.info(f"所有参数测试完成，结果已保存至 {self.output_file}")
