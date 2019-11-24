#!flask/bin/python
from flask import Flask, jsonify, request
from shotbot import Bot, Relay

app = Flask(__name__)
targets = [1,1]

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if (request.method=='POST'):
        print "saving some shit"
        targets = request.json['target']
    return jsonify({'target': targets})

if __name__ == '__main__':
    app.run(debug=True)