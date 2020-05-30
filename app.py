import os
import sys
import  numpy as np
import pickle
from collections import defaultdict

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect


# Declare a flask app
app = Flask(__name__)


print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(bug_id):
    values = defaultdict()
    
    infile=open('models/pred','rb')
    x=pickle.load(infile)
    print(x)
    yp=np.argmax(x,axis=1)
    outfile=open('models/cl','rb')
    y=pickle.load(outfile)
    
    jsonFile = open('models/deep_data.json','rb')
    temp = json.load(jsonFile)
    print(y)
    
    for entry in temp:
        values[entry[0]] = {
            'issue_id' : entry[1],
            'issue_title' : entry[2],
            'reported_time' : entry[3],
            'owner' : entry[4],
            'description' : entry[5]
        }
      
    #for key in values.keys():
    #    print(values[key]['description'])
    #print(values[bug_id]['description'])
    
    name = y[yp[int(bug_id)]]
    desc = values[bug_id]['description']
    return (name , desc)


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
         bug_id = request.form.get('bug_id')
         devname,description = model_predict(bug_id)
         return render_template('index.html', dev =devname, desc=description)

if __name__ == '__main__':
    app.run(port=5007, threaded=False)

    # Serve the app with gevent
    #http_server = WSGIServer(('0.0.0.0', 5000), app)
    #http_server.serve_forever()
