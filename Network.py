import h5py
import os
import cv2
import tensorflow as tf
import tflearn
import numpy as np

tf.reset_default_graph()

class Network:	
	def Define():	# less deep
		img_aug = tflearn.data_augmentation.ImageAugmentation()
		img_aug.add_random_flip_leftright()
		img_aug.add_random_crop((48, 48),6)
		img_aug.add_random_rotation(max_angle=25.)		

		img_prep = tflearn.data_preprocessing.ImagePreprocessing()
		img_prep.add_featurewise_zero_center()
		img_prep.add_featurewise_stdnorm()

		n = 5

		network = tflearn.input_data(shape=[None, 48, 48, 1], data_augmentation=img_aug, data_preprocessing=img_prep) #48 x 48 grayscale
		network = tflearn.conv_2d(network, 16, 3, regularizer='L2', weight_decay=0.0001)
		network = tflearn.residual_block(network, n, 16)
		network = tflearn.residual_block(network, 1, 32, downsample=True)
		network = tflearn.residual_block(network, n-1, 32)
		network = tflearn.residual_block(network, 1, 64, downsample=True)
		network = tflearn.residual_block(network, n-1, 64)
		network = tflearn.batch_normalization(network)
		network = tflearn.activation(network, 'relu')
		network = tflearn.global_avg_pool(network)
		# Regression
		network = tflearn.fully_connected(network, 7, activation='softmax')

		return network	
	
	def Train(h5_dataset,model_name,run_name,pre_load = False,tb_dir = './tfboard/',epoch=100,val=None):
		h5f = h5py.File(h5_dataset, 'r')
		X = h5f['X'] #images
		Y = h5f['Y'] #labels
		X = np.reshape(X, (-1, 48, 48, 1))
		
		val_set = 0.015
		
		if (val != None):
			print("Using validation set: " + val)
			validation = h5py.File(val, 'r')
			X_v = validation['X'] #images
			Y_v = validation['Y'] #labels
			X_v = np.reshape(X_v, (-1, 48, 48, 1))
			Y_v = np.reshape(Y_v, (-1, 7))
			val_set = (X_v,Y_v)

		network = Network.Define()
		mom = tflearn.Momentum(0.1, lr_decay=0.1, decay_step=8000, staircase=True)
		network = tflearn.regression(network, optimizer=mom,
				         loss='categorical_crossentropy')
		# Training
		model = tflearn.DNN(network,
				    clip_gradients=0.,
				    max_checkpoints=1,
				    checkpoint_path="./Utils/", 
				    tensorboard_dir=tb_dir, 
				    tensorboard_verbose=3)
		
		if (pre_load == True):
			model.load(model_name)

		model.fit(X, Y, n_epoch=epoch, validation_set=val_set, shuffle=True,
			  show_metric=True, batch_size=512,#128,
			  snapshot_epoch=True, run_id=run_name)

		model.save(model_name)
	
	def Predict(input_file,model_name,cascade_file,verbose=True,load=True,openCv=None):
		if (openCv == None):
			cascade_classifier = cv2.CascadeClassifier(cascade_file)
		else:
			cascade_classifier = openCv
		
		if (load):
			network = Network.Define()
			model = tflearn.DNN(network)
			model.load(model_name)
		else:
			model = load
		
		img = cv2.imread(input_file)
		result = model.predict(Network._FormatImage(img,cascade_classifier).reshape(1,48,48,1))

		labels = ["Angry","Disgust","Fear","Happy","Sad","Surprise","Neutral"]
		dic = {}
		for i in range(0,7):
			dic[labels[i]] = result[0][i]

		sorted_dic = sorted(dic.items(), key=lambda kv: kv[1], reverse=True)
		if (verbose):
			print(str(sorted_dic))
		
		return sorted_dic

	def Test(model_name,test_dir,cascade_file,verbose=True):
		cascade_classifier = cv2.CascadeClassifier(cascade_file)

		network = Network.Define()
		model = tflearn.DNN(network)
		model.load(model_name)

		avg = 0
		avg2 = 0
		labels = ["Angry","Disgust","Fear","Happy","Sad","Surprise","Neutral"]
		ret = []
		
		for i in range(0,7):
			c = 0
			c2 = 0
			l = os.listdir(test_dir+"/"+str(i))
			tot = len(l)
			for f in l:
				img = cv2.imread(test_dir+"/"+str(i)+'/'+f)
				try:
					format = Network._FormatImage(img,cascade_classifier)
					result = model.predict(format.reshape(1,48,48,1))
					dic = {}
					for j in range(0,7):
						dic[j] = result[0][j]

					sorted_dic = sorted(dic.items(), key=lambda kv: kv[1], reverse=True)
					first = sorted_dic[0][0]
					if (first == i):
						c+=1
						c2+=1
					elif (sorted_dic[1][0] == i):
						c2 += 1
				except Exception:
					tot -= 1
						
			percent = round(c * 100 / tot,5)
			percent2 = round(c2 * 100 / tot,5)
			avg += percent
			avg2 += percent2
			if (verbose):
				print(str(i) +  " (" + labels[i] + "):\t" + str(c) + " su " + str(tot) + " ( " + str(percent) + ")\t| Top 2: " + str(c2) + " su " + str(tot) + " (" + str(percent2) + ")")
			ret.append(percent)
		
		avg /= 7
		avg2 /= 7
		if (verbose):
			print("Average: " + str(avg))
			print("Average second emotion: " + str(avg2))	
		return ret

	def Ensemble(models,testDir):
		l = []
		for m in models:
			tf.reset_default_graph()
			l.append(Network.Test(m,testDir,"./Utils/h.xml",True))
		
		labels = ["Angry","Disgust","Fear","Happy","Sad","Surprise","Neutral"]
		avg = 0		

		for i in range(0,7):
			local_max = 0
			for j in range(0,len(l)):		
				if (l[j][i] >= local_max):
					local_max = l[j][i]
				
			print(str(i) +  " (" + labels[i] + "):\t" + str(local_max))		
			avg += local_max
		
		avg /= 7		
		print("Average: " + str(avg))
			
		

	def _FormatImage(image,cascade_classifier):
		if len(image.shape) > 2 and image.shape[2] == 3:
			image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		else:
			image = cv2.imdecode(image, cv2.CV_LOAD_IMAGE_GRAYSCALE)

		
		faces = cascade_classifier.detectMultiScale(image,scaleFactor = 1.3,minNeighbors = 5)

		# None is we don't found any face - try to give back the whole picture anyway, but probably won't work welll
		if not len(faces) > 0:
			return cv2.resize(image, (48, 48), interpolation = cv2.INTER_CUBIC) / 255.
			#return None
		max_area_face = faces[0]
		for face in faces:
			if face[2] * face[3] > max_area_face[2] * max_area_face[3]:
				max_area_face = face
		# Chop image to face
		face = max_area_face
		image = image[face[1]:(face[1] + face[2]), face[0]:(face[0] + face[3])]
		#image = cv2.equalizeHist(image)
		# Resize image to network size
		try:
			image = cv2.resize(image, (48, 48), interpolation = cv2.INTER_CUBIC) / 255.
		except Exception: # Problem during resize
			return None
		
		
		return image


path = "./Model/fjra_30.tfl"
#Network.Train("./Dataset/fjra.h5",path,"fjra",False,"./TFBoard/",epoch=30)
#Network.Test(path,"./Test/","./Utils/cascade.xml")
#Network.Predict("./saved.jpg",path,"./Utils/cascade.xml")
