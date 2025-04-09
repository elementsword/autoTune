class Parameter:
    """
    参数类，用于表示和操作单个参数的属性。
    """

    def __init__(self, name=None, param_type=None, min_val=None, max_val=None, steps=None, options=None,get=None,set=None):
        """
        初始化参数对象
        :param name: 参数名称
        :param param_type: 参数类型 ("range" 或 "options")
        :param min_val: 最小值（适用于 range 类型）
        :param max_val: 最大值（适用于 range 类型）
        :param steps: 步长（适用于 range 类型）
        :param options: 可选值列表（适用于 options 类型）
        :param default: 默认值
        :param get: 
        :param set: 
        """
        self.name = name
        self.param_type = param_type
        self.min_val = min_val
        self.max_val = max_val
        self.steps = steps
        self.options = options or []
        self.get = get
        self.set = set

    def is_range(self):
        """判断参数是否为范围类型"""
        return self.param_type == "range"

    def is_options(self):
        """判断参数是否为选项类型"""
        return self.param_type == "options"

    def get_range(self):
        """获取范围类型参数的范围"""
        if self.is_range():
            return (self.min_val, self.max_val, self.steps)
        return None

    def get_options(self):
        """获取选项类型参数的选项列表"""
        if self.is_options():
            return self.options
        return None
    
    def get_Get_Command(self):
        """获取选项类型参数的选项列表"""
        return self.get
    
    def get_Set_Command(self):
        """获取选项类型参数的选项列表"""
        return self.set
    
    def set_Default(self, default):
        """
        设置参数的默认值
        :param default: 要设置的默认值
        """
        self.default = default
        return True
        
    
    def __repr__(self):
        """返回参数对象的字符串表示"""
        if self.is_range():
            return f"Parameter(name={self.name}, type=range, range=({self.min_val}, {self.max_val}, steps={self.steps}), default={self.default},get={self.get},set={self.set})"
        elif self.is_options():
            return f"Parameter(name={self.name}, type=options, options={self.options}, default={self.default},get={self.get},set={self.set})"
        else:
            return f"Parameter(name={self.name}, type=unknown, default={self.default},get={self.get},set={self.set})"