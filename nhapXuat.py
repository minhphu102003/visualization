import cmath

def nhap():
    x = input('Nhập giá trị tuổi: ')
    return x

def xuat(x):
    print(f"Giá trị tuổi của bạn là {x}")

def nhap_he_so():
    a = float(input("Nhập hệ số a (a ≠ 0): "))
    while a == 0:
        print("Hệ số a phải khác 0. Vui lòng nhập lại.")
        a = float(input("Nhập hệ số a (a ≠ 0): "))
    
    b = float(input("Nhập hệ số b: "))
    c = float(input("Nhập hệ số c: "))
    return a, b, c

def giai_phuong_trinh_bac_hai(a, b, c):
    delta = b**2 - 4*a*c
    
    if delta > 0:
        x1 = (-b + cmath.sqrt(delta)) / (2*a)
        x2 = (-b - cmath.sqrt(delta)) / (2*a)
        return x1, x2
    elif delta == 0:
        x = -b / (2*a)
        return x, x
    else:
        x1 = (-b + cmath.sqrt(delta)) / (2*a)
        x2 = (-b - cmath.sqrt(delta)) / (2*a)
        return x1, x2

def xuat_nghiem(nghiem):
    if isinstance(nghiem, tuple):
        print(f"Nghiệm của phương trình là x1 = {nghiem[0]} và x2 = {nghiem[1]}")
    else:
        print(f"Phương trình có nghiệm kép x = {nghiem}")

if __name__ == '__main__':
    # x = nhap()
    # xuat(x)
    a, b, c = nhap_he_so()
    nghiem = giai_phuong_trinh_bac_hai(a, b, c)
    xuat_nghiem(nghiem)

