from tflearn.data_utils import build_hdf5_image_dataset

class SideFunctions:
	def BuildH5FromDirectory(directory,size):
		build_hdf5_image_dataset(directory, image_shape=size, mode='folder', grayscale= True, categorical_labels=True, normalize=True)

SideFunctions.BuildH5FromDirectory("Model/Combined/",(48,48))