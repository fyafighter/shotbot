from redis import Redis
from rq import Connection, Worker
 
redis_conn = Redis()
with Connection(redis_conn):
    worker = Worker(["default"])
    worker.work()
