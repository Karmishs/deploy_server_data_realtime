from ultralytics import YOLO
import os
import cv2
# Load a pretrained YOLOv8n model
model = YOLO('yolov8x.pt')

def get_image_files(folder_path):
    image_files = []
    # Lặp qua tất cả các tệp và thư mục trong thư mục
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Kiểm tra xem tệp có phải là tệp ảnh không
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # Nếu là tệp ảnh, thêm vào danh sách
                image_files.append(file_path)
    return image_files

def detect_objects(img):
    # Thực hiện inference
    results = model(img, conf=0.03)
    
    # Tạo từ điển để lưu số lượng các vật thể của mỗi loại
    object_counts = {}
    
    # Lặp qua các kết quả và đếm số lượng các vật thể của mỗi loại
    for result in results:
        # Lấy các hộp giới hạn và nhãn tương ứng từ kết quả
        boxes = result.boxes.cpu().numpy()  # Get boxes on CPU in numpy format
        labels = result.names
        
        # Duyệt qua từng hộp giới hạn và nhãn
        for box in boxes:  # Iterate over boxes
            class_id = int(box.cls[0])  # Get class ID
            class_name = labels[class_id]  # Get class name using the class ID
            
            # Tăng số lượng của loại vật thể trong từ điển
            if class_name in object_counts:
                object_counts[class_name] += 1
            else:
                object_counts[class_name] = 1
                
                
    print(object_counts)
    totalobject = 0
    if 'car' in object_counts:
        totalobject += object_counts['car'] * 4
    if 'truck' in object_counts:
        totalobject += object_counts['truck'] * 8
    if 'bus' in object_counts:
        totalobject += object_counts['bus'] * 12
    if 'bicycle' in object_counts:
        totalobject += object_counts['bicycle'] * 1
    
    if 'motorcycle' in object_counts and 'person' in object_counts:
        totalobject += object_counts['motorcycle'] if object_counts['motorcycle'] > object_counts['person'] else object_counts['person']
    
    traffic_status = ''
    if totalobject < 60:
        traffic_status = 'Low'
    elif totalobject < 120:
        traffic_status = 'Medium'
    else:
        traffic_status = 'High'
    return traffic_status
    
# Load ảnh từ tệp
image_files = get_image_files(r'C:\Workspace\UDPTDLTM\Weather-and-Daily-Life\traffic camera')

# Lặp qua tất cả các tệp ảnh
for image_file in image_files:
    # Đọc ảnh từ tệp
    img = cv2.imread(image_file)
    
    # Thực hiện phát hiện vật thể
    totalobject = detect_objects(img)
    
    # Lưu số lượng kết quả vào file csv
    with open('traffic_count.csv', 'a') as f:
        f.write(f'{image_file},{totalobject}\n')