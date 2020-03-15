from flask import Flask, jsonify, request
from bot import Bot
import os, json, threading, time, random

bot = Bot("main_bot")
bot_target_queue = {}
app = Flask(__name__)
app_settings = os.getenv("APP_SETTINGS")
app.config.from_object(app_settings)

@app.route('/')
def index():
  return 'Shotbot is online.'

@app.route('/command', methods=['POST'])
def command():
  command_param = request.args.get("switch")
  print(command_param)
  if (command_param in bot.get_relays()):
    bot.enqueue_manual_move(command_param)
    return ("[]")
  else:
    if (command_param=='bouncers'): grounder_shots()
    elif (command_param=='edges'): edge_shots()
    elif (command_param=='random'): random_shots()
    elif (command_param=='level') :bot.level() 
    else: bot.all_stop()
    return("Running "+ command_param)

@app.route('/target', methods=['PUT', 'GET'])
def target():
    if (request.method=='GET'):
        return jsonify(target=bot.get_target())
    elif(request.method=='PUT'):
        bot.set_target(request.json['target'][0], request.json['target'][1])
    return jsonify(target=bot.get_target())

@app.route('/stop', methods=['PUT'])
def stop():
    if(request.method=='PUT'):
        bot.all_stop()
    return jsonify(target=bot.get_target())

@app.route('/relay', methods=['PUT'])
def relay():
    if(request.method=='PUT'):
        bot.manual_move(request.json['relay'], request.json['timeout'])
    return jsonify(target=bot.get_target())

@app.route('/level', methods=['PUT'])
def level():
    if(request.method=='PUT'):
        bot.level()
    return jsonify(target=bot.get_target())

@app.route('/shotmode', methods=['PUT'])
def shotmode():
    if (request.method=='GET'):
        if request.json['target'].mode == 'edges':
            print("Running edges mode")
        elif request.json['target'].mode == 'bouncers':
            print("Running bouncers mode")
        elif request.json['target'].mode == 'random':
            print("Running random mode")

@app.route('/status', methods=['GET', 'PUT'])
def status():
    if (request.method=='GET'):
        return jsonify(status="online", relays=bot.get)

@app.route('/control', methods=['GET', 'PUT'])
def control():
    if (request.method=='PUT'):
        request.json['relay']
        return jsonify(status="online")

def grounder_shots():
    print("GROUNDERS!")
    bot.enqueue_manual_move("pitch")
    for x in range(30):
        print(str(x%3))
        target = x%3 + 1
        bot.set_target(target, 1)

def edge_shots():
    print("GRID")
    bot.enqueue_manual_move("pitch")
    for x in range(10):
        #print(str(x%3))
        target = x % 3 + 1
        #print("Moving to " + str(target) + ", 1")
        #print("Moving to " + str(target) + ", 2")
        #print("Moving to " + str(target) + ", 3")
        bot.set_target(target, 1)
        bot.set_target(target, 2)
        bot.set_target(target, 3)
        bot.set_target(1,2)
        time.sleep(0.1)

def random_shots():
    print("RANDOM!")
    bot.enqueue_manual_move("pitch")
    bot.set_target(1,1)
    for x in range(30):
        r = random.randint(1,3)
        r2 = random.randint(1,3)
        print("Moving to " + str(r) + ", " + str(r2))
        bot.set_target(r, r2)

if __name__ == '__main__':
    bot = Bot("main_bot")
    app.run(host='0.0.0.0', port=5000)
