from picamera2 import Picamera2
from ultralytics import YOLO
from time import sleep
import math
import cv2
import os

import torch.nn.functional as F
import torch


class Camera:
    def __init__(self, model_paths=None):
        self.models = []
        for model_path in model_paths:
            model = YOLO(model_path)
            class_names = os.path.splitext(os.path.basename(model_path))[0].split('-')
            print(class_names)
            self.models.append((model, class_names))

        self.picam2 = Picamera2()
        self.camera_config = self.picam2.create_preview_configuration(main={"format": "RGB888"})
        self.picam2.configure(self.camera_config)
        self.picam2.start()

    def predict(self, trial=3):
        sleep(2)
        img = self.picam2.capture_array()
        #image_bgr = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_YUY2)
        image_bgr = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        prediction = []
        for i in range(trial):

            for model in self.models:
                results = model[0](image_bgr, conf=0.5)
                for result in results:
                    detections = result.boxes

                    for det in detections:
                        prediction.append((model[1][int(det.cls[0].item())], det.conf[0].item()))

        plastic_bottles_points = [cls[1] for cls in prediction if cls[0] == 'plastic_bottles']
        print(plastic_bottles_points)

        return prediction
    
    def view(self):
        while True:
            frame = self.picam2.capture_array()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_YUY2)

            print(frame.shape)

            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        cv2.destroyAllWindows()
        self.picam2.stop()

    def stream(self):
        while True:
            frame = self.picam2.capture_array()
            #frame_bgr = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_YUY2)
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            height, width = frame_bgr.shape[:2]
            new_width = int(width * 0.8)
            new_height = int(height * 0.8)

            # Calculate cropping box coordinates
            center_x, center_y = width // 2, height // 2
            crop_x1 = center_x - new_width // 2
            crop_y1 = center_y - new_height // 2
            crop_x2 = center_x + new_width // 2
            crop_y2 = center_y + new_height // 2

            cropped_frame = frame_bgr[crop_y1:crop_y2, crop_x1:crop_x2]

            for model in self.models:
                results = model[0](cropped_frame, stream=True)

                for r in results:
                    boxes = r.boxes

                    for box in boxes:
                        # bounding box
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values
                        
                        # confidence
                        confidence = math.ceil((box.conf[0]*100))/100
                        
                        if confidence >= 0.5:

                            # put box in cam
                            cv2.rectangle(frame_bgr, (x1 + crop_x1, y1 + crop_y1), (x2 + crop_x1, y2 + crop_y1), (255, 0, 255), 3)

                            # class name
                            cls = int(box.cls[0])

                            # object details
                            org = [x1 + crop_x1, y1 + crop_y1]
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            fontScale = 1
                            color = (255, 0, 0)
                            thickness = 2

                            cv2.putText(frame_bgr, model[1][cls] + f" {confidence}", org, font, fontScale, color, thickness)
                            print(model[1][cls], confidence)
            
            cv2.imshow('Webcam', frame_bgr)
            if cv2.waitKey(1) == ord('q'):
                break

if __name__ == '__main__':
    #x = Camera("/home/admin/Desktop/bin-system/resources/Glass_Bottles-can-plastic_bottles.pt")
    x = Camera(model_paths=["/home/admin/Desktop/bin-system/resources/dry waste-wet waste.pt", "/home/admin/Desktop/bin-system/resources/Glass_Bottles-can-plastic_bottles.pt"])
    #x.stream()
    print(x.predict())
    #print(y)