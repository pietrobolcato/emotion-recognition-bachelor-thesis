import os.path
import uuid
import cv2

csv = "./Automatically Annotated/Automatically_Annotated_file_lists/automatically_annotated.csv"
outdir = "./Automatically Annotated/Out_normalised/"
indir = "./Automatically Annotated/Automatically_Annotated_Images/Automatically_Annotated_Images/"

# affectnet:fer
dict = {"0":"6",
	"1":"3",
	"2":"4",
	"3":"5",
	"4":"2",
	"5":"1",
	"6":"0",
	"7":"6",
	"8":"6"}

num_lines = sum(1 for line in open(csv))
num_lines -= 1
c = 0

o = open(csv,"r")
next(o)
for line in o:
	c += 1
	percent = c*100/num_lines
	split = line.split(",")
	emotion = split[6]
	if (int(emotion) <= 8): 
		try:
			file = indir + split[0]
			extension = os.path.splitext(file)[1]
			gen = uuid.uuid4()
			emotion_path = outdir + dict[emotion] + "/" + str(gen) + extension
			start_x = int(split[1])
			start_y = int(split[2])
			end_x = start_x + int(split[3])
			end_y = start_y + int(split[4])
			print(	"File: " + file + 
			 	"\nEmo aff: " + emotion + 
			 	"\nEmo fer: " + dict[emotion] + 
			 	"\nOut path: " + emotion_path + 
			 	"\nStart x: " + str(start_x) + "\tEnd x: " + str(end_x) + 
			 	"\nStart y: " + str(start_y) + "\tEnd y: " + str(end_y) + 
			 	"\nPercent: " + str(percent) + " (" + str(c) + " over " + str(num_lines) + ")")
			
			img_src = cv2.imread(file)
			img_src = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
			img_src = img_src[start_y:end_y, start_x:end_x]
			img_src = cv2.resize(img_src, (48, 48), interpolation = cv2.INTER_CUBIC)
			img_src = cv2.equalizeHist(img_src)
			cv2.imwrite(emotion_path,img_src)
		except Exception as e:
			print("Error: " + str(e))
		
		print("____")
		
		#input()
