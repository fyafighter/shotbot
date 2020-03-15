import os, time
import redis
from rq import Connection, Worker, Queue
from flask import Flask
from bot import Bot
bot = Bot("main_bot")
r = bot.get_relays()
#r['up'].switchOff()
#r['down'].switchOff()
#bot.manual_move("up", 10)
#time.sleep(11)
#bot.manual_move("down", 10)

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
    q = Queue()
    q.empty()
    worker = Worker(app.config["QUEUES"])
    worker.work()
