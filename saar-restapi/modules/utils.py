import pymongo, os
import requests, json
from datetime import timezone, datetime
from functools import wraps
from flask import request


class MongoC:
    def __init__(self, db_name, col_name):
        self.db_name = db_name
        self.col_name = col_name
        self.client = self.connect()

    def connect(self):
        return pymongo.MongoClient(
            os.environ["MONGO_DB_URL"],
            username="admin",
            password="admin",
            authSource="admin",
        )

    def disconnect(self):
        self.client.close()

    @property
    def ref(self):
        return self.client[self.db_name][self.col_name]

    def create(self, **doc):
        print(**doc)
        return self.ref.insert_one({
            **doc,
            "created": datetime.now(),
            "updated": datetime.now(),
        })

    def update(self, doc_id, doc):
        return self.ref.update_one({ "_id": doc_id }, { **doc, "updated": datetime.now() })

    def delete(self, doc_id):
        return self.ref.delete_one({ "_id": doc_id })

    def find(self):
        return self.col_name.find(self.col_name)


mongoc = MongoC('audit', 'audit')

# def mongo_db():
#     '''
#     init db client
#     '''
#     myclient = pymongo.MongoClient(
#         os.environ["MONGO_DB_URL"],
#         username="admin",
#         password="admin",
#         authSource="admin"
#     )
#     mydb = myclient[os.environ['MONGO_DBNAME']]
#     mycol = mydb[os.environ['MONGO_COL']]
#     return mydb, mycol

def read_logs_from_db(limit):
    '''
    Read logs from mongoDb with any limit
    '''
    docs = []
    mydocs = mongoc.find()
    print(mydocs)
    # mydocs = col.find().sort("timestamp", -1).limit(limit)
    # for doc in mydocs:
    #     docs.append(doc)
    # return json.dumps(docs, default = convert_datetime)

def write_logs_to_db(payload):
    '''
    Write the logs into the mongoDb
    '''
    mongoc.create(payload)
    # _update = { "timestamp": datetime.now(timezone.utc) }
    # payload.update(_update)
    # _id = col.insert_one(payload)
    # return _id.inserted_id

def convert_datetime(o):
    if isinstance(o, datetime):
        return o.__str__()

def write_logs():
    def _write_logs(f):
        @wraps(f)
        def middleware(*args, **kwargs):
            payload = { "operation": request.path, "ip": request.remote_addr }
            # url = "http://127.0.0.1:5002/api/v1/audit"
            url = os.environ['AUDIT_SERVER_URL'] + "/api/v1/audit"
            res = requests.post(url, data = json.dumps(payload) )
            return f(*args, **kwargs)

        return middleware

    return _write_logs