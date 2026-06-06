# 🔬 IndustryLens — Streamlit Edition

> Phân tích xu hướng ngành nghề · Dự báo tăng trưởng · Đề xuất chiến lược

---

## 📦 Link & tài nguyên

| Tài nguyên | Link |
|---|---|
| 🌐 **Demo live** | [industry-lens.streamlit.app](https://industry-lens.streamlit.app) *(sau khi deploy)* |
| ☁️ **Dữ liệu mẫu (Google Drive)** | [Xem/tải sample_data.csv](https://drive.google.com/drive/folders/your_folder_id_here) |
| 📂 **Source code** | Thư mục hiện tại |
| 📋 **Định dạng dữ liệu** | Xem bảng cột bên dưới |

---

## 🚀 Cài đặt & chạy

### Bước 1 — Clone & cài thư viện

```bash
# Clone hoặc giải nén project
cd industry-streamlit

# Cài thư viện
pip install -r requirements.txt
```

### Bước 2 — Cấu hình biến môi trường

```bash
# Sao chép file mẫu
cp .env.local .env

# Mở và điền giá trị thực vào .env
# (xem hướng dẫn lấy GDRIVE_FILE_ID bên dưới)
```

**Nội dung file `.env`:**
```env
GDRIVE_FILE_ID=1ABC...XYZ       # ID file CSV trên Google Drive
GDRIVE_LOCAL_FILENAME=sample_data.csv
```

### Bước 3 — Chạy app

```bash
streamlit run app.py
# → Mở trình duyệt: http://localhost:8501
```

---

## 📖 Hướng dẫn sử dụng

### 1️⃣ Tải dữ liệu lên

Có **3 cách** để nạp dữ liệu:

| Cách | Mô tả |
|------|-------|
| ☁️ **Tải từ Google Drive** | Nhấn "⬇️ Tải từ Drive" trong sidebar — tự động download file mẫu mới nhất |
| 📁 **Upload thủ công** | Kéo thả hoặc chọn file CSV/Excel từ máy tính |
| 🔄 **Cập nhật Drive** | Nhấn "🔄 Cập nhật" để lấy phiên bản mới nhất từ Drive |

### 2️⃣ Đọc kết quả phân tích

Sau khi upload, dashboard hiện 5 KPI chính và **6 tab**:

| Tab | Nội dung |
|-----|---------|
| 📈 **Xu hướng** | Line chart tuyển dụng, lương, điểm tăng trưởng theo thời gian |
| 🔮 **Dự báo** | Dự báo 6 tháng tới bằng Ridge Regression polynomial |
| 📊 **Phân phối** | Donut chart cấp độ kinh nghiệm, cạnh tranh, rủi ro AI; top kỹ năng |
| 🔬 **Nâng cao** | Scatter plot, box plot theo cấp độ, heatmap tương quan |
| 💡 **Chiến lược** | Nhận định tự động, tag ngành/khu vực/vị trí |
| 📋 **Dữ liệu** | Filter + xem raw data, tải CSV đã lọc |

### 3️⃣ Đổi giao diện màu sắc

- Sidebar → **"🎨 Chủ đề màu sắc"** → chọn 1 trong 6 theme
- Sidebar → **"🖌️ Tuỳ chỉnh màu chính"** → color picker tự do

| Theme | Phong cách |
|-------|-----------|
| 🌌 Dark Galaxy | Tối, tím-hồng (mặc định) |
| 🌊 Ocean Depth | Xanh đại dương |
| 🌸 Sakura Light | Sáng, hồng nhẹ |
| 🍃 Forest Calm | Xanh lá tươi mát |
| 🔥 Cyberpunk | Neon tím-vàng mạnh |
| ☁️ Cloud White | Trắng tối giản |

### 4️⃣ Chia sẻ báo cáo

- Nhấn **"🌐 Chia sẻ công khai"** → lưu báo cáo vào thư mục `public_data/`
- Người dùng khác xem lại qua sidebar → **"Báo cáo công khai"**
- Nhấn **"⬇️ Tải báo cáo JSON"** để xuất kết quả phân tích

### 5️⃣ Tạo dữ liệu test

```bash
python generate_sample.py
# → Tạo sample_data.csv với 600 bản ghi ngẫu nhiên
```

---

## ☁️ Cấu hình Google Drive

### Lấy File ID

1. Upload file `sample_data.csv` lên Google Drive
2. Click chuột phải → **"Chia sẻ"** → chọn **"Bất kỳ ai có đường link"**
3. Copy link:
   ```
   https://drive.google.com/file/d/1ABC...XYZ/view?usp=sharing
   ```
4. Lấy phần `1ABC...XYZ` → đó là **File ID**
5. Điền vào `.env`:
   ```env
   GDRIVE_FILE_ID=1ABC...XYZ
   ```

### Cập nhật dữ liệu

Khi muốn cập nhật dataset:
1. Thay file mới lên cùng vị trí trên Drive (giữ nguyên File ID)
2. Mở app → Sidebar → nhấn **"🔄 Cập nhật"**
3. App tự tải phiên bản mới nhất về

---

## 🚀 Deploy lên Streamlit Cloud

### Bước 1 — Push code lên GitHub

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/your-username/industry-lens.git
git push -u origin main
```

> ⚠️ Đảm bảo `.gitignore` đã loại trừ file `.env` và `public_data/`

### Bước 2 — Kết nối Streamlit Cloud

1. Vào [share.streamlit.io](https://share.streamlit.io)
2. **"New app"** → chọn repo GitHub
3. Main file: `app.py`

### Bước 3 — Cấu hình Secrets

Vào **Settings → Secrets** và thêm (định dạng TOML):

```toml
[gdrive]
file_id = "1ABC...XYZ"
local_filename = "sample_data.csv"
```

> Không cần file `.env` khi dùng Streamlit Cloud — app đọc từ `st.secrets` tự động.

---

## 📋 Định dạng dữ liệu

| Cột | Kiểu | Bắt buộc | Mô tả |
|-----|------|----------|-------|
| `date` | Date (YYYY-MM-DD) | ✅ | Ngày ghi nhận |
| `industry` | Text | ✅ | Tên ngành |
| `job_title` | Text | ✅ | Vị trí công việc |
| `region` | Text | ❌ | Khu vực địa lý |
| `job_openings` | Integer | ❌ | Số lượng tuyển dụng |
| `avg_salary` | Float | ❌ | Lương trung bình ($) |
| `salary_growth_rate` | Float | ❌ | Tốc độ tăng lương (%) |
| `experience_level` | Text | ❌ | Fresher / Junior / Senior |
| `remote_ratio` | Integer 0–100 | ❌ | Tỷ lệ làm remote (%) |
| `required_skills` | Text | ❌ | Kỹ năng, cách nhau bằng dấu phẩy |
| `competition_level` | Text | ❌ | Low / Medium / High |
| `automation_risk` | Text | ❌ | Low / Medium / High |
| `growth_score` | Float 0–100 | ❌ | Điểm tăng trưởng ngành |
| `demand_forecast` | Text | ❌ | Growing / Stable / Declining |

> App tự bỏ qua cột thiếu — không cần đủ 14 cột.

---

## 📁 Cấu trúc thư mục

```
industry-streamlit/
├── app.py                  ← App chính (Streamlit)
├── requirements.txt        ← Thư viện Python
├── generate_sample.py      ← Script tạo dữ liệu test
├── .env.local              ← Mẫu biến môi trường (an toàn để commit)
├── .env                    ← Biến thực (KHÔNG commit — đã có trong .gitignore)
├── .gitignore              ← Loại trừ secrets & data
├── README.md               ← Tài liệu này
├── .streamlit/
│   └── config.toml         ← Cấu hình Streamlit (theme mặc định)
├── sample_data.csv         ← (tự tạo) dữ liệu mẫu local
└── public_data/            ← (tự tạo) báo cáo đã chia sẻ
```

---

## 🛠️ Yêu cầu hệ thống

- Python **3.10+**
- pip **23+**
- RAM: tối thiểu **512 MB** (khuyến nghị 1 GB+)
- Kết nối internet để tải font Google và dữ liệu từ Drive

---

## ❓ Câu hỏi thường gặp

**Q: App báo lỗi khi tải từ Drive?**
> Kiểm tra: (1) File ID đúng chưa, (2) File đã được set "Bất kỳ ai có link", (3) `gdown` đã cài chưa (`pip install gdown`)

**Q: Biểu đồ không hiển thị?**
> Đảm bảo cột `date` đúng định dạng `YYYY-MM-DD` và có ít nhất 3 dòng dữ liệu.

**Q: Làm sao thêm ngôn ngữ khác?**
> Sửa các chuỗi text trong `app.py` — phần tiêu đề, nhãn biểu đồ và insights đều là plain string.

**Q: File .env có bị lộ không?**
> Không, nếu bạn không xóa `.env` khỏi `.gitignore`. File `.env.local` là mẫu an toàn.
