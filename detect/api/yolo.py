"""
TPDS Detect API :: YOLOv3 Model
"""

import argparse
import os
import time

import numpy as np
import cv2

# === YOLO config variables === #
# Paths to necessary files
yolo_path = "detect/api/yolo_config"
weights_path = os.path.join(yolo_path, "yolo-obj_1000.weights")
config_path = os.path.join(yolo_path, "yolo-obj.cfg")
classes_path = os.path.join(yolo_path, "classes.txt")
# Config vars
conf_thresh = 0.5  # Confidence threshold
nms_thresh = 0.1  # Non-maximum suppression
input_height = 416  # Height of network's input image
input_width = 416  # Width of network's input image
input_dim = (input_height, input_width)

# === YOLO utility functions === #


def get_labels(class_file: str):
    """
    Load the tpds class labels that the model was trained on.
    
    :param class_file (str) : Path to class file (classes.txt).
    :return classes (list)  : List of classes model was trained on.
    """
    with open(class_file, "r") as clf:
        classes = clf.read().splitlines()
    return classes


def load_model(config_file: str, weights_file: str):
    """
    Loads and instantiates the object detection model using 
    opencv2's dnn (deep neural network) module.
    
    :param config_file (str)  : Path to `.cfg` file used to train the model.
    :param weights_file (str) : Path to `.weights` file to use for inference.
    :return net (cv2.dnn)     : Instantiated and configured model.
    """
    net = cv2.dnn.readNetFromDarknet(config_file, weights_file)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    return net


def get_prediction(image, img_dim: tuple = (416, 416)):
    """
    Run object detection on image and return detections.
    
    :param image (np.uint8)  : Image array on which to run inference.
    :param net (cv2.dnn)     : Instantiated YOLO model
    :param labels (list)     : List of class labels.
    :return prediction (str) : Predicted object.
    """
    # Get class labels
    classes = get_labels(classes_path)

    # Instantiate network
    net = load_model(config_path, weights_path)

    (H, W) = image.shape[:2]

    # Determine only the output layer names we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Construct a blob from the input image, then run a forward pass
    # of the detector, giving the bboxes and probabilities.
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, img_dim, swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layer_outputs = net.forward(ln)
    end = time.time()
    msg = f"[INFO] YOLO took {end - start:.6f} seconds."  # Set up timing message
    # print(msg)  # Print timing message

    # Initialize lists for bboxes, confidences, and class_ids
    boxes, confidences, class_ids, class_names = [], [], [], []

    # Loop over each layer of the layer outputs
    for output in layer_outputs:
        # Loop over each of the detections
        for detection in output:
            # Extract the class_id and confidence (proba) of current object
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Filter out weak predictions
            if confidence > conf_thresh:
                # Scale bbox coord back to size of image
                box = detection[0:4] * np.array([W, H, W, H])
                (center_x, center_y, width, height) = box.astype("int")

                # Use the center coords to calc top and left corner of box
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))

                # Update lists
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                class_names.append(classes[class_id])

    # Apply non-max suppression
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf_thresh, nms_thresh)

    return idxs

