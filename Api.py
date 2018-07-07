import json
import numpy
import time
import uuid
import os
import Music
from tflearn import DNN
from cv2 import CascadeClassifier
from flask import Flask, jsonify, request, make_response, Response
from flask_cors import CORS
from Network import Network

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

app = Flask(__name__, static_url_path = "")
CORS(app)
model_path = "./Model/fjra_30.tfl"

network = Network.Define()
model = DNN(network)
model.load(model_path)
cascade = CascadeClassifier("./Utils/cascade.xml")

@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/emotions/api/v1.0/recognition', methods=['POST'])
def image():
	name = str(uuid.uuid4())+".jpg"
	i = request.files['image']  # get the image
	i.save(name)
	
	start_time = time.time()
	p = Network.Predict(name,model_path,"./Utils/cascade.xml",load=model,openCv=cascade)
	songs = Music.GetByMood(p[0][0])
	elapsed_time = time.time() - start_time
	
	os.remove(name)
	p.append(elapsed_time)
	p.append(songs)
	j = json.dumps(p,cls=MyEncoder)

	return Response(j)
    
if __name__ == '__main__':
	app.run(debug = True)
