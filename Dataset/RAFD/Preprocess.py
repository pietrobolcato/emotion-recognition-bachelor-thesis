import os
import cv2

input_dir = "./Images/"
out_dir = "./Classified/"
y = 1024
x = 681

for i in range(0,7):
	l = os.listdir("./" + str(i))
	for j in l:
		path = input_dir + str(i) + "/" + j
		out_path = out_dir + str(i) + "/" + j
		print(path)
		img_src = cv2.imread(path)
		img_src = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
		img_src = img_src[190:740, 0:x]
		img_src = cv2.resize(img_src, (48, 48), interpolation = cv2.INTER_CUBIC)
		cv2.imwrite(path,img_src)