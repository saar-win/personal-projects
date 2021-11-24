import redis

class Redis_actions:
    def __init__(self, host):
        '''
        '''
        self.host = host
        self.r = redis.Redis(host=self.host, port=6379, db=0)

    def set_redis(self, _id, data):
        '''
        '''
        return self.r.set(_id, data)

    def get_redis(self, key):
        '''
        '''
        val = self.r.get(key)
        return val.decode('utf-8')
