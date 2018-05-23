from flask import Flask, jsonify, abort, request, make_response, url_for, Response
from flask_cors import CORS
from Network import Network
import json
import numpy

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

@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)
    
@app.route('/emotions/api/v1.0/recognition', methods = ['POST'])
def create_task():
	return jsonify( { 'task': 'gigi' } ), 201

@app.route('/image', methods=['POST'])
def image():
	i = request.files['image']  # get the image
	i.save('saved.jpg')
	p = Network.Predict("./saved.jpg",model_path,"./Utils/cascade.xml")
	j = json.dumps(p,cls=MyEncoder)

	return Response(j)
    
if __name__ == '__main__':
	app.run(debug = True)


