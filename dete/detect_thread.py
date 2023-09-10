from threading import Thread
from ultralytics import YOLO
import numpy as np

class detet_thread(Thread):
    r"""
    this class mainly solve function of the detection of object, then 
    push object's infomation in the video which sended by camare to other moudle if they need
    """
    def __init__(self):
        Thread.__init__(self)
        self.img_array = np.array([])
        self.result = []


        # Load a model
        self.model = YOLO("yolov8n.yaml")  # build a new model from scratch
        self.model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)


    def run(self):
        #predict   
        results = self.model(self.img_array)  # predict on an image

        #push result
        self.result = results

    # Train the model
    # model.train(data="coco128.yaml", epochs=3)  # train the model
    # metrics = model.val()  # evaluate model performance on the validation set