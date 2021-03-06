import cv2
import numpy as np
import os
import sys
from samples import coco
from mrcnn import utils
from mrcnn import model as modellib

# Input the original image name
os.system('clear')
original_image = input("Enter image name (put it in current folder)  : ")

# Use OpenCV to read the original image
image = cv2.imread(original_image)
intent= int(input("Input intentsity of Blur no between 1 to 50(only odd no) :"))


print("Read original image successfully! The original image shape is:")
print(image.shape)
blur = cv2.GaussianBlur(image ,(intent,intent),0)
blur1 = cv2.GaussianBlur(image ,(intent,intent),0)
cv2.imshow("blur",blur)
k = cv2.waitKey(0)
if k == 27:                 
    cv2.destroyAllWindows()
elif k == ord('s'):        
    name2 = os.path.splitext(original_image)[0]+"_blur_image.jpg"
	cv2.imwrite(name2, blur)
    cv2.destroyAllWindows()


# Load the pre-trained model data
ROOT_DIR = os.getcwd()
MODEL_DIR = os.path.join(ROOT_DIR, "logs")
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)


# Change the config infermation
class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    
    # Number of images to train with on each GPU. A 12GB GPU can typically
    # handle 2 images of 1024x1024px.
    # Adjust based on your GPU memory and image sizes. Use the highest
    # number that your GPU can handle for best performance.
    IMAGES_PER_GPU = 1
    
config = InferenceConfig()

# COCO dataset object names
model = modellib.MaskRCNN(
    mode="inference", model_dir=MODEL_DIR, config=config
)
model.load_weights(COCO_MODEL_PATH, by_name=True)

class_names = [
    'BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
    'bus', 'train', 'truck', 'boat', 'traffic light',
    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
    'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
    'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
    'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard',
    'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
    'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
    'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
    'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
    'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
    'teddy bear', 'hair drier', 'toothbrush'
]



def apply_mask(image, mask):
    blur[:, :, 0] = np.where(
        mask == 0,
        blur[:, :,0],
        image[:, :, 0]
    )
    blur[:, :, 1] = np.where(
        mask == 0,
        blur[:, :,1],
        image[:, :, 1]
    )
    blur[:, :, 2] = np.where(
        mask == 0,
        blur[:, :,2],
        image[:, :, 2]
    )
    return blur
    

def apply_mask2(image, mask):
    blur1[:, :, 0] = np.where(
        mask == 0,
        image[:, :, 0],
        blur1[:, :,0]
    )
    blur1[:, :, 1] = np.where(
        mask == 0,
        image[:, :, 1],
        blur1[:, :,1]
    )
    blur1[:, :, 2] = np.where(
        mask == 0,
        image[:, :, 2],
        blur1[:, :,2]
    )
    return blur1   



# This function is used to show the object detection result in original image.
def display_instances(image, boxes, masks, ids, names, scores):
    # max_area will save the largest object for all the detection results
    max_area = 0
    
    # n_instances saves the amount of all objects
    n_instances = boxes.shape[0]

    if not n_instances:
        print('NO INSTANCES TO DISPLAY')
    else:
        assert boxes.shape[0] == masks.shape[-1] == ids.shape[0]

    for i in range(n_instances):
        if not np.any(boxes[i]):
            continue

        # compute the square of each object
        y1, x1, y2, x2 = boxes[i]
        square = (y2 - y1) * (x2 - x1)

        # use label to select person object from all the 80 classes in COCO dataset
        label = names[ids[i]]
        if label == 'person':
            # save the largest object in the image as main character
            # other people will be regarded as background
            if square > max_area:
                max_area = square
                mask = masks[:, :, i]
            else:
                continue
        else:
            continue

        # apply mask for the image
    save1 = apply_mask(image, mask)
    save2 = apply_mask2(image,mask)
    return save1,save2


## run fast rcnn model
results = model.detect([image], verbose=0)
r = results[0]

##applying our effect

frame1 ,frame2= display_instances(
    image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores']
)


## save image
cv2.imshow('potrait_image', frame1)

# Wait for keys to exit or save
k = cv2.waitKey(0)
if k == 27:                 
    cv2.destroyAllWindows()
elif k == ord('s'):        
    name = os.path.splitext(original_image)[0]+"_potrait_image.jpg"
	cv2.imwrite(name,frame1)
    cv2.destroyAllWindows()


cv2.imshow('blur_person', frame2)

# Wait for keys to exit or save
k = cv2.waitKey(0)
if k == 27:                 
    cv2.destroyAllWindows()
elif k == ord('s'):        
    name1 = os.path.splitext(original_image)[0]+"_blur_person_image.jpg"  
	cv2.imwrite(name1,frame2)
    cv2.destroyAllWindows()



