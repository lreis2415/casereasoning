class Case:
    # 定义一个抽象的初始化方法，需要子类实现
    def __init__(self):
        raise NotImplementedError("Subclass must implement __init__ method")

    def set_parameter(self, parameter, value):
        # 拼接parameter和"calculate_"前缀，得到方法名
        method_name = "set_" + parameter
        # 使用getattr函数，根据self对象和方法名获取方法对象
        method = getattr(self, method_name, None)
        # 判断方法对象是否存在，如果存在就调用它，否则打印错误信息
        if method is not None:
            return method()
        else:
            print("Invalid parameter name")

    def get_parameter(self, parameter):
        # 拼接parameter和"calculate_"前缀，得到方法名
        method_name = "get_" + parameter
        # 使用getattr函数，根据self对象和方法名获取方法对象
        method = getattr(self, method_name, None)
        # 判断方法对象是否存在，如果存在就调用它，否则打印错误信息
        if method is not None:
            return method()
        else:
            print("Invalid parameter name")

    def calculate_parameter(self, parameter):
        # 拼接parameter和"calculate_"前缀，得到方法名
        method_name = "calculate_" + parameter
        # 使用getattr函数，根据self对象和方法名获取方法对象
        method = getattr(self, method_name, None)
        # 判断方法对象是否存在，如果存在就调用它，否则打印错误信息
        if method is not None:
            return method()
        else:
            print("Invalid parameter name")