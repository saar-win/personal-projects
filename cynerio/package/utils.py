import redis, json

class Redis_actions:
    def __init__(self, host):
        '''
        '''
        self.host = host
        self.r = redis.Redis(host=self.host, port=6379, db=0)

    def set(self, req):
        '''
        '''
        obj = json.loads(req)
        return self.r.set(obj["id"], obj["data"], ex=60)

    def get(self, key):
        '''
        '''
        val = self.r.get(key)
        if val is not None:
            return val.decode("utf-8")
        else:
            return None

    def delete(self, key):
        '''
        '''
        if self.get(key) != None:
            val = self.r.delete(key)
        else:
            val = None
        return val
