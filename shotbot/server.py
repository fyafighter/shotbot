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

@app.route('/center', methods=['PUT'])
def center():
    if(request.method=='PUT'):
        bot.center()
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

if __name__ == '__main__':
    bot = Bot("main_bot")
    app.run(host='0.0.0.0', port=5000)
