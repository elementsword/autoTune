import readTool
import time
import subprocess
from parameter import Parameter
from logger import Logger
# 获取日志实例
logger = Logger().get_logger()
class BaseData:
    def __init__(self):
        # 加载配置文件
        self.config = readTool.load_config("config.yaml")
        # 基线数据 
        self.output_file = "baseline.txt"
        # 门槛 高于多少
        self.improvement = self.config.get('thresholds').get('improvement')
        self.parameter_list = []
        self.baseline_time = None
        self.target = None  
    def getBase(self):
        # 获取内核参数列表
        kernel_params = self.config.get('parameters', [])
        for param in kernel_params:
            try:
                each_parameter = Parameter(
                param.get("name"),
                param.get("type"),
                param.get("min"),
                param.get("max"),
                param.get("steps"),
                param.get("options"),
                param.get("get"),
                param.get("set")
                )
                # 执行 sysctl 读取内核参数
                result = subprocess.run([each_parameter.get], capture_output=True, text=True, check=True, shell=True)
                value = result.stdout.strip()
                if each_parameter.set_Default(value):
                    logger.info(f"参数 {each_parameter.name} 的初始值设置完毕: {value}")
                    self.parameter_list.append(each_parameter)
                else:
                    logger.info(f"参数 {each_parameter.name} 的初始值设置失败: {value}")
                    
            except subprocess.CalledProcessError:
                logger.info(f"无法获取参数: {param}")
        self.target = self.config['target']
        # 记录开始时间
        start_time = time.time()
        # 通过 bash 执行脚本
        result = subprocess.run(['bash', self.target], capture_output=True, text=True)
        # 记录结束时间
        end_time = time.time()
        self.baseline_time = end_time - start_time

        

