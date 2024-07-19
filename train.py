import os
import torch
import logging
from ultralytics import YOLO

logging.basicConfig(filename='log-error.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

if __name__ == '__main__':

    try:

        model   = YOLO("yolov8n-seg.pt")
        results = model.train(
                batch=8,
                data="conf_yaml.yaml",
                device='cpu',
                epochs=40,
                imgsz=640,
            )

    except Exception as e:

        logging.error(exc_info=e)
