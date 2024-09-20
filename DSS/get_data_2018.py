from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import pandas as pd

# Cấu hình Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Chạy trình duyệt trong chế độ không có giao diện đồ họa
chrome_options.add_argument("--disable-gpu")  # Vô hiệu hóa GPU (tăng hiệu suất trong môi trường không có GUI)
chrome_options.add_argument("--no-sandbox")  # Bỏ qua sandbox (nếu cần trên Linux)

# Đường dẫn tới ChromeDriver (bạn cần thay thế đường dẫn này)
driver_path = "path/to/chromedriver"

# Khởi tạo trình duyệt
driver = webdriver.Chrome(options=chrome_options)

def get_data(code, year):
    try:
        # Tạo URL với mã và năm
        url = f"https://diemthi.vnanet.vn/Home/SearchBySobaodanh?code={code}&nam={year}"
        
        # Mở trang web
        driver.get(url)
        
        # Đợi trang tải (nếu cần)
        time.sleep(1)  # Tùy chỉnh thời gian nếu cần
        
        # Tìm và lấy dữ liệu (sử dụng các phương pháp của Selenium)
        result_element = driver.find_element(By.XPATH, '/html/body/pre')
        data = result_element.text

        # Chuyển đổi dữ liệu từ string sang JSON
        json_data = json.loads(data)

        # Kiểm tra nếu có dữ liệu trong trường "result"
        if json_data["result"]:
            print(code) 
            scores = {
                "SBD": code,
                "Toan": json_data["result"][0].get("Toan", None),
                "NguVan": json_data["result"][0].get("NguVan", None),
                "NgoaiNgu": json_data["result"][0].get("NgoaiNgu", None),
                "VatLi": json_data["result"][0].get("VatLi", None),
                "HoaHoc": json_data["result"][0].get("HoaHoc", None),
                "KHTN": json_data["result"][0].get("KHTN", None),
                "DiaLi": json_data["result"][0].get("DiaLi", None),
                "LichSu": json_data["result"][0].get("LichSu", None),
                "GDCD": json_data["result"][0].get("GDCD", None),
                "KHXH": json_data["result"][0].get("KHXH", None)
            }
            return scores
        else:
            return None

    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")
        return None

if __name__ == "__main__":
    nam = 2018
    code = 1000001
    all_scores = []  # Mảng để chứa tất cả điểm

    for i in range(6):
        for j in range(10**9-1-10**7):  # Giới hạn vòng lặp để tránh quá nhiều request
            code_str = str((code + j)).zfill(8)  # đảm bảo mã có đúng 8 chữ số
            year = nam + i
            scores = get_data(code_str, year)
            if scores:
                all_scores.append(scores)

    # Chuyển đổi mảng scores thành DataFrame và ghi vào file CSV
    df = pd.DataFrame(all_scores)
    df.to_csv("scores.csv", index=False, encoding='utf-8-sig')

# Đóng trình duyệt khi hoàn thành
driver.quit()