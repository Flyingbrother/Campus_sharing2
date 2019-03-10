from redis import *

class redisHelper():
    def __init__(self, host, port):
        self.__redis = StrictRedis(host, port)

    def set(self, key, value):
        self.__redis.set(key, value)

    def get(self, key):
        return self.__redis.get(key)


# if __name__ == '__main__':
#     re = redisHelper('172.27.0.6', 6379)
#     judge = re.get('py10')
#     print(judge)

    # if judge[0] == 'like':
    #     print(1)
    # else:
    #     print(0)
