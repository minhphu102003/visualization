import pdfplumber
import pandas as pd
import re
from datetime import datetime

def process_content(content):
    # Loại bỏ dấu nháy đơn và kép
    content = content.replace('"', '')
    
    # Tách chuỗi thành các phần dựa vào dấu chấm
    content_parts = content.split('.')
    
    # Tạo danh sách mới để lưu các phần cần giữ lại
    valid_parts = []
    
    # Bỏ qua phần tử đầu tiên và kiểm tra phần tử từ thứ 2 trở đi
    for part in content_parts[1:]:  # Bỏ qua phần đầu tiên
        part = part.strip()  # Loại bỏ khoảng trắng ở đầu và cuối
        if part and part[0].isalpha():  # Nếu phần tử bắt đầu bằng ký tự alphabet
            valid_parts.append(part)
    
    # Gộp lại các phần còn lại thành một chuỗi, ngăn cách bằng dấu chấm
    final_content = '. '.join(valid_parts)
    
    return final_content

def process_string(data_row):
    try:
        # Xử lý một hàng dữ liệu với định dạng: [stt, date, amount, content]
        stt = int(data_row[0].strip())  # Chuyển đổi số thứ tự thành kiểu số nguyên
        date = datetime.strptime(data_row[1].strip(), '%d/%m/%Y').strftime('%d/%m/%Y')  # Định dạng lại ngày
        amount = float(data_row[2].replace('.', '').strip())  # Chuyển đổi số tiền thành kiểu float
        content = process_content(data_row[3].strip())  # Xóa khoảng trắng và xử lý mô tả giao dịch
        
        return [stt, date, amount, content]
    except ValueError:
        # Bỏ qua hàng nếu không thể chuyển đổi stt hoặc amount
        return None

def read_pdf(list_columns, path, poches, output_type=0, file_prefix="output"):
    processed_data = []  # Khởi tạo danh sách để lưu trữ dữ liệu đã xử lý
    row_count = 0  # Đếm số hàng đã xử lý
    mode = 'w'  # Chế độ ghi, ban đầu là 'w' (write - ghi mới), sau đó chuyển thành 'a' (append - nối tiếp)
    
    # File đích sẽ là một file duy nhất, được quyết định bởi output_type
    output_file_excel = f"{file_prefix}.xlsx"
    output_file_csv = f"{file_prefix}.csv"
    
    # Mở file PDF
    with pdfplumber.open(path) as pdf:
        total_pages = len(pdf.pages)
        # Lặp qua từng trang của PDF
        for page_num, page in enumerate(pdf.pages):
            print(f"Đang xử lý trang {page_num + 1}/{total_pages}...")
            
            # Sử dụng phương thức extract_table để trích xuất bảng
            tables = page.extract_tables()
            
            # Kiểm tra và xử lý các bảng
            for table in tables:
                for row in table:
                    if row:  # Kiểm tra nếu hàng không rỗng
                        processed_row = process_string(row)  # Gọi hàm xử lý chuỗi
                        if processed_row:  # Chỉ thêm vào danh sách nếu hàng hợp lệ
                            processed_data.append(processed_row)  # Thêm hàng đã xử lý vào danh sách
                            row_count += 1

                            # Nếu đủ poches hàng, ghi tạm vào file và xóa dữ liệu tạm thời
                            if row_count % poches == 0:
                                df = pd.DataFrame(processed_data, columns=list_columns)
                                if output_type == 0 or output_type == 2:  # Lưu vào Excel nếu output_type là 0 hoặc 2
                                    if mode == 'w':
                                        df.to_excel(output_file_excel, index=False, header=True)
                                    else:
                                        with pd.ExcelWriter(output_file_excel, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                                            df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
                                if output_type == 1 or output_type == 2:  # Lưu vào CSV nếu output_type là 1 hoặc 2
                                    df.to_csv(output_file_csv, index=False, mode=mode, header=(mode == 'w'))
                                
                                processed_data = []  # Reset danh sách sau khi ghi tạm
                                mode = 'a'  # Chuyển sang chế độ append sau lần ghi đầu tiên

                                # In tiến độ theo số dòng đã xử lý
                                print(f"Đã xử lý {row_count} hàng...") 
    
    # Sau khi xử lý xong, nếu còn dữ liệu chưa ghi, ghi nốt
    if processed_data:
        df = pd.DataFrame(processed_data, columns=list_columns)
        if output_type == 0 or output_type == 2:  # Lưu vào Excel nếu output_type là 0  hoặc 2
            if mode == 'w':
                df.to_excel(output_file_excel, index=False, header=True)
            else:
                with pd.ExcelWriter(output_file_excel, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
        if output_type == 1 or output_type == 2:  # Lưu vào CSV nếu output_type là 1 hoặc 2
            df.to_csv(output_file_csv, index=False, mode=mode, header=(mode == 'w'))

if __name__ == '__main__':
    path = 'VCB_13_9_2024.pdf'
    list_columns = ['stt', 'date', 'amount', 'content']
    poches = 500  # Số hàng mỗi lần in và lưu
    output_type = 2  # 0: Excel, 1: CSV, 2: Cả Excel và CSV
    file_prefix = "output_data"  # Tên file lưu trữ
    
    # Gọi hàm và xử lý file PDF
    read_pdf(list_columns=list_columns, path=path, poches=poches, output_type=output_type, file_prefix=file_prefix)