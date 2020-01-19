import os
import redis
from rq import Connection, Worker
from flask import Flask

app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static",
    )

# set config
app_settings = os.getenv("APP_SETTINGS")
app.config.from_object(app_settings)
redis_url = app.config["REDIS_URL"]

#start the worker
redis_connection = redis.from_url(redis_url)
with Connection(redis_connection):
    worker = Worker(app.config["QUEUES"])
    worker.work()

#redis_conn = Redis()
#with Connection(redis_conn):
#    worker = Worker(["default"])
#    worker.work()
