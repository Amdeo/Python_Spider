import time

class caluCodeTime():
    def __init__(self):
        self.__start()

    def __start(self):
        self.startTime = time.perf_counter()

    def end(self):
        self.endTime = time.perf_counter()
        print("time is {}".format(self.endTime - self.startTime))

if __name__ == '__main__':
    time1 = caluCodeTime()
    a = 1
    for value in range(100000000):
        a = a + 1
    time1.end()
