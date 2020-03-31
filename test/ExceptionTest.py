class A:
    def __init__(self):
        print("构造函数")

    def func(self):
        raise Exception("测试信息")

    def del1(self):
        print("删除实例")
        del self

    def __del__(self):
        print("析构函数")
