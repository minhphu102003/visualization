import os
import json

# Hàm đổi tên file
def rename_files_in_folder(folder_path, output_json_path):
    try:
        # Kiểm tra thư mục có tồn tại không
        if not os.path.exists(folder_path):
            print(f"Thư mục {folder_path} không tồn tại.")
            return
        files = os.listdir(folder_path)
        if not files:
            print("Thư mục không có file nào.")
            return
        # Tạo danh sách lưu trữ thông tin đổi tên
        renamed_files = []
        # Lặp qua từng file và đổi tên
        for file_name in files:
            old_file_path = os.path.join(folder_path, file_name)
            # Bỏ qua nếu là thư mục
            if os.path.isdir(old_file_path):
                continue
            # Tách phần số và tên tỉnh dựa trên "-"
            parts = file_name.split("-")
            if len(parts) < 2:
                print(f"Bỏ qua file không hợp lệ: {file_name}")
                continue
            # Lấy số (loại bỏ số 0 ở đầu) và phần mở rộng
            file_number = int(parts[0])  # Loại bỏ số 0 vô nghĩa
            province_name = parts[1].split(".")[0]  # Lấy tên tỉnh (bỏ phần mở rộng)
            file_extension = os.path.splitext(file_name)[1]  # Lấy phần mở rộng
            # Tạo tên file mới
            new_file_name = f"{file_number}{file_extension}"
            new_file_path = os.path.join(folder_path, new_file_name)
            # Đổi tên file
            os.rename(old_file_path, new_file_path)
            # Thêm vào danh sách
            renamed_files.append({"key": file_number, "value": province_name})
        # Ghi danh sách vào file JSON
        save_to_json(output_json_path, renamed_files)
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# Hàm ghi file JSON
def save_to_json(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Đã xảy ra lỗi khi ghi file JSON: {e}")

# Hàm đọc file JSON
def read_from_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        print(f"Đã xảy ra lỗi khi đọc file JSON: {e}")
        return None

if __name__== '__main__':
    # Sử dụng chương trình
    folder_path = './DataSet/HSG'
    output_json_path = 'dictionary_province.json'

    rename_files_in_folder(folder_path, output_json_path)

    data = read_from_json(output_json_path)
    if data:
        print("Nội dung file JSON:", data)
