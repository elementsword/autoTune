import logging
import os

class Logger:
    _instance = None
    #单例模式 
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, log_file="autoTune.log", level=logging.INFO):
        """
        初始化日志记录器
        :param log_file: 日志文件路径
        :param level: 日志级别
        """
        if not hasattr(self, "logger"): #确保只初始化一次 
            self.logger = logging.getLogger("AutoTuneLogger")
            self.logger.setLevel(level)

            # 创建日志格式
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            # 控制台日志处理器
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # 文件日志处理器
            if log_file:
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger