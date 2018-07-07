# Deep Learning approach to Facial Emotion Recogniton and Music Suggestion

## Abstract
The capability of a system to automatically recognize and classify human emotions has always been one of the key problems in human-computer interaction. This multidisciplinary task involves a wide variety of related fields including computer vision among the others. There are many different types of visual signals that can be used to understand the underlying emotion in a person. Nevertheless, it is widely acknowledged that facial expressions can give the most significant clues. 

This dissertation proposes a deep learning approach to static image-based emotion recognition in an uncontrolled environment as well as presenting its potentiality with a demo application capable of suggesting music according to the user recognized mood. The proof of concept outlined by the application can be further developed and it can be integrated as a part of a larger music recommendation system, useful in modern on-demand music streaming services including Spotify or Apple Music. 

The final proposed model is a 32 layers Residual Neural Network trained on the combination of four different datasets composed of labelled images from both controlled and uncontrolled environments. As every dataset has different image specifications and different type of labelled emotions, the data preprocessing and normalization proves to be a crucial step for the good network training capabilities. It helps to remove irrelevant noise, to reduce biases between the classes and unifies all the faces in the same domain. The additional use of a face detector at both preprocessing and testing time along with the generation of randomized perturbation at training time further increase the classification performances of unseen face examples. The proposed method surpasses the accuracy baseline for every dataset used.
 
The demo application implements a backend that offers the RESTful API used to run the model to access the network capabilities and to get music suggestions based on an input emotion. The frontend interface is an HTML5, CSS3 and JavaScript application that manages the camera and acquisition of the snapshot. It connects to the backend endpoint and access the API through AJAX to have the prediction about the emotions and the songs suggestions.

## Getting started

First install the requirements with

```
pip install -r "requirements.txt"
```

Then run the backend with

```
python Api.py
```

And start the frontend by opening with a browser `App/index.html`