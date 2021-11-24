import redis

class Redis:
    def ___init___(self):
        '''
        '''
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def set_redis(self, key, val):
        '''
        '''
        print(key, val)
        # return self.r.set(key)

    def get_redis(self, key):
        '''
        '''
        ans = self.r.get(key)
        return ans.decode('utf-8')
