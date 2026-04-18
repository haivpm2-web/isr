# ISR Hospital Management System

Hệ thống quản lý bệnh viện phục hồi chức năng – Django Web App.

## Tính năng

| Vai trò | Chức năng |
|---|---|
| **Admin** | Tạo / xóa / vô hiệu hóa tài khoản bệnh nhân, bác sĩ, điều dưỡng, admin |
| **Bác sĩ** | Xem hồ sơ bệnh nhân, xem thống kê, kê đơn thuốc |
| **Điều dưỡng / Y tá** | Nhập kết quả ECG, dữ liệu khám, dữ liệu phục hồi, đánh giá PHCN |
| **Bệnh nhân** | Xem thông số ECG, xem tiến trình phục hồi chân (chỉ đọc) |

### Thông số ECG theo dõi
- Nhịp tim (bpm), khoảng PR / QRS / QT / QTc / RR (ms)
- Biên độ sóng P / QRS / T (mV)
- Thay đổi đoạn ST (mm)
- Loại nhịp (15 dạng: xoang, rung nhĩ, block, PVC…)
- Biểu đồ xu hướng nhịp tim theo thời gian

### Thông số phục hồi chân
- Tỷ lệ phục hồi (%)
- Sức mạnh cơ – thang MRC 0–5
- Biên độ vận động (độ)
- Mức độ đau – thang VAS 0–10
- Mức độ sưng (0–3)
- Khả năng đi lại (7 mức)
- Ghi chú vật lý trị liệu & bác sĩ
- Biểu đồ tiến trình phục hồi theo thời gian

---

## Cài đặt

### 1. Tạo môi trường ảo & cài thư viện

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Migrate database

```bash
python manage.py migrate
```

### 3. Tạo tài khoản Admin đầu tiên

```bash
python manage.py createsuperuser
```

Sau đó đăng nhập vào `/admin/` và thay đổi `role` của tài khoản superuser thành `admin`, hoặc chạy:

```bash
python manage.py shell
```
```python
from accounts.models import CustomUser
u = CustomUser.objects.get(username='your_admin_username')
u.role = 'admin'
u.save()
```

### 4. Chạy server

```bash
python manage.py runserver
```

Truy cập: **http://127.0.0.1:8000**

---

## Deploy Railway

### 1. Tạo project trên Railway

- Push source code lên GitHub
- Trong Railway, chọn **New Project** → **Deploy from GitHub repo**
- Add service **PostgreSQL** trong cùng project

### 2. Cấu hình biến môi trường

Thiết lập các biến sau trong Railway:

```env
DJANGO_SECRET_KEY=your-strong-secret-key
DJANGO_DEBUG=False
```

`DATABASE_URL` sẽ được Railway tự cấp khi bạn thêm PostgreSQL.

App hiện tự đọc `RAILWAY_PUBLIC_DOMAIN` do Railway cung cấp để thêm vào `ALLOWED_HOSTS` và `CSRF_TRUSTED_ORIGINS`. Bạn chỉ cần khai báo thêm `DJANGO_ALLOWED_HOSTS` hoặc `DJANGO_CSRF_TRUSTED_ORIGINS` nếu dùng custom domain hoặc muốn mở rộng thêm host khác.

### 3. Deploy

Project đã có sẵn file `railway.json`, Railway sẽ tự chạy:

```bash
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn hospital_isr.wsgi --bind 0.0.0.0:$PORT
```

### 4. Lưu ý

- Không nên dùng SQLite trên Railway nếu không gắn volume persistent
- Static files đã được cấu hình qua WhiteNoise
- Nếu dùng custom domain, thêm domain đó vào `DJANGO_ALLOWED_HOSTS` và `DJANGO_CSRF_TRUSTED_ORIGINS`

---

## Cấu trúc project

```
ISR/
├── manage.py
├── requirements.txt
├── hospital_isr/          # Django settings
│   ├── settings.py
│   └── urls.py
├── accounts/              # Quản lý tài khoản & auth
├── patients/              # Model + view bệnh nhân, ECG, phục hồi
├── doctors/               # Model + view bác sĩ
├── templates/             # Toàn bộ HTML templates
│   ├── base.html
│   ├── accounts/
│   ├── patients/
│   └── doctors/
└── static/css/            # Stylesheet
```

---

## Luồng sử dụng

1. **Admin** đăng nhập → Tạo tài khoản bác sĩ và điều dưỡng
2. **Admin** tạo tài khoản bệnh nhân, phân công bác sĩ
3. **Điều dưỡng / Y tá** đăng nhập → Nhập ECG / khám / phục hồi / PHCN
4. **Bác sĩ** đăng nhập → Xem thống kê, xem hồ sơ và kê đơn thuốc
5. **Bệnh nhân** đăng nhập → Xem kết quả ECG và tiến trình phục hồi của mình
