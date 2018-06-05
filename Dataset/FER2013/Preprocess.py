import csv
from PIL import Image

csv_in = "fer2013.csv"
output_dir = "./Classified/"
image_size = (48,48)
image_mode='RGB'

with open(csv_in,'r') as csvin:
	traindata=csv.reader(csvin, delimiter=',', quotechar='"')
	rowcount=0
	for row in traindata:
		if rowcount > 0:
			print('rows ' + str(rowcount) + "\n")
			x=0
			y=0
			pixels=row[1].split()
			img = Image.new(image_mode,image_size)
			for pixel in pixels:
				colour=(int(pixel),int(pixel),int(pixel))
				img.putpixel((x,y), colour)
				x+=1
				if x >= 48:
					x=0
					y+=1
			imgfile=output_dir+'/'+str(row[0])+'/'+str(rowcount)+'.png'
			img.save(imgfile,'png')
		rowcount+=1