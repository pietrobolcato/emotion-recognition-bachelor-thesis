import os
import cv2
from shutil import copyfile

emo_l = ["angry","neutral","disgust","fear","happy","sad","surprise"]
num_l = ["0","1","2","3","4","5","6"]

cascade_classifier = cv2.CascadeClassifier("h.xml")

for root, directories, filenames in os.walk('./Labels/'):
	for filename in filenames: 
		emo_file = os.path.join(root,filename)
		emo = open(emo_file,"r").read().strip()[0]
		print("\n[+] " + emo_file + ": " + emo + " (" + emo_l[int(emo)-1] + ")" )

		root_image = root.replace("Labels","Images")
		image_list = os.listdir(root_image)
		image_list = sorted(image_list)
		count = len(image_list)
		half = int(count/2)
		image_list = image_list[half:count]
		for f in image_list:
			src = root_image + "/" + f
			dest = "./Classified/" + emo_l[int(emo)-1] + "/" + f
			print(src + "  ->  "  + dest)

			img_src = cv2.imread(src)
			img_src = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
			faces = cascade_classifier.detectMultiScale(img_src,scaleFactor = 1.3,minNeighbors = 5)
			# None is we don't found any face - try to give back the whole picture anyway, but probably won't work welll
			if not len(faces) > 0:
				img_src = cv2.resize(img_src, (48, 48), interpolation = cv2.INTER_CUBIC)
				cv2.imwrite(dest,img_src)
			else:
				max_area_face = faces[0]
				for face in faces:
					if face[2] * face[3] > max_area_face[2] * max_area_face[3]:
						max_area_face = face
				# Chop image to face
				face = max_area_face
				img_src = img_src[face[1]:(face[1] + face[2]), face[0]:(face[0] + face[3])]
				# Resize image to network size			
				img_src = cv2.resize(img_src, (48, 48), interpolation = cv2.INTER_CUBIC)
				cv2.imwrite(dest,img_src)
				#input()			
				#copyfile(src,dest)
