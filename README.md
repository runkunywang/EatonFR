# Face Recognition Tutorial
A multi-threaded version of real-time face recognition via webcam (inspired by ageitgey/face_recognition).

## Table of Contents
* [Installation](#installation)
    * [Requirements](#requirements)
    * [Downloading required libraries](#downloading-required-libraries)
    
* [Usage](#usage)
    * [How to add images to the model](#how-to-add-images-to-the-model)
    * [Running the model](#running-the-model)
    
* [Model Info](#model-info)

* [Developer Section](#developer-section)

*[Reference Links](#reference-links)

## Installation
### Requirements
* Python 3.3+
* MacOS

### Installing dependencies
* Cmake
    * Using Homebrew on MacOS
        > `brew install cmake`
        
### Downloading required libraries
We suggest using the standard `pip3` package manager to install the libraries below in a terminal window.
* Numpy
    >`pip3 install numpy`
* Matplotlib
    >`pip3 install matplotlib`
* Dlib
    >`pip3 install dlib`
* OpenCV
    >`pip3 install opencv-python`
* Python Setup Tools (for pkg-resources library)
    >`pip3 install setuptools`
* In_place (for add_face.py)
    >`pip3 install in_place`

## Usage
### How to add images to the model
Follow the following steps to add a new image to the face recognition model:
* You can use the add_face.py script to add an image file with a custom name to the face recognition model. In case you do not specify a person name, the file name (without the extension) will be treated like the person name.
> Syntax: `python3 add_face.py -f <FILE_PATH> -n "<PERSON NAME>"`
> Example: `python3 add_face.py -f johnPic.jpg -n "John Smith"`
> Example (without custom name): `python3 add_face.py -f John\ Smith.jpg'`

* In case there are any issues with the above script, you can follow the steps below to manually add the images to your face recognition model.

* Drag the image to the same folder as the python program file (preferably jpeg images).

* In the main function, add a line with the image file name inside the `known_face_encodings` variable.
    >`FaceRecognition.face_encodings(FaceRecognition.load_image(<IMAGE_FILENAME>))[0]`
<p align="center">
    <img src="/docs/known_encodings.png">
</p>

* Again in the main function, add a corresponding line with the person's name in the `known_face_names` variable. Be careful to maintain the same relative ordereing as the `known_face_encodings` variable above.
<p align="center">
    <img src="/docs/known_face_names.png">
</p>

* Your model is good to go! Feel free to run and test the program now.

### Running the model
The program requires no additional arguments. You can simply run it like a python file. Simply, in the terminal, type:
> `python3 face_recognition_webcam_mt.py`

To exit the program, simply quit the application. You can use the shortcut `Cmd+Q'. You can also just press the 'q' key to exit.

## Model Explanation
For this face recognition program, we use pre-trained dlib models from [this](https://github.com/davisking/dlib-models) github repository by David King. The two models we are currently using in our code along with their description from the source are listed below.
* shape_predictor_5_face_landmarks.dat: This is a 5 point landmarking model which identifies the corners of the eyes and bottom of the nose. It is trained on the [dlib 5-point face landmark dataset](http://dlib.net/files/data/dlib_faces_5points.tar), which consists of 7198 faces.
* dlib_face_recognition_resnet_model_v1.dat: This model is a ResNet network with 29 conv layers. It's essentially a version of the ResNet-34 network from the paper Deep Residual Learning for Image Recognition by He, Zhang, Ren, and Sun with a few layers removed and the number of filters per layer reduced by half. The network was trained from scratch on a dataset of about 3 million faces.

More details about the models can be found on David King's [repo](https://github.com/davisking/dlib-models).

## Developer Section
Our code comprises of three classes (FaceRecognition, WebcamVideoStream, FaceRecognitionProcess) and the main function.
1. FaceRecognition: This class is used to process known images in the dataset. It also provides functions for comparing two face encodings.
    * trim_bounds: function for drawing a bounding box around a face in an image without exceeding image bounds.
        * arguments: 
            * bbox: 4-d tuple containing bounds for the face (left, top, right, bottom)
            * image_shape: 4-d tuple containing absolute bounds for the image (left, top, right, bottom)
        * returns: 4-d tuple containing the correct bounds for the faces in the images (left, top, right, bottom)
        
    * face_locations:  function for creating box bounds for all the faces in a given image.
        * arguments:
            * image: image being processed
            * upsample (optional): number of times the image is upsampled. default value is 1.
        * returns: an array containing 4-d tuples denoting bounding boxes for each face in an image.
        
    * load_image: function for loading an image.
        * arguments:
            * file: string containing image file path to be loaded
            * pixeltype (optional): cv2.IMREAD_COLOR by default.
        * returns: image pixels in a numpy array
        
    * face_encodings: function for encoding an image using pre-trained dlib models.
        * arguments:
            * image: image in a numpy array format.
            * locations (optional): pre-defined face locations. By default, the function finds face locations by itself.
            * upsample (optional): number of times the image is upsampled. default value is 1.
            * jitter (optional): If num_jitters>1 then each face will be randomly jittered slightly num_jitters times, each run through the 128D projection, and the average used as the face descriptor. ([source](http://dlib.net/python/index.html#dlib.face_recognition_model_v1))
        * returns: an array of face encodings for each face shape found in the image
        
    * encoding_distance: function for calculating the difference between a given encoding and an array of known encodings.
        * arguments:
            * known_encodings: an array of known face encodings
            * encoding check: a face encoding being checked
        * returns: an array containing the difference between a given encoding and each known encodings.
    
    * compare_encodings: functions for comparing encodings based on a tolerance level
        * arguments:
            * known_encodings: an array of known face encodings
            * encoding check: a face encoding being checked
            * tolerance (optional): tolerance level. default value is 0.5
        * returns: a list of boolean values for each known encoding
        
1. WebcamVideoStream: This class is used to open and maintain the webcam stream on a separate thread.
    * Initializer: constructor function
        * arguments:
            * src (optional): default value is 0 (for webcam)
    
    * start: starts the webcam video
        * returns: the WebcamVideoStream instance itself
        
    * update: updates the webcam feed frame-by-frame
    
    * read: reads a frame from the webcam stream
        * returns: a frame from the webcam stream
        
    * stop: stops the webcam stream
    
1. FaceRecognitionProcess: This class is used to capture a frame from the webcam stream, find faces in it, encode it, and compare it with other known face encodings.
    * Initializer: constructor function
        * arguments:
            * fx: horizontal resizing dimension (for the frame)
            * fy: vertical resizing dimension (for the frame)
            * capture: WebcamVideoStream instance
            * known_encodings: Known face encodings
            * known_names: corresponding names for the known_encodings

    * start: starts the facial recognition process
        * returns: the FaceRecognitionProcess instance itself 

    * process: function that grabs a frame from the webcam stream, resizes it, finds faces in it, encodes it, and compares it to the known encodings.
    
    * stop: stops the facial recognition process
    
Finally, the main function takes care of the known encodings and known names. It then sets up the FaceRecognitionProcess object to run. Also, it takes care of displaying the bounding boxes along with the person name on the webcam stream.
    
## Reference Links
* Object Detection with Face Recognition: https://github.com/fzehracetin/object-detection-with-face-recognition
* Object Detection Reference (on Windows): https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10 
