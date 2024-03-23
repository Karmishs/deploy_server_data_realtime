import requests
import json
import os
from datetime import datetime
import schedule
import time
import pytz

def get_distance_data(origin, destination, api_key):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&departure_time=now&key={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def analyze_traffic(data):
    result = {}
    if data['status'] == 'OK':
        row = data['rows'][0]
        element = row['elements'][0]
        duration = element['duration']['value']
        duration_in_traffic = element['duration_in_traffic']['value']
        traffic_difference = duration_in_traffic / duration
        if traffic_difference > 1.5:
            traffic = 'heavy'
        elif traffic_difference > 1.25:
            traffic = 'moderate'
        else:
            traffic = 'light'
        result['origin'] = data['origin_addresses'][0]
        result['destination'] = data['destination_addresses'][0]
        result['duration'] = duration
        result['duration_in_traffic'] = duration_in_traffic
        result['traffic'] = traffic
        
        gmt7 = pytz.timezone('Asia/Ho_Chi_Minh')

        # Lấy thời gian hiện tại theo múi giờ GMT+7
        current_time_gmt7 = datetime.now(gmt7)

        # Format thời gian lấy dữ liệu thành chuỗi
        current_time_str = current_time_gmt7.strftime('%H-%M-%S')
        result['timestamp'] = current_time_str
    else:
        print("Failed to fetch data.")
    return result


def save_data(result):
    # Tạo đối tượng múi giờ cho múi giờ GMT+7
    gmt7 = pytz.timezone('Asia/Ho_Chi_Minh')

    # Lấy thời gian hiện tại theo múi giờ GMT+7
    current_time_gmt7 = datetime.now(gmt7)

    # Format thời gian lấy dữ liệu thành chuỗi
    current_time_str = current_time_gmt7.strftime('%H-%M-%S')

    # Tạo thư mục dựa trên ngày lấy dữ liệu
    current_date = current_time_gmt7.strftime('%Y-%m-%d')
    folder_path = os.path.join('traffic_data', current_date)
    os.makedirs(folder_path, exist_ok=True)

    # Tạo tên tệp tin dựa trên thời gian lấy dữ liệu
    file_name = f"{current_time_str}.json"
    file_path = os.path.join(folder_path, file_name)

    # Lưu dữ liệu vào tệp tin JSON
    with open(file_path, 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, ensure_ascii=False)

    print("Data saved successfully.")

api_key = 'AIzaSyDg16DHjytKsi4JxUoZpQHMtbaxKxNpL1A'
# origin = 'Bùng Binh Phù Đổng'
# destination = '[10.792811, 106.653452]'
origin = "10.792786,106.653508"
destination = "10.771566,106.693125"

def job():
    # Thực hiện lấy dữ liệu và lưu trữ
    data = get_distance_data(origin, destination, api_key)
    result = analyze_traffic(data)
    save_data(result)


# Lập lịch cho công việc chạy mỗi 15 phút
schedule.every().hour.at(':00').do(job)
schedule.every().hour.at(':15').do(job)
schedule.every().hour.at(':30').do(job)
schedule.every().hour.at(':45').do(job)

# Vòng lặp chạy vô hạn để duy trì lập lịch
while True:
    schedule.run_pending()
    time.sleep(15)