import time

def timer(func):
    def timed(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        ends = time.time()

        print('{} works in {}'.format(func.__name__, ends - start))
        return res
    return timed
