import yaml
import os

def load_config(file_path = "config.yaml"):
    """读取 YAML 配置文件，并返回字典格式的数据"""
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"配置文件 {file_path} 未找到。")
        return None
    except yaml.YAMLError as exc:
        print("解析 YAML 文件时出错：", exc)
        return None

