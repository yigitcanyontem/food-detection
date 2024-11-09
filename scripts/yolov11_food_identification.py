import os
import cv2
import base64
import json
import io
from ultralytics import YOLO

# Model path and parameters
# model_path = "../weights/hotel_room_dataset_best_25_epochs.pt"
model_path = "../runs/detect/train10/weights/best.pt"
confidence_threshold = 0.1  # Confidence threshold for detections
iou_threshold = 0.1   # IoU threshold for NMS (non-maximum suppression)

# Load the model
model = YOLO(model_path)

# Extract model name from the model path
model_name = os.path.basename(model_path).split(".")[0]

# Define the main results directory based on the format
main_save_dir = f"./results_{model_name}_th_{iou_threshold}_conf_{confidence_threshold}"
os.makedirs(main_save_dir, exist_ok=True)

# Run the model with specified thresholds
results = model.predict(source="../test_images", conf=confidence_threshold, iou=iou_threshold)

# List to store all JSON data
all_json_data = []

for i, result in enumerate(results):
    # Create a subdirectory for each image
    img_save_dir = os.path.join(main_save_dir, f"image_{i}")
    os.makedirs(img_save_dir, exist_ok=True)

    # Load the original image and the annotated image
    img_path = result.path  # Original image path
    img = cv2.imread(str(img_path))

    # Save the annotated image with detections
    annotated_img = result.plot()
    annotated_img_path = os.path.join(img_save_dir, f"annotated_image_{i}.jpg")
    cv2.imwrite(annotated_img_path, annotated_img)

    # List to store detected objects for the current image
    image_objects = []

    # Save each detected object as a separate image and generate JSON
    for j, box in enumerate(result.boxes):
        # Get the label name and bounding box coordinates
        label_id = int(box.cls.item())  # Convert tensor to int
        label_name = result.names[label_id]  # Class label
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates

        # Crop and save the detected object
        cropped_img = img[y1:y2, x1:x2]
        cropped_img_path = os.path.join(img_save_dir, f"{label_name}_{i}_{j}.jpg")
        cv2.imwrite(cropped_img_path, cropped_img)

        # Convert the cropped image to base64
        _, img_encoded = cv2.imencode('.jpg', cropped_img)  # Encode image to .jpg format
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')  # Convert to base64 string

        # Add the object data to the list
        object_data = {
            "label": label_name,
            "img": img_base64
        }
        image_objects.append(object_data)

    # Save JSON data for the current image
    json_file_path = os.path.join(img_save_dir, "objects.json")
    with open(json_file_path, "w") as json_file:
        json.dump(image_objects, json_file, indent=4)

    # Append to the overall JSON data list
    all_json_data.append({
        "image_id": i,
        "objects": image_objects
    })

# Optionally, save all results in a single JSON file
all_json_file_path = os.path.join(main_save_dir, "all_detected_objects.json")
with open(all_json_file_path, "w") as all_json_file:
    json.dump(all_json_data, all_json_file, indent=4)
