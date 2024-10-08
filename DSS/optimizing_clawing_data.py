from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# Cấu hình Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")


# Thread-safe list for storing scores
all_scores = []
lock = Lock()  # To prevent race conditions when appending to the list

def get_data(driver, code, year):
    try:
        # Tạo URL với mã và năm
        url = f"https://diemthi.vnanet.vn/Home/SearchBySobaodanh?code={code}&nam={year}"
        
        # Mở trang web
        driver.get(url)
        
        # Đợi trang tải (nếu cần)
        time.sleep(1)  # Can adjust this time if needed
        
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

def scrape_city(codeCity):
    nam = 2018
    codeStudent = 1
    none_count = 0
    continue_none_count = 10
    
    # Mỗi thread khởi tạo driver riêng
    driver = webdriver.Chrome(options=chrome_options)
    
    for j in range(10**5):
        code_str = str(codeCity).zfill(2) + str(codeStudent + j).zfill(6)  # Tạo mã số báo danh
        year = nam

        # Lấy dữ liệu
        scores = get_data(driver, code_str, year)

        if scores:
            # Sử dụng lock để đảm bảo việc ghi vào all_scores an toàn
            with lock:
                all_scores.append(scores)
            none_count = 0  # Reset lại none_count nếu có dữ liệu
        elif j > 2000:
            none_count += 1  # Tăng đếm nếu không có dữ liệu khi j > 2000
            if none_count > continue_none_count:
                print(f"Dừng lại sau {continue_none_count} lần liên tiếp không có dữ liệu cho tỉnh {codeCity}.")
                break
    
    driver.quit()  # Đóng trình duyệt sau khi hoàn thành
 
if __name__ == "__main__":
    # Tạo ThreadPoolExecutor với 10 luồng chạy song song
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(scrape_city, range(1, 101))  # Scrape 100 cities in parallel

    # Chuyển đổi mảng scores thành DataFrame và ghi vào file CSV
    df = pd.DataFrame(all_scores)
    df.to_csv("scores.csv", index=False, encoding='utf-8-sig')
