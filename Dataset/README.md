# Dataset

The final dataset used is a combination of several datasets:<br/>
[FER2013](https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data)<br/>
[RAFD](http://www.socsci.ru.nl:8180/RaFD2/RaFD?p=main)<br/>
[AffectNet](http://mohammadmahoor.com/affectnet/)<br/>
[Kohn-Kanade](http://www.consortium.ri.cmu.edu/ckagree/)<br/>

The permission to download them has to be requested. Then, every dataset has is own script that preprocess, normalise and classify the images in order to be used as a combined dataset.
Finally, [SideFunctions.py](https://github.com/seicaratteri/emotions_thesis_final/blob/master/SideFunctions.py) file is used to create the .h5 file used to train the network.
