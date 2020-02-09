import threading
import threadpool


class myclass:
    def __init__(self):
        self.a = 1
        self.b = 2

    def run(self):
        g = [1,2,3,4,5]
        func_args = [([self,i],None) for i in g]
        pool = threadpool.ThreadPool(10)
        requests = threadpool.makeRequests(myclass.thread_func,func_args)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    def thread_func(self,m):
        print(m)



if __name__ == "__main__":
    d = myclass()
    d.run()
