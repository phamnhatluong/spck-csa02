# 🔬 IndustryLens — Streamlit Edition

Web app phân tích xu hướng ngành nghề, dự báo tăng trưởng và đề xuất chiến lược.
Giao diện **Streamlit** — chạy ngay, không cần frontend riêng.

---

## 🚀 Cài đặt & Chạy

```bash
# 1. Cài thư viện
pip install -r requirements.txt

# 2. Tạo dữ liệu mẫu (tuỳ chọn)
python generate_sample.py

# 3. Chạy app
streamlit run app.py

# Mở trình duyệt: http://localhost:8501
```

---

## 🎨 Tính năng nổi bật

| Tính năng | Mô tả |
|-----------|-------|
| **6 chủ đề màu** | Dark Galaxy, Ocean Depth, Sakura Light, Forest Calm, Cyberpunk, Cloud White |
| **Tuỳ chỉnh màu chính** | Color picker tự do trong sidebar |
| **Upload CSV/Excel** | Kéo thả hoặc chọn file, tối đa 50MB |
| **6 tab phân tích** | Xu hướng · Dự báo · Phân phối · Nâng cao · Chiến lược · Dữ liệu |
| **13+ loại biểu đồ** | Line, Bar, Donut, Pie, Scatter, Box, Heatmap, Dual-axis |
| **Dự báo 6 tháng** | Hồi quy đa thức (Ridge Regression) |
| **Nhận định tự động** | AI insights từ pattern dữ liệu |
| **Chia sẻ công khai** | Lưu & xem lại báo cáo của người khác |
| **Tải báo cáo JSON** | Export kết quả phân tích |
| **Lọc dữ liệu** | Filter theo ngành, khu vực, cấp độ |

---

## 📋 Định dạng dữ liệu

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `date` | Date | Ngày (YYYY-MM-DD) |
| `industry` | Text | Tên ngành |
| `job_title` | Text | Vị trí công việc |
| `region` | Text | Khu vực địa lý |
| `job_openings` | Number | Số lượng tuyển dụng |
| `avg_salary` | Number | Lương trung bình |
| `salary_growth_rate` | Number | Tốc độ tăng lương (%) |
| `experience_level` | Text | Fresher / Junior / Senior |
| `remote_ratio` | Number | Tỷ lệ remote (0–100) |
| `required_skills` | Text | Kỹ năng, phân cách bằng dấu phẩy |
| `competition_level` | Text | Low / Medium / High |
| `automation_risk` | Text | Low / Medium / High |
| `growth_score` | Number | Điểm tăng trưởng (0–100) |
| `demand_forecast` | Text | Growing / Stable / Declining |

> Không cần đủ tất cả cột — app tự bỏ qua cột thiếu.

---

## 📁 Cấu trúc thư mục

```
industry-streamlit/
├── app.py                 ← App chính
├── requirements.txt       ← Thư viện
├── generate_sample.py     ← Tạo dữ liệu test
├── sample_data.csv        ← (sau khi chạy generate)
├── public_data/           ← Báo cáo đã chia sẻ (tự tạo)
└── .streamlit/
    └── config.toml        ← Cấu hình Streamlit
```
