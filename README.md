# Fighter aircrafts classifer with Django backend
This is a simple fighter aircrafts classfier using a
convolutional neural network. The CNN model itself is a 
pre-trained InceptionV3 architecture, 
and is used for transfer learning of custom dataset in this project.

The custom dataset is called 
MTARSI(Multi-type Aircraft of Remote Sensing Images),
and you can download via following link if necessary.

https://zenodo.org/record/5044950#.YsZY_2DP2Uk

Whilst this is mainly a deep learning project,
the project is intended to remind myself how to
design a backend and a simple frontend(bootstrap) with
a deep learning model. 

You can also refer to colab notebook files in the project folder
if you want to know how the training was done.

## So what is it exactly?
It is a CNN model that identifies fighter aircrafts  
that runs on your web browser, and it uses Django backend to
handle input and output data from the tensorflow model. 

* You can only classify a single aircraft at a time.
* Only top-view images like satelite imagery are valid as input data.
* You can simply crop images of aircrafts from imagery sources like Google Maps or Google Earth.

## How to use

* Download pretrained CNN model(InceptionV3) with MTARSI dataset from following link:
https://drive.google.com/drive/folders/1Io_eTAVVlj0fsYXTD7vkVRw4ATlliqR5?usp=sharing

place TF-MODEL folder in the main directory of the project folder.

* To run this project, simply run following commands in terminal in the main project folder.
```
$ python manage.py runserver
```

* Required frameworks(libraries) can be installed with following command.
```
$ pip install -r requirements.txt
```

