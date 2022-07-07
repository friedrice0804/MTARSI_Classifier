from keras.models import load_model
from django.conf import settings

import tensorflow as tf
import numpy as np
import cv2


class load_pred_model:
    def __init__(self, compile = True):
        self.prediction_model = load_model(settings.TFMODEL_DIR, compile=compile)

    def predictor(self, img):
        return self.prediction_model(img)


class getResults:
    def __init__(self, print_planeTitle = True):
        self.print_planeTitle = print_planeTitle
        self.pred = load_pred_model()
        self.angles = None
    
    def __call__(self, file_dir, angles = [-90, 0, 180, 90, 30, 45, 35, 25, 100], rotations = True):
        if rotations:
            self.angles = angles
            return self.rotationResults(file_dir)
        else:
            return self.nonRotationResults(file_dir)
    
    def imagepipe(self, img):
        image = cv2.resize(img, (180, 180))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype('float32')
        img = image / 255.0

        rgb_to_tensor = tf.convert_to_tensor(img, dtype = tf.float32)
        img = tf.expand_dims(rgb_to_tensor, 0)

        return img

    def nonRotationResults(self, file_dir):
        img = cv2.imread(file_dir)

        # to imagepipe function
        img =self.imagepipe(img)

        # prediction
        pred = self.pred.predictor(img)
        cls = np.argmax(pred, axis = 1)

        if self.print_planeTitle:
             cls = classtoPlane(int(cls))

        return cls
        
    def rotationResults(self, file_dir):
        idxs = []

        for angle in self.angles:
            img = cv2.imread(file_dir)

            # Rotations per angle
            (h, w) = img.shape[:2]
            center = (w / 2, w / 2)
            M = cv2.getRotationMatrix2D(center, angle, 1)
            rot = cv2.warpAffine(img, M, (w, h))

            # to imagepipe function
            img = self.imagepipe(rot)

            # prediction
            pred = self.pred.predictor(img)
            classes = np.argmax(pred, axis = 1)
            idxs.append(int(classes))
        
        cls =  max(set(idxs), key=idxs.count)

        # To be replaced with logging
        print('indices: {}, majority: {}'.format(idxs, cls))

        if self.print_planeTitle:
             cls = classtoPlane(int(cls))
        
        return cls


def classtoPlane(pred):
        labels = ['A-10 Thunderbolt',
                  'ATR-72 Airliner',
                  'ATR_72 ASW',
                  'Airliner',
                  'B-1 Lancer',
                  'B-29 Superfortress',
                  'B-2 Spirit',
                  'B-52 Stratofortress',
                  'B-57 Canberra',
                  'BusinessJet',
                  'C-130 Hercules',
                  'C-135 Stratolifter',
                  'C-17 Globemaster',
                  'EADS CASA C-295',
                  'C-40 Clipper',
                  'C-5 Galaxy',
                  'DC-4',
                  'DC-4E',
                  'E-2 Hawkeye',
                  'E-3 Sentry',
                  'EA-6B Prowler',
                  'F-15 Eagle',
                  'F-16 Falcon',
                  'F/A-18 Hornet',
                  'F-22 Raptor',
                  'F-35 JSF',
                  'F-4 Phantom',
                  'KC-767 Tanker',
                  'King Air Beechcraft (Airliner)',
                  'King_Air_Beechcraft (ISR)',
                  'LightACHighSetWing',
                  'LightACLowSetWing',
                  'LightACTwinEnginProp',
                  'None_taxiways_runways',
                  'P-3 Orion',
                  'Boeing RC-135',
                  'Su-37 Flanker',
                  'T-1A Jayhawk Trainer',
                  'T-43A_Boeing 737-253A_Trainer',
                  'Tupolev Tu-160',
                  'UTA Fokker 50 Utility Transport',
                  'Unknown']

        label = labels[pred]
        return label