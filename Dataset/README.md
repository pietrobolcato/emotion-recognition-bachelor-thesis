# Dataset

The final dataset used is a combination of several datasets:
[FER2013](https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data)
[RAFD](http://www.socsci.ru.nl:8180/RaFD2/RaFD?p=main)
[AffectNet](http://mohammadmahoor.com/affectnet/)
[Kohn-Kanade](http://www.consortium.ri.cmu.edu/ckagree/)

The permission to download them has to be requested. Then, every dataset has is own script that preprocess, normalise and classify the images in order to be used as a combined dataset.
Finally, the SideFunctions.py file is used to create the .h5 file used to train the network.
